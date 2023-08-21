import pytest
from nonemail import EmailClient, ConnectReq

@pytest.mark.asyncio
async def test_mail_client():


    connect_req = ConnectReq(
        server="imap.qq.com",
        port=993,
        username="xxx@qq.com",
        password="xxx",
    )

    async with EmailClient(connect_req) as client:
        res = await client.impl.select("INBOX")
        assert res.result == "OK"
