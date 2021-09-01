from time import sleep
import numpy as np
from glob import glob
from cypherTools import encrypt_byte_list, encrypt_text, decrypt_text, decrypt_byte_list, get_hash
from sqlalchemy import create_engine, Table, Column, MetaData, String, Integer, LargeBinary, insert, select

class goIncognito:
    all_videos = glob("*.mp4") + glob("*.mkv") + glob("*.mov")
    all_files = glob("*.loc")

    def __init__(self):
        pass

    def create_table(self):
        self.video_content = Table("Video Content", self.metadata,
        Column("name", String, nullable=False),
        Column("name_code", LargeBinary, nullable=False),
        Column("ext", String(4), nullable=False),
        Column("encrypted_bytes", LargeBinary, nullable=False))

        self.metadata.create_all()

    def check_exists(self):
        video_in_file = self.engine.execute(select(self.video_content)).all()
        if len(video_in_file) != 0:
            return True
        return False

    def validate_save_name(self, imgname, imgext):
        imgnamecopy = imgname
        for i in range(2, 1000):
            if len(glob(f"{imgname}.{imgext}")) != 0:
                imgname = imgnamecopy + f' ({i})'
            else:
                break
        return f"{imgname}.{imgext}"

    def instantiate_video_info(self, vid_name):
        *vid_name, self.vid_ext = vid_name.split(".")
        self.vid_name = ''.join(vid_name)
        self.engine = create_engine(f"sqlite:///{get_hash(self.vid_name, 'j&42n$(@%njb6(*&(MRFW@))-)')}.loc") # extra bullshit added to ensure security
        self.metadata = MetaData(bind=self.engine)
        self.create_table()
        return self.check_exists()

    def extract_video_info(self, file_name):
        self.engine = create_engine(f"sqlite:///{file_name}")
        self.metadata = MetaData(bind=self.engine)
        self.create_table()

        video_in_file = self.engine.execute(select(self.video_content)).all()
        if len(video_in_file) == 0:
            return False

        for video in video_in_file:
            self.vid_name = decrypt_text(video.name,  list(video.name_code))
            self.vid_ext = video.ext
            self.vidbytearray = decrypt_byte_list(np.frombuffer(video.encrypted_bytes, dtype=np.uint8))
        return True

    def encrypt(self):
        print(self.all_videos)
        for video in self.all_videos:
            is_exist = self.instantiate_video_info(video)
            if is_exist:
                print(f"\"{self.vid_name}\" excluded...Please change name and try again")
                continue

            encrypted_bytearray = encrypt_byte_list(np.fromfile(video, dtype=np.uint8))
            encrypted_vidname, vidnamecode = encrypt_text(self.vid_name).values()
            sleep(0.1)

            self.engine.execute(insert(self.video_content),
            [{"name": encrypted_vidname,
            "name_code": bytes(vidnamecode),
            "ext": self.vid_ext,
            "encrypted_bytes": encrypted_bytearray.tobytes()}])
            sleep(0.2)

    def decrypt(self):
        print(self.all_files)
        for file in self.all_files:
            has_video = self.extract_video_info(file)
            if not has_video:
                continue
            sleep(0.1)

            vid_title = self.validate_save_name(self.vid_name, self.vid_ext)
            with open(vid_title, 'wb') as vidfile:
                vidfile.write(self.vidbytearray.tobytes())
            sleep(0.2)

incognito = goIncognito()
incognito.encrypt()
