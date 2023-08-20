"""Email(IMAP4 + SMTP) 驱动适配"""

from typing import Type, AsyncGenerator
from contextlib import asynccontextmanager

from nonebot.drivers.none import Driver as NoneDriver
from nonebot.drivers import (
    combine_driver,
)

from .model.aioimap4 import AIOIMAP4, ConnectReq
from .model.aiosmtp import AIOSMTP

class Email(AIOSMTP, AIOIMAP4):

    async def close(self) -> None:
        await self.impl.logout()
        await self.impl.close()


class Mixin:
    """Email(IMAP4 + SMTP) Mixin"""

    @property
    def type(self) -> str:
        return "email"

    @asynccontextmanager
    async def email(self, connect_req: ConnectReq) -> AsyncGenerator[Email, None]:
        email = Email()
        await email.connect(connect_req)
        yield email
        await email.close()


Driver: Type[NoneDriver] = combine_driver(NoneDriver, Mixin)  # type: ignore
"""Email(IMAP4 + SMTP) 驱动"""
