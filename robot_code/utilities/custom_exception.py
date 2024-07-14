

class FailedCustomException(Exception):
    def __init__(self, message, source, file_name):
        self.message = str(message)  # .replace(":", "").replace(",", "")
        self.source = source
        self.file_name = file_name
        super().__init__(self.message)

    def __str__(self):
        return f'\nmessage: *** {self.message} ***\nsource_file_name: *** {self.file_name} ***\nsorce_function_name: *** {self.source} ***'
    pass
