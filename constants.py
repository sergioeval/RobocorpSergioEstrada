import inspect
# NEWS_URL = "https://apnews.com/"
NEWS_URL = "https://www.nbcnews.com/"
PICTURES_PATH = "output/pictures/"
OUTPUT_BASE_PATH = "output/"
LOGGING_PATH = "output/logs/"
LOG_MESSAGES = {
    "info": "*** INFO ***"
}


class FailedCustomException(Exception):
    def __init__(self, message, source, file_name):
        self.message = str(message)  # .replace(":", "").replace(",", "")
        self.source = source
        self.file_name = file_name
        super().__init__(self.message)

    def __str__(self):
        return f'{{"message": *** {self.message} ***, "source_file_name": {self.file_name}, "sorce_function_name": {self.source}}}'
    pass
