

class ShortenerException(Exception):
    pass


class NonexistentUrlException(ShortenerException):
    pass


class SlugAlreadyExistsException(ShortenerException):
    pass