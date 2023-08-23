from ssl import SSLContext
from asyncio import AbstractEventLoop
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
    timeout: int = 30
    mailbox: str = "INBOX"
    ssl: bool = True
    ssl_content: SSLContext | None = None
    loop: AbstractEventLoop | None = None


class AIOIMAP4(ConnectAbility, ReceiveAbility, MailBoxOperateAbility):
    @property
    def sub_procotol(self) -> str:
        return "AIOIMAP4"

    @property
    def impl(self):
        return self._client

    async def connect(
        self,
        request: ConnectReq,
    ) -> "AIOIMAP4":
        if request.ssl:
            self._client = IMAP4_SSL(
                host=request.server,
                port=request.port,
                timeout=request.timeout,
                ssl_context=request.ssl_content,  # type: ignore
            )
        else:
            self._client = IMAP4_BASE(
                host=request.server,
                port=request.port,
                timeout=request.timeout,
                ssl_context=request.ssl_content,  # type: ignore
                loop=request.loop, # type: ignore
            )

        await self._client.wait_hello_from_server()
        await self._client.login(request.username, request.password)
        return self

    async def receive(self, timeout: int = 30) -> ImapResponse:
        return await self.impl.wait_server_push(timeout=timeout)

    async def operate(self, cmd: Command) -> ImapResponse:
        assert self.impl.protocol is not None
        return await self.impl.protocol.execute(cmd)

    async def select(self, mailbox: str = "INBOX") -> ImapResponse:
        return await self.impl.select(mailbox)

    async def idle_start(self, timeout: int = 30):

        return await self.impl.idle_start(timeout=timeout)

    def idle_done(self):

        return self.impl.idle_done()
