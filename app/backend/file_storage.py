import os
import shutil

from werkzeug.utils import secure_filename

from app.backend.config import UPLOAD_FOLDER


class EventStorage:
    def saved_as(self):
        ...


class LocalFileStorage(EventStorage):
    file = None

    def __init__(self, file):
        self.file = file

    def saved_as(self):
        filename = secure_filename(self.file.filename)
        saved_at = os.path.join(UPLOAD_FOLDER, filename)
        with open(saved_at, "wb") as buffer:
            shutil.copyfileobj(self.file.file, buffer)

        return os.path.abspath(saved_at)
