

class NotFoundError(Exception):
    """ Intended for cases when a requested resource does not exist in the database """
    pass


class BadRequestError(Exception):
    """ Intended for cases when an API request is malformed or invalid """
    pass
