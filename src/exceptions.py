

class ShortenerException(Exception):
    pass


class NonexistentUrlException(ShortenerException):
    pass


class SlugAlreadyExistsException(ShortenerException):
    pass

class InvalidUrlException(ShortenerException):
    pass