from playwright.async_api import async_playwright

from src.config import settings
from src.exceptions import (
    LoginError,
    NavigationError,
    TrinketCreationError,
    TrinketUpdateError,
    TrinketVerificationError,
)
from src.services.trinket_create import CreateTrinketPage
from src.services.trinket_login import LoginPage
from src.services.trinket_update import UpdateTrinketPage


class TrinketClient:
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        self.base_url = settings.TRINKET_BASE_URL
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def login(self, username: str, password: str):
        try:
            login_page = LoginPage(self.page, self.base_url)
            await login_page.navigate()
            await login_page.login(username, password)
        except (LoginError, NavigationError):
            raise
        except Exception as e:
            raise LoginError(f"Unexpected error during login: {e}") from e

    async def create_trinket(self, title: str, code: str) -> tuple[str, str]:
        try:
            create_page = CreateTrinketPage(self.page, self.base_url)
            await create_page.navigate()
            trinket_id = await create_page.create_trinket(title, code)
            trinket_id, code = await create_page.check_create_success(trinket_id)
            return trinket_id, code
        except (NavigationError, TrinketCreationError, TrinketVerificationError):
            raise
        except Exception as e:
            raise TrinketCreationError(f"Unexpected error during trinket creation: {e}") from e

    async def update_trinket(self, trinket_id: str, title: str, new_code: str) -> str:
        try:
            update_page = UpdateTrinketPage(self.page, self.base_url)
            await update_page.navigate(trinket_id)
            await update_page.update_trinket(trinket_id, title, new_code)
            return await update_page.check_update_success(trinket_id, new_code)
        except (NavigationError, TrinketUpdateError, TrinketVerificationError):
            raise
        except Exception as e:
            raise TrinketUpdateError(f"Failed to update trinket: {e}") from e
