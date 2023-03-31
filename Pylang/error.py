class Error(Exception):
    """Base class for other exceptions"""
    pass

class MinssingKeyError(Error):
    """Raised when not found function in list"""
    pass

class NotFoundDefaultLang(Error):
    """Raised when not found variable in dict"""
    pass

class MatchLangError(Error):
    """Raised when value is not a list"""
    pass

class NotLangLoaded(Error):
    """Raised when custom function dont return string"""
    pass

# class BadComparatorError(Error):
#     """Raised when not valide comparator is pass to parseCondition"""
#     pass