"""
Utilities và helper functions cho AdsPower Automation
"""
import json
import time
import random
from typing import Dict, List, Any, Optional
from loguru import logger


class AdsPowerUtils:
    """Class chứa các utility functions"""
    
    @staticmethod
    def generate_random_user_agent() -> str:
        """Tạo user agent ngẫu nhiên"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(user_agents)
    
    @staticmethod
    def generate_random_viewport() -> Dict[str, int]:
        """Tạo viewport ngẫu nhiên"""
        viewports = [
            {"width": 1920, "height": 1080},
            {"width": 1366, "height": 768},
            {"width": 1536, "height": 864},
            {"width": 1440, "height": 900},
            {"width": 1280, "height": 720}
        ]
        return random.choice(viewports)
    
    @staticmethod
    def generate_random_timezone() -> str:
        """Tạo timezone ngẫu nhiên"""
        timezones = [
            "America/New_York",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Australia/Sydney"
        ]
        return random.choice(timezones)
    
    @staticmethod
    def generate_random_language() -> List[str]:
        """Tạo danh sách ngôn ngữ ngẫu nhiên"""
        languages = [
            ["en-US", "en"],
            ["en-GB", "en"],
            ["fr-FR", "fr"],
            ["de-DE", "de"],
            ["es-ES", "es"],
            ["ja-JP", "ja"],
            ["zh-CN", "zh"]
        ]
        return random.choice(languages)
    
    @staticmethod
    def create_random_profile_data(name_prefix: str = "AutoProfile") -> Dict[str, Any]:
        """Tạo dữ liệu profile ngẫu nhiên"""
        return {
            "name": f"{name_prefix}_{int(time.time())}",
            "group_id": "0",
            "domain": "facebook.com",
            "user_agent": AdsPowerUtils.generate_random_user_agent(),
            "webrtc": "altered",
            "location": "us",
            "language": AdsPowerUtils.generate_random_language(),
            "timezone": AdsPowerUtils.generate_random_timezone(),
            "geolocation": {
                "mode": "prompt",
                "fillBasedOnIp": True
            },
            "webgl": "noise",
            "canvas": "noise",
            "webgl_metadata": {
                "mode": "mask",
                "vendor": "Google Inc. (Intel)",
                "renderer": "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)"
            },
            "audio": "noise",
            "fonts": ["Arial", "Verdana", "Times New Roman"],
            "screen": {
                "resolution": f"{AdsPowerUtils.generate_random_viewport()['width']}x{AdsPowerUtils.generate_random_viewport()['height']}",
                "colorDepth": 24
            },
            "mediaDevices": {
                "videoInputs": 1,
                "audioInputs": 1,
                "audioOutputs": 1
            },
            "cpu": {
                "mode": "noise",
                "cores": random.choice([2, 4, 6, 8])
            },
            "memory": {
                "mode": "noise",
                "deviceMemory": random.choice([4, 8, 16, 32])
            }
        }
    
    @staticmethod
    def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
        """Tạo delay ngẫu nhiên giữa các thao tác"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        logger.debug(f"Random delay: {delay:.2f} seconds")
    
    @staticmethod
    def human_like_typing_delay() -> float:
        """Tạo delay giống như người thật khi gõ"""
        return random.uniform(0.05, 0.2)
    
    @staticmethod
    def save_data_to_json(data: Any, filename: str) -> None:
        """Lưu dữ liệu vào file JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save data to {filename}: {e}")
            raise
    
    @staticmethod
    def load_data_from_json(filename: str) -> Any:
        """Đọc dữ liệu từ file JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Data loaded from {filename}")
            return data
        except Exception as e:
            logger.error(f"Failed to load data from {filename}: {e}")
            raise
    
    @staticmethod
    def validate_profile_data(profile_data: Dict[str, Any]) -> bool:
        """Kiểm tra tính hợp lệ của dữ liệu profile"""
        required_fields = ['name', 'user_agent', 'language', 'timezone']
        
        for field in required_fields:
            if field not in profile_data:
                logger.error(f"Missing required field: {field}")
                return False
        
        # Kiểm tra user agent
        if not isinstance(profile_data['user_agent'], str) or len(profile_data['user_agent']) < 50:
            logger.error("Invalid user agent")
            return False
        
        # Kiểm tra language
        if not isinstance(profile_data['language'], list) or len(profile_data['language']) < 1:
            logger.error("Invalid language format")
            return False
        
        # Kiểm tra timezone
        if not isinstance(profile_data['timezone'], str) or '/' not in profile_data['timezone']:
            logger.error("Invalid timezone format")
            return False
        
        logger.info("Profile data validation passed")
        return True
    
    @staticmethod
    def extract_domain_from_url(url: str) -> str:
        """Trích xuất domain từ URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except Exception as e:
            logger.error(f"Failed to extract domain from {url}: {e}")
            return ""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Làm sạch text (loại bỏ ký tự đặc biệt, khoảng trắng thừa)"""
        if not text:
            return ""
        
        # Loại bỏ khoảng trắng thừa
        text = ' '.join(text.split())
        
        # Loại bỏ ký tự đặc biệt không cần thiết
        import re
        text = re.sub(r'[^\w\s\-.,!?@#$%&*()+=:;"\'<>/\\]', '', text)
        
        return text.strip()
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format kích thước file thành dạng dễ đọc"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    @staticmethod
    def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
        """Decorator để retry khi function thất bại"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_retries - 1:
                            logger.error(f"Function {func.__name__} failed after {max_retries} attempts: {e}")
                            raise
                        else:
                            logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                            time.sleep(delay)
            return wrapper
        return decorator
    
    @staticmethod
    def async_retry_on_failure(max_retries: int = 3, delay: float = 1.0):
        """Decorator async để retry khi function thất bại"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                import asyncio
                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_retries - 1:
                            logger.error(f"Async function {func.__name__} failed after {max_retries} attempts: {e}")
                            raise
                        else:
                            logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                            await asyncio.sleep(delay)
            return wrapper
        return decorator


