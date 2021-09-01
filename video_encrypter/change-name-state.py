from glob import glob
from sqlalchemy import create_engine, Table, Column, MetaData, String, Integer, LargeBinary, insert, select
from cypherTools import decrypt_text, get_hash
import os


class changeNameState:
    files = glob("*.loc")

    def create_table(self):
        self.video_content = Table("Video Content", self.metadata,
        Column("name", String, nullable=False),
        Column("name_code", LargeBinary, nullable=False),
        Column("ext", String(4), nullable=False),
        Column("encrypted_bytes", LargeBinary, nullable=False))

        self.metadata.create_all()

    def connect_to(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.metadata = MetaData(bind=self.engine)
        self.create_table()

    def extract_name_info(self):
        video_in_file = self.engine.execute(select(self.video_content)).all()
        if len(video_in_file) == 0:
            return (False, None)

        for video in video_in_file:
            return (True, decrypt_text(video.name, list(video.name_code)))

    def show(self):
        for file in self.files:
            self.connect_to(file)
            name_exists, file_name = self.extract_name_info()
            if not name_exists:
                continue

            if file != file_name + ".loc":
                os.rename(file, file_name + ".loc")

    def hide(self):
        for file in self.files:
            self.connect_to(file)
            name_exists, file_name = self.extract_name_info()
            if not name_exists:
                continue

            default_hide_name = get_hash(file_name, 'j&42n$(@%njb6(*&(MRFW@))-)') + ".loc"
            if file != default_hide_name:
                os.rename(file, default_hide_name)


namestate = changeNameState()
shownamestate = namestate.show
hidenamestate = namestate.hide
# shownamestate()
