
# Exception for all provider related errors
class ProviderError(Exception):
    def __init__(self, message:str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

# Exception for 4xx errors
class ProviderClientError(ProviderError):
    pass

# Exception for 5xx errors
class ProviderServerError(ProviderError):
    pass

# Exception when provider takes too long to respond
class ProviderTimeoutError(ProviderError):
    def __int__(self, message: str = "Provider's request timed out"):
        super().__init__(message, status_code=504)

# Exception when every provider fails
class AllProvidersFailedError(Exception):
    pass