class SelectorHelper:
    """Helper class cho CSS selectors"""
    
    # Common selectors
    LOGIN_FORM = "form[action*='login'], form[action*='signin']"
    USERNAME_INPUT = "input[name='username'], input[name='email'], input[type='email'], input[id*='username'], input[id*='email']"
    PASSWORD_INPUT = "input[name='password'], input[type='password'], input[id*='password']"
    LOGIN_BUTTON = "button[type='submit'], input[type='submit'], button:contains('Login'), button:contains('Sign in')"
    SEARCH_INPUT = "input[name='q'], input[name='search'], input[type='search'], input[placeholder*='search']"
    SEARCH_BUTTON = "button[type='submit'], input[type='submit'], button:contains('Search')"
    
    @staticmethod
    def get_selector_by_text(text: str, tag: str = "*") -> str:
        """Tạo selector để tìm element theo text"""
        return f"{tag}:contains('{text}')"
    
    @staticmethod
    def get_selector_by_attribute(attribute: str, value: str, tag: str = "*") -> str:
        """Tạo selector để tìm element theo attribute"""
        return f"{tag}[{attribute}='{value}']"
    
    @staticmethod
    def get_selector_by_partial_attribute(attribute: str, value: str, tag: str = "*") -> str:
        """Tạo selector để tìm element theo partial attribute"""
        return f"{tag}[{attribute}*='{value}']"


class DataExtractor:
    """Class để trích xuất dữ liệu từ trang web"""
    
    @staticmethod
    def extract_links(page_content: str) -> List[str]:
        """Trích xuất tất cả links từ HTML content"""
        import re
        link_pattern = r'href=["\']([^"\']+)["\']'
        links = re.findall(link_pattern, page_content)
        return list(set(links))  # Loại bỏ duplicate
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Trích xuất email addresses từ text"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """Trích xuất số điện thoại từ text"""
        import re
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        return [''.join(phone) for phone in phones]
    
    @staticmethod
    def extract_prices(text: str) -> List[str]:
        """Trích xuất giá tiền từ text"""
        import re
        price_pattern = r'\$[\d,]+\.?\d*|\d+\.?\d*\s*(?:USD|EUR|GBP|VND)'
        prices = re.findall(price_pattern, text)
        return prices
