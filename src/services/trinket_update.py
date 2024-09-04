from loguru import logger
from playwright.async_api import Page, expect

from src.exceptions import NavigationError, TrinketUpdateError, TrinketVerificationError


class UpdateTrinketPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.trinkets_list_url = f"{base_url}/library/trinkets"

    async def navigate(self, trinket_id: str) -> None:
        try:
            await self.page.goto(f"{self.trinkets_list_url}/{trinket_id}")
            logger.info(f"Navigated to trinket {trinket_id} page")
        except Exception as e:
            raise NavigationError(f"Failed to navigate to trinket {trinket_id} page: {e}") from e

    async def update_trinket(self, trinket_id: str, title: str, new_code: str) -> None:
        try:
            iframe = self.page.frame_locator("#embed-code iframe")
            editor = iframe.locator(".ace_editor")
            await editor.wait_for(state="visible", timeout=5000)

            textarea = iframe.locator(".ace_text-input")
            await textarea.wait_for(state="visible", timeout=5000)
            await textarea.clear()
            await textarea.fill(new_code)

            # Update trinket title if changed
            title_span = self.page.locator('span[editable-text="trinket.name"]')
            await expect(title_span).to_be_visible(timeout=5000)
            current_title = await title_span.inner_text()
            if current_title != title:
                logger.info(f"Updating trinket {trinket_id} title from '{current_title}' to '{title}'")
                await title_span.click()

                title_input = self.page.locator("input.editable-input")
                await expect(title_input).to_be_visible(timeout=5000)
                await title_input.fill(title[:50])
                await self.page.keyboard.press("Enter")

            save_button = self.page.locator('a[ng-click="save()"]').first
            await expect(save_button).to_be_visible(timeout=10000)
            await save_button.click()

            logger.info(f"Trinket {trinket_id} successfully updated")
        except Exception as e:
            raise TrinketUpdateError(f"Failed to update trinket {trinket_id}: {e}") from e

    async def check_update_success(self, trinket_id: str, new_code: str) -> str:
        try:
            await self.navigate(trinket_id)

            iframe = self.page.frame_locator("#embed-code iframe")
            editor = iframe.locator(".ace_editor")
            await editor.wait_for(state="visible", timeout=5000)

            textarea = iframe.locator("div.ace_content")
            await textarea.wait_for(state="visible", timeout=5000)

            updated_code = await textarea.inner_text()

            if updated_code.replace("\n", "") != new_code.replace("\n", ""):
                raise TrinketVerificationError(f"Failed to verify trinket {trinket_id} code update! Codes do not match")

            logger.info(f"Trinket {trinket_id} update verified")
            return new_code
        except TrinketVerificationError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            raise TrinketVerificationError(f"Failed to verify trinket {trinket_id} update: {e}") from e
