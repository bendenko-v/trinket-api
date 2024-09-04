import re
from urllib.parse import urlparse

from loguru import logger
from playwright.async_api import Page, expect

from src.exceptions import NavigationError, TrinketCreationError, TrinketVerificationError


class CreateTrinketPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.trinkets_list_url = f"{base_url}/library/trinkets"

    def get_trinket_id(self):
        current_url = self.page.url
        parsed_url = urlparse(current_url)
        path_parts = parsed_url.path.split("/")
        return path_parts[-1]

    async def navigate(self):
        try:
            await self.page.goto(f"{self.trinkets_list_url}/create?lang=python3")
            await self.page.wait_for_selector("#embed-code iframe", state="visible", timeout=15000)
            logger.info("Trinket editor successfully loaded")
        except Exception as e:
            raise NavigationError(f"Failed to navigate to trinket creation page: {e}") from e

    async def create_trinket(self, title: str, code: str) -> str:
        try:
            # Wait for trinket editor
            iframe = self.page.frame_locator("#embed-code iframe")
            editor = iframe.locator(".ace_editor")
            await editor.wait_for(state="visible", timeout=5000)

            textarea = iframe.locator(".ace_text-input")
            await textarea.wait_for(state="visible", timeout=5000)
            await textarea.fill(code)

            # Create trinket title
            title_span = self.page.locator('span[editable-text="trinket.name"]')
            await expect(title_span).to_be_visible(timeout=5000)
            await title_span.click()

            title_input = self.page.locator("input.editable-input")
            await expect(title_input).to_be_visible(timeout=5000)
            await title_input.fill(title[:50])
            await self.page.keyboard.press("Enter")

            # Save trinket
            save_button = self.page.locator('a[ng-click="save()"]')
            await expect(save_button).to_be_visible(timeout=5000)
            await save_button.click()

            await self.page.wait_for_url(re.compile(f"{self.trinkets_list_url}/[a-zA-Z0-9]+$"), timeout=15000)

            trinket_id = self.get_trinket_id()

            logger.info(f"Trinket created successfully, ID: {trinket_id}")
            return trinket_id
        except Exception as e:
            raise TrinketCreationError(f"Failed to create trinket: {e}") from e

    async def check_create_success(self, trinket_id: str) -> tuple:
        try:
            await self.page.goto(f"{self.trinkets_list_url}/{trinket_id}")

            iframe = self.page.frame_locator("#embed-code iframe")
            editor = iframe.locator(".ace_editor")
            await editor.wait_for(state="visible", timeout=5000)

            textarea = iframe.locator("div.ace_content")
            await textarea.wait_for(state="visible", timeout=5000)

            code = await textarea.inner_text()

            logger.info(f"Trinket id {trinket_id} creation verified")
            return trinket_id, code
        except Exception as e:
            raise TrinketVerificationError(f"Failed to verify trinket {trinket_id} creation: {e}") from e
