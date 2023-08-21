from types import TracebackType, NoneType
from typing_extensions import Self
from .procotol.aioimap4 import AIOIMAP4, ConnectReq
from .procotol.aiosmtp import AIOSMTP


class EmailClient(AIOSMTP, AIOIMAP4):
    """AIOIMAP4 + AIOSMTP Email Client"""

    def __init__(self, connect_req: ConnectReq):
        self.connect_req = connect_req

    async def close(self) -> None:
        await self.impl.logout()

    async def startup(self):
        await self.connect(self.connect_req)
        return self

    async def __aenter__(self) -> Self:
        return await self.startup()

    async def __aexit__(
        self, ExceptionType: type[Exception], value: str, traceback: TracebackType
    ):
        if not isinstance(ExceptionType, NoneType):
            raise ExceptionType(value)

        await self.close()