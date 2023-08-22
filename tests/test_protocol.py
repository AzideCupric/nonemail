import datetime
import pytest


@pytest.mark.skip(reason="隐私问题")
@pytest.mark.asyncio
async def test_aipimap4():
    from json import dumps
    from email import parser
    from fast_mail_parser import parse_email
    from asyncio import get_running_loop
    from nonemail import AIOIMAP4, ConnectReq
    loop = get_running_loop()
    connect_req = ConnectReq(
        server="imap.qq.com",
        port=993,
        username="xxx",
        password="xxx",
        loop=loop
    )
    imap = AIOIMAP4()
    client = await imap.connect(connect_req)

    await client.impl.enable("UTF8=ACCEPT")
    res = await client.impl.select("INBOX")
    print(res)

    # email = await client.impl.fetch("1", "BODY[HEADER]")
    # parser = parser.BytesParser()
    # raw_email = parser.parsebytes(email.lines[1])
    # await client.impl.logout()
    # parsed_eml = parse_email(raw_email.as_string())

    # print(dumps(parsed_eml.headers, indent=4, ensure_ascii=False))
    # print(parsed_eml.text_plain)

    email = await client.impl.uid("1", "RFC822")
    parser = parser.BytesParser()
    raw_email = parser.parsebytes(email.lines[1])
    await client.impl.logout()

    def json_serial(obj):
        if isinstance(obj, bytes):
            serial = obj.decode(encoding="utf-8")
            return serial

    parsed_eml = parse_email(raw_email.as_string())
    eml_dict = {}
    eml_dict["subject"] = parsed_eml.subject
    eml_dict["date"] = parsed_eml.date
    eml_dict["text/plain"] = parsed_eml.text_plain
    eml_dict["text/html"] = parsed_eml.text_html
    eml_dict["headers"] = parsed_eml.headers

    eml_dict["attachments"] = []
    for attachment in parsed_eml.attachments:
        att = {}
        att["mimetype"] = attachment.mimetype
        att["filename"] = attachment.filename
        att["content"] = attachment.content
        eml_dict["attachments"].append(att)

    with open("./test.json", "w", encoding="utf-8") as f:
        f.write(dumps(eml_dict, indent=4, ensure_ascii=False, default=json_serial))


# @pytest.mark.skip(reason="隐私问题")
@pytest.mark.asyncio
async def test_aiostmp():
    from nonemail import AIOSMTP, SendReq
    from email.message import EmailMessage

    email = EmailMessage()
    email["From"] = "xxx@qq.com"
    email["To"] = "xxx@qq.com"
    email["Subject"] = "测试邮件"
    email.set_content("测试邮件")
    email["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

    sender = AIOSMTP()
    connect_req = SendReq(
        server="smtp.qq.com",
        port=465,
        message=email,
        password="xxx",
    )
    await sender.send(connect_req)

