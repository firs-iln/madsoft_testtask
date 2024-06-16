class InvalidSchemaError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidDataError(InvalidSchemaError):
    pass


class NotFoundException(Exception):
    pass
    # def __init__(self, message: str):
    #     super().__init__(message)
