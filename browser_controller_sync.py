"""
Browser Controller sử dụng Playwright - Sync Version
Điều khiển trình duyệt thông qua CDP connection (Synchronous)
"""
import random
import time
from typing import Optional, Dict, List, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from loguru import logger
from config import config
from adspower_api_sync import AdsPowerAPISync


class BrowserControllerSync:
    """Controller đồng bộ để điều khiển trình duyệt thông qua Playwright"""
    
    def __init__(self, adspower_api: AdsPowerAPISync):
        self.adspower_api = adspower_api
        self.playwright = None
        self.browser = None
        self.context = None
        self.pages: List[Page] = []
        self.current_user_id = None
    
    def __enter__(self):
        """Context manager entry"""
        self.start_playwright()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def start_playwright(self):
        """Khởi động Playwright"""
        try:
            self.playwright = sync_playwright().start()
            logger.info("Playwright started successfully")
        except Exception as e:
            logger.error(f"Failed to start Playwright: {e}")
            raise
    
    def connect_to_browser(self, profile_id: str, webdriver_url: str) -> Browser:
        """Kết nối đến trình duyệt AdsPower thông qua CDP (API v2)"""
        try:
            
            # Kết nối đến trình duyệt thông qua CDP
            self.browser = self.playwright.chromium.connect_over_cdp(webdriver_url)
            self.current_user_id = profile_id
            
            logger.info(f"Successfully connected to browser for profile: {profile_id}")
            return self.browser
            
        except Exception as e:
            logger.error(f"Failed to connect to browser: {e}")
            raise
    
    def create_context(self, **kwargs) -> BrowserContext:
        """Tạo browser context mới"""
        if not self.browser:
            raise Exception("Browser not connected. Call connect_to_browser() first.")
        
        try:
            # Cấu hình mặc định cho context
            context_options = {
                'viewport': {
                    'width': config.viewport_width,
                    'height': config.viewport_height
                },
                'user_agent': None,  # Sử dụng user agent từ AdsPower
                'locale': 'vi-VN',
                'timezone_id': 'Asia/Ho_Chi_Minh',
                **kwargs
            }
            
            self.context = self.browser.new_context(**context_options)
            logger.info("Browser context created successfully")
            return self.context
            
        except Exception as e:
            logger.error(f"Failed to create browser context: {e}")
            raise
    
    def new_page(self, **kwargs) -> Page:
        """Tạo trang mới"""
        if not self.context:
            self.create_context()
        
        try:
            page = self.context.new_page()
            
            # Cấu hình timeout
            page.set_default_timeout(config.page_timeout)
            page.set_default_navigation_timeout(config.navigation_timeout)
            
            self.pages.append(page)
            logger.info(f"New page created. Total pages: {len(self.pages)}")
            return page
            
        except Exception as e:
            logger.error(f"Failed to create new page: {e}")
            raise
    
    def get_page(self, index: int = 0) -> Page:
        """Lấy trang theo index"""
        if not self.pages or index >= len(self.pages):
            return self.new_page()
        return self.pages[index]
    
    def navigate_to(self, url: str, page_index: int = 0, **kwargs) -> Page:
        """Điều hướng đến URL"""
        page = self.get_page(page_index)
        
        try:
            logger.info(f"Navigating to: {url}")
            page.goto(url, **kwargs)
            logger.info(f"Successfully navigated to: {url}")
            return page
            
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise
    
    def wait_for_element(self, selector: str, page_index: int = 0, timeout: int = None) -> Any:
        """Chờ element xuất hiện"""
        page = self.get_page(page_index)
        timeout = timeout or config.page_timeout
        
        try:
            element = page.wait_for_selector(selector, timeout=timeout)
            logger.info(f"Element found: {selector}")
            return element
            
        except Exception as e:
            logger.error(f"Element not found: {selector}, timeout: {timeout}ms")
            raise
    
    def click_element(self, selector: str, page_index: int = 0, **kwargs) -> None:
        """Click vào element"""
        page = self.get_page(page_index)
        
        try:
            page.click(selector, **kwargs)
            logger.info(f"Clicked element: {selector}")
            
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            raise
    
    def fill_input(self, selector: str, text: str, page_index: int = 0, 
                   min_delay: float = 0.05, max_delay: float = 0.15, 
                   clear_first: bool = True, **kwargs) -> None:
        """
        Điền text vào input với delay giống người dùng thật
        
        Args:
            selector: CSS selector của input element
            text: Text cần điền
            page_index: Index của trang
            min_delay: Delay tối thiểu giữa các ký tự (giây)
            max_delay: Delay tối đa giữa các ký tự (giây)
            clear_first: Có xóa nội dung cũ trước khi điền không
            **kwargs: Các tham số khác cho page.type()
        """
        page = self.get_page(page_index)
        
        try:
            # Chờ element xuất hiện
            page.wait_for_selector(selector, timeout=5000)
            
            # Click vào input để focus
            page.click(selector)
            
            # Xóa nội dung cũ nếu cần
            if clear_first:
                page.keyboard.press("Control+a")  # Select all
                page.keyboard.press("Delete")     # Delete selected
                time.sleep(random.uniform(0.1, 0.3))  # Delay sau khi xóa
            
            # Điền từng ký tự với delay ngẫu nhiên
            for char in text:
                page.keyboard.type(char)
                # Delay ngẫu nhiên giữa các ký tự
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)
            
            logger.info(f"Filled input {selector} with text: {text[:20]}... (human-like typing)")
            
        except Exception as e:
            logger.error(f"Failed to fill input {selector}: {e}")
            raise
    
    def send_key_enter(self, selector: str, page_index: int = 0, **kwargs) -> None:
        """Gửi key enter vào input"""
        page = self.get_page(page_index)
        
        try:
            page.keyboard.press("Enter")
            logger.info(f"Sent key enter to {selector}")
            
        except Exception as e:
            logger.error(f"Failed to send key enter to {selector}: {e}")
            raise
    
    def get_text(self, selector: str, page_index: int = 0) -> str:
        """Lấy text từ element"""
        page = self.get_page(page_index)
        
        try:
            text = page.text_content(selector)
            logger.info(f"Got text from {selector}: {text[:50]}...")
            return text or ""
            
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {e}")
            raise
    
    def get_attribute(self, selector: str, attribute: str, page_index: int = 0) -> str:
        """Lấy attribute từ element"""
        page = self.get_page(page_index)
        
        try:
            value = page.get_attribute(selector, attribute)
            logger.info(f"Got attribute {attribute} from {selector}: {value}")
            return value or ""
            
        except Exception as e:
            logger.error(f"Failed to get attribute {attribute} from {selector}: {e}")
            raise
    
    def take_screenshot(self, path: str = None, page_index: int = 0, **kwargs) -> bytes:
        """Chụp ảnh màn hình"""
        page = self.get_page(page_index)
        
        try:
            if path:
                page.screenshot(path=path, **kwargs)
                logger.info(f"Screenshot saved to: {path}")
            else:
                screenshot = page.screenshot(**kwargs)
                logger.info("Screenshot taken")
                return screenshot
                
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    def evaluate_script(self, script: str, page_index: int = 0) -> Any:
        """Thực thi JavaScript"""
        page = self.get_page(page_index)
        
        try:
            result = page.evaluate(script)
            logger.info(f"Script executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute script: {e}")
            raise
    
    def inject_script(self, script: str, page_index: int = 0) -> None:
        """Inject JavaScript vào trang"""
        page = self.get_page(page_index)
        
        try:
            page.add_script_tag(content=script)
            logger.info("Script injected successfully")
            
        except Exception as e:
            logger.error(f"Failed to inject script: {e}")
            raise
    
    def wait_for_load_state(self, state: str = "load", page_index: int = 0) -> None:
        """Chờ trang load hoàn tất"""
        page = self.get_page(page_index)
        
        try:
            page.wait_for_load_state(state)
            logger.info(f"Page load state '{state}' completed")
            
        except Exception as e:
            logger.error(f"Failed to wait for load state '{state}': {e}")
            raise
    
    def get_cookies(self, page_index: int = 0) -> List[Dict]:
        """Lấy cookies từ trang"""
        page = self.get_page(page_index)
        
        try:
            cookies = page.context.cookies()
            logger.info(f"Retrieved {len(cookies)} cookies")
            return cookies
            
        except Exception as e:
            logger.error(f"Failed to get cookies: {e}")
            raise
    
    def set_cookies(self, cookies: List[Dict], page_index: int = 0) -> None:
        """Set cookies cho trang"""
        page = self.get_page(page_index)
        
        try:
            page.context.add_cookies(cookies)
            logger.info(f"Set {len(cookies)} cookies")
            
        except Exception as e:
            logger.error(f"Failed to set cookies: {e}")
            raise
    
    def get_local_storage(self, page_index: int = 0) -> Dict[str, str]:
        """Lấy local storage"""
        page = self.get_page(page_index)
        
        try:
            storage = page.evaluate("() => ({ ...localStorage })")
            logger.info(f"Retrieved local storage with {len(storage)} items")
            return storage
            
        except Exception as e:
            logger.error(f"Failed to get local storage: {e}")
            raise
    
    def set_local_storage(self, key: str, value: str, page_index: int = 0) -> None:
        """Set local storage item"""
        page = self.get_page(page_index)
        
        try:
            page.evaluate(f"localStorage.setItem('{key}', '{value}')")
            logger.info(f"Set local storage: {key} = {value}")
            
        except Exception as e:
            logger.error(f"Failed to set local storage: {e}")
            raise
    
    def get_session_storage(self, page_index: int = 0) -> Dict[str, str]:
        """Lấy session storage"""
        page = self.get_page(page_index)
        
        try:
            storage = page.evaluate("() => ({ ...sessionStorage })")
            logger.info(f"Retrieved session storage with {len(storage)} items")
            return storage
            
        except Exception as e:
            logger.error(f"Failed to get session storage: {e}")
            raise
    
    def set_session_storage(self, key: str, value: str, page_index: int = 0) -> None:
        """Set session storage item"""
        page = self.get_page(page_index)
        
        try:
            page.evaluate(f"sessionStorage.setItem('{key}', '{value}')")
            logger.info(f"Set session storage: {key} = {value}")
            
        except Exception as e:
            logger.error(f"Failed to set session storage: {e}")
            raise
    
    def close_page(self, page_index: int = 0) -> None:
        """Đóng trang"""
        if page_index < len(self.pages):
            try:
                self.pages[page_index].close()
                self.pages.pop(page_index)
                logger.info(f"Page {page_index} closed")
                
            except Exception as e:
                logger.error(f"Failed to close page {page_index}: {e}")
                raise
    
    def close_context(self) -> None:
        """Đóng browser context"""
        if self.context:
            try:
                self.context.close()
                self.context = None
                self.pages.clear()
                logger.info("Browser context closed")
                
            except Exception as e:
                logger.error(f"Failed to close browser context: {e}")
                raise
    
    def close_browser(self) -> None:
        """Đóng trình duyệt (API v2)"""
        if self.current_user_id:
            try:
                # Dừng trình duyệt AdsPower
                result = self.adspower_api.stop_browser(self.current_user_id)
                if result.get('code') == 0:
                    logger.info(f"Browser stopped for profile: {self.current_user_id}")
                else:
                    logger.warning(f"Failed to stop browser: {result.get('msg')}")
                
                self.current_user_id = None
                
            except Exception as e:
                logger.error(f"Failed to stop browser: {e}")
                raise
    
    def close(self) -> None:
        """Đóng tất cả kết nối"""
        try:
            # self.close_context()
            self.close_browser()
            
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
                logger.info("Playwright stopped")
                
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            raise
    
    def get_page_info(self, page_index: int = 0) -> Dict:
        """Lấy thông tin trang"""
        page = self.get_page(page_index)
        
        try:
            info = {
                'url': page.url,
                'title': page.title(),
                'viewport': page.viewport_size,
                'user_agent': page.evaluate('navigator.userAgent'),
                'cookies_count': len(self.get_cookies(page_index)),
                'local_storage_count': len(self.get_local_storage(page_index)),
                'session_storage_count': len(self.get_session_storage(page_index))
            }
            
            logger.info(f"Page info retrieved for page {page_index}")
            return info
            
        except Exception as e:
            logger.error(f"Failed to get page info: {e}")
            raise
    
    def wait_for_network_idle(self, page_index: int = 0, timeout: int = None) -> None:
        """Chờ network idle"""
        page = self.get_page(page_index)
        timeout = timeout or config.navigation_timeout
        
        try:
            page.wait_for_load_state("networkidle", timeout=timeout)
            logger.info("Network idle state reached")
            
        except Exception as e:
            logger.error(f"Failed to wait for network idle: {e}")
            raise
    
    def scroll_to_element(self, selector: str, page_index: int = 0) -> None:
        """Scroll đến element"""
        page = self.get_page(page_index)
        
        try:
            page.locator(selector).scroll_into_view_if_needed()
            logger.info(f"Scrolled to element: {selector}")
            
        except Exception as e:
            logger.error(f"Failed to scroll to element {selector}: {e}")
            raise
    
    def hover_element(self, selector: str, page_index: int = 0) -> None:
        """Hover vào element"""
        page = self.get_page(page_index)
        
        try:
            page.hover(selector)
            logger.info(f"Hovered over element: {selector}")
            
        except Exception as e:
            logger.error(f"Failed to hover over element {selector}: {e}")
            raise
    
    def select_option(self, selector: str, value: str, page_index: int = 0) -> None:
        """Chọn option trong select"""
        page = self.get_page(page_index)
        
        try:
            page.select_option(selector, value)
            logger.info(f"Selected option {value} in {selector}")
            
        except Exception as e:
            logger.error(f"Failed to select option {value} in {selector}: {e}")
            raise
    
    def upload_file(self, selector: str, file_path: str, page_index: int = 0) -> None:
        """Upload file"""
        page = self.get_page(page_index)
        
        try:
            page.set_input_files(selector, file_path)
            logger.info(f"Uploaded file {file_path} to {selector}")
            
        except Exception as e:
            logger.error(f"Failed to upload file {file_path} to {selector}: {e}")
            raise
    
    def download_file(self, url: str, download_path: str, page_index: int = 0) -> None:
        """Download file"""
        page = self.get_page(page_index)
        
        try:
            with page.expect_download() as download_info:
                page.goto(url)
            download = download_info.value
            download.save_as(download_path)
            logger.info(f"Downloaded file to {download_path}")
            
        except Exception as e:
            logger.error(f"Failed to download file from {url}: {e}")
            raise
