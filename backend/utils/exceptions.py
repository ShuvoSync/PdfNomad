# Custom app exceptions can go here
class PDFNomadException(Exception):
    def __init__(self, message: str):
        self.message = message
