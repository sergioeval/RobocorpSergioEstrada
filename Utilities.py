import inspect
from RPA.Archive import Archive
from constants import (
    LOGGING_PATH,
    OUTPUT_BASE_PATH
)
import re
from robocorp import workitems


class FailedCustomException(Exception):
    def __init__(self, message, source, file_name):
        self.message = str(message)  # .replace(":", "").replace(",", "")
        self.source = source
        self.file_name = file_name
        super().__init__(self.message)

    def __str__(self):
        return f'\nmessage: *** {self.message} ***\nsource_file_name: *** {self.file_name} ***\nsorce_function_name: *** {self.source} ***'
    pass


def archive_all():
    arc = Archive()
    arc.archive_folder_with_zip(
        folder=LOGGING_PATH, archive_name=OUTPUT_BASE_PATH+"logs.zip")


def check_contains_money_amount(text):
    pattern = r'\$\d{1,3}(,\d{3})*(\.\d{1,2})?|(\d+ (dollars|USD))'
    return bool(re.search(pattern, text))


def save_work_items(payloads):
    for payload in payloads:
        workitems.outputs.create(payload)
