import pytest


@pytest.mark.asyncio
async def test_load_in_nonebot():
    import nonebot

    nonebot.init(driver="nonemail.driver")

    driver = nonebot.get_driver()
    assert driver.type == "none+email"


