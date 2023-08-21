from abc import ABC, abstractmethod
from .mailing import Request, Response

class SendAbility(ABC):
    """发送部分的协议实现"""

    @property
    @abstractmethod
    def protocol(self) -> str:
        """协议名称"""
        raise NotImplementedError

    @abstractmethod
    async def send(self, request: Request) -> Response:
        """发送邮件"""
        raise NotImplementedError

class ReceiveAbility(ABC):
    """接收部分的协议实现"""

    @property
    @abstractmethod
    def protocol(self) -> str:
        """协议名称"""
        raise NotImplementedError

    @abstractmethod
    async def receive(self, request: Request) -> Response:
        """接收邮件"""
        raise NotImplementedError

class ConnectAbility(ABC):
    """连接部分的协议实现"""

    @property
    @abstractmethod
    def protocol(self) -> str:
        """协议名称"""
        raise NotImplementedError

    @abstractmethod
    async def connect(self, request: Request) -> Response:
        """连接邮件服务器"""
        raise NotImplementedError

class MailBoxOperateAbility(ABC):
    """邮箱操作部分的协议实现"""

    @property
    @abstractmethod
    def protocol(self) -> str:
        """协议名称"""
        raise NotImplementedError

    @abstractmethod
    async def operate(self, request: Request) -> Response:
        """邮箱操作"""
        raise NotImplementedError
