from loguru import logger
from playwright.async_api import Page, expect

from src.exceptions import LoginError, NavigationError


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    async def navigate(self):
        try:
            await self.page.goto(f"{self.base_url}/login")
            await self.page.wait_for_selector('input[name="email"]')
        except Exception as e:
            raise NavigationError(f"Failed to navigate to login page: {e}") from e

    async def login(self, username: str, password: str):
        try:
            await self.page.locator('input[name="email"]').fill(username)
            await self.page.locator('input[name="password"]').fill(password)
            await self.page.locator('input[value="log in"]').click()

            await expect(self.page).to_have_url(f"{self.base_url}/home", timeout=10000)
            logger.info("Successfully logged in and redirected to home page")
        except Exception as e:
            raise LoginError(f"Failed to login: {e}") from e
