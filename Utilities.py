import inspect
from RPA.Archive import Archive
from constants import (
    LOGGING_PATH,
    OUTPUT_BASE_PATH
)


class FailedCustomException(Exception):
    def __init__(self, message, source, file_name):
        self.message = str(message)  # .replace(":", "").replace(",", "")
        self.source = source
        self.file_name = file_name
        super().__init__(self.message)

    def __str__(self):
        return f'{{"message": *** {self.message} ***, "source_file_name": {self.file_name}, "sorce_function_name": {self.source}}}'
    pass


def archive_all():
    arc = Archive()
    arc.archive_folder_with_zip(
        folder=LOGGING_PATH, archive_name=OUTPUT_BASE_PATH+"logs.zip")
