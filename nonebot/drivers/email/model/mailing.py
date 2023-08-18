from abc import ABC, abstractmethod

Domain = str

class Request(ABC):
    """请求类"""
    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

class Response(ABC):
    """响应类"""
    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError
