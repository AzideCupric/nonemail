from ssl import SSLContext
from aioimaplib import IMAP4 as IMAP4_BASE, IMAP4_SSL
from dataclasses import dataclass, KW_ONLY

from .mailing import Request as BaseRequest, Response as BaseResponse
from .ability import ConnectAbility, ReceiveAbility, MailBoxOperateAbility


@dataclass
class ConnectReq(BaseRequest):
    """Email邮箱连接请求类"""

    server: str
    port: int
    username: str
    password: str


class IMAP4(ConnectAbility, ReceiveAbility, MailBoxOperateAbility):
    @property
    def protocol(self) -> str:
        return "IMAP4"

    async def connect(
        self,
        request: ConnectReq,
        timeout: int = 30,
        ssl: bool = True,
        ssl_content: SSLContext | None = None,
    ) -> None:
        if ssl:
            self.client = IMAP4_SSL(
                host=request.server,
                port=request.port,
                timeout=timeout,
                ssl_context=ssl_content,  # type: ignore
            )
        else:
            self.client = IMAP4_BASE(
                host=request.server,
                port=request.port,
                timeout=timeout,
                ssl_context=ssl_content, # type: ignore
            )
