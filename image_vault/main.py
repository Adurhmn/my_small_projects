# jpg, jpeg, jfif, tiff, bmp, webp, gif, png,
from helper_tools import encrypt_text, decrypt_text, encrypt_byte_list, decrypt_byte_list
from sqlalchemy import create_engine, MetaData, Table, Column, String, insert, select, delete, LargeBinary
from hashlib import md5
import os
from glob import glob
from tqdm import tqdm
import numpy as np
from hashlib import md5
PASSWORD_HASH = "9a618248b64db62d15b300a07b00580b" # replace with your desired password hash(md5)

class Stash():
    engine = create_engine(f"sqlite:///stash.loc")
    metadata = MetaData(engine)

    def __init__(self):
        '''Creates DataBase&Table if they does not exists'''
        self.picStash = Table("picStash", self.metadata,
                Column("picName", String),
                Column("picNameCode", LargeBinary),
                Column("picExtension", String(4)),
                Column("picEncryptedByte", LargeBinary),
                Column("picNameHash", String(32)))
        self.metadata.create_all()
        self.duplicateimg_log = list()

    def validate_save_name(self, imgname, imgext):
        imgnamecopy = imgname
        for i in range(2, 1000):
            if len(glob(f"{imgname}.{imgext}")) != 0:
                imgname = imgnamecopy + f' ({i})'
            else:
                break
        return f"{imgname}.{imgext}"

    def get_pics(self):
        pics = list()
        pics += glob("*.png") + glob("*.jpg") + glob("*.jpeg") + glob("*.gif") + glob("*.tiff") + glob("*.bmp") + glob("*.webp") + glob("*.jfif")
        return pics

    def check_preexists(self, img_name):
        pre_existing = self.engine.execute(select(self.picStash).where(self.picStash.c.picNameHash == self.nameHash)).all()
        if pre_existing:
            self.duplicateimg_log.append(img_name)

    def interpret_img_info(self, img_name_raw):
        *img_name, self.img_ext = img_name_raw.split('.')
        self.img_name = ''.join(img_name)
        self.encrypted_img_name = encrypt_text(self.img_name)
        self.nameHash = str(md5(bytes(self.img_name, encoding='utf-8')).hexdigest())
        self.check_preexists(img_name_raw)

    def stash_all(self):
        pics = self.get_pics()
        if not pics:
            print("No images found..!")
            return

        for pic in tqdm(pics, desc="Stashing"):
            # INSTANTIATES CURRENT IMAGE DETAILS
            self.interpret_img_info(pic)

            # CHECKS IF IMAGE FILE IS CORRUPTED OR DUPLICATE
            if pic in self.duplicateimg_log:
                continue

            encrypted_imgbytes = encrypt_byte_list(np.fromfile(pic, dtype=np.uint8)) #encrypts image bytes

            self.engine.execute(insert(self.picStash),
            [{"picName": self.encrypted_img_name['data'],
              "picNameCode": bytes(self.encrypted_img_name['code']),
              "picExtension": self.img_ext,
              "picEncryptedByte": encrypted_imgbytes.tobytes(),
              "picNameHash": self.nameHash}])

            os.remove(pic)
        print("Stashing Successfull.")

        if self.duplicateimg_log:
            print(f"\n\n\n\tDUPLICATE IMAGES -->The below files cannot be stashed with this name since other files in stash already have the same name:\n\t\t{self.duplicateimg_log}")

    def unstash_all(self):
        pics = self.engine.execute(select(self.picStash)).all()
        if not pics:
            print("Stash is empty..!")
            return

        for pic in tqdm(pics, desc="Unstashing"):
            img_name = self.validate_save_name(imgname=decrypt_text(pic.picName, list(pic.picNameCode)), imgext=pic.picExtension)
            with open(img_name, 'wb') as imgfile:
                imgbyte = decrypt_byte_list(np.frombuffer(pic.picEncryptedByte, dtype=np.uint8))
                imgfile.write(imgbyte)
            self.engine.execute(delete(self.picStash).where(self.picStash.c.picNameHash == pic.picNameHash))
        print("Unstashing Successfull.")

password = input("Enter Stash Password:>")
if str(md5(bytes(password, "utf-8")).hexdigest()) == PASSWORD_HASH:
    st = time.time()
    stash_app = Stash()
    stash_app.unstash_all()
