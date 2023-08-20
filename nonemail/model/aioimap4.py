from ssl import SSLContext
from aioimaplib import (
    IMAP4 as IMAP4_BASE,
    IMAP4_SSL,
    Response as ImapResponse,
    Command,
)
from dataclasses import dataclass

from .mailing import Request as BaseRequest
from .ability import ConnectAbility, ReceiveAbility, MailBoxOperateAbility


@dataclass
class ConnectReq(BaseRequest):
    """Email邮箱连接请求类"""

    server: str
    port: int
    username: str
    password: str


class AIOIMAP4(ConnectAbility, ReceiveAbility, MailBoxOperateAbility):
    @property
    def protocol(self) -> str:
        return "IMAP4"

    @property
    async def impl(self):
        return self.client

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
                ssl_context=ssl_content,  # type: ignore
            )

    async def receive(self, timeout: int = 30) -> ImapResponse:
        return await self.client.wait_server_push(timeout=timeout)

    async def operate(self, cmd: Command) -> ImapResponse:
        assert self.client.protocol is not None
        return await self.client.protocol.execute(cmd)
