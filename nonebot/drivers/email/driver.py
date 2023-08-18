"""Email(IMAP4 + SMTP) 驱动适配"""

from typing_extensions import override
from typing import Type, AsyncGenerator
from contextlib import asynccontextmanager

from nonebot.drivers.none import Driver as NoneDriver
from nonebot.drivers import (
    combine_driver,
)

from aiosmtplib import send
from aioimaplib import IMAP4


