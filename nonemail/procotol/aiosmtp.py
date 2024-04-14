from aiosmtplib import send

from .ability import SendAbility
from email.message import EmailMessage
from .mailing import Domain, Request as BaseRequest


class SendReq(BaseRequest):
    """Email发送请求类"""

    def __init__(
        self,
        server: Domain,
        port: int | None = None,
        *,
        message: EmailMessage,
        password: str,
        use_tls: bool = True,
        **kwargs,
    ):
        self.server = server
        self.port = port
        self.message = message
        self.password = password
        self.use_tls = use_tls
        self.kwargs = kwargs

    def __repr__(self) -> str:
        # fmt: off
        return (
            f"<EmailRequest {self.server}:{self.port}>"
            "\n"
            f"{self.message.as_string()}"
            "\n"
            "</EmailRequest>"
        )
        # fmt: on


class AIOSMTP(SendAbility):
    """SMTP协议异步实现"""

    @property
    def sub_procotol(self) -> str:
        return "AIOSMTP"

    async def send(self, request: SendReq) -> None:
        await send(
            message=request.message,
            sender=request.kwargs.get("sender", None),
            recipients=request.kwargs.get("recipients", None),
            hostname=request.server,
            port=request.port,
            username=request.kwargs.pop("username", None)
            or request.message["From"].split("@")[0],
            password=request.password,
            use_tls=request.use_tls,
            **request.kwargs,
        )
