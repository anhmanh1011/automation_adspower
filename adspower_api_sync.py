"""
AdsPower Local API Client - Sync Version
Tương tác với AdsPower thông qua Local API (Synchronous)
"""
import requests
import json
import time
from typing import Dict, List, Optional, Any
from loguru import logger
from config import config


class AdsPowerAPISync:
    """Client đồng bộ để tương tác với AdsPower Local API"""
    
    def __init__(self, api_url: str = None, api_key: str = None):
        self.api_url = api_url or config.adspower_api_url
        self.api_key = api_key or config.adspower_api_key
        self.session = requests.Session()
        
        # Thêm headers mặc định
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AdsPower-Automation-Sync/1.0'
        })
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Thực hiện HTTP request đến AdsPower API"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=data)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def get_profile_list(self, page: int = 1, page_size: int = 100) -> Dict:
        """Lấy danh sách profiles"""
        endpoint = "/api/v1/user/list"
        data = {
            "page": page,
            "page_size": page_size
        }
        return self._make_request('GET', endpoint, data)
    
    def get_profile_detail(self, user_id: str) -> Dict:
        """Lấy thông tin chi tiết của profile"""
        endpoint = f"/api/v1/user/detail"
        data = {"user_id": user_id}
        return self._make_request('GET', endpoint, data)
    
    def start_browser(self, profile_id: str, headless: bool = None, 
                     last_opened_tabs: bool = True, proxy_detection: bool = True,
                     password_filling: bool = False, password_saving: bool = False,
                     cdp_mask: bool = True, delete_cache: bool = False,
                     device_scale: float = None, launch_args: List[str] = None) -> Dict:
        """Khởi động trình duyệt cho profile (API v2)"""
        endpoint = "/api/v2/browser-profile/start"
        data = {
            "profile_id": profile_id,
            "headless": 1 if headless else 0,
            "last_opened_tabs": 1 if last_opened_tabs else 0,
            "proxy_detection": 1 if proxy_detection else 0,
            "password_filling": 1 if password_filling else 0,
            "password_saving": 1 if password_saving else 0,
            "cdp_mask": 1 if cdp_mask else 0,
            "delete_cache": 1 if delete_cache else 0
        }
        
        # Thêm các tham số tùy chọn
        if device_scale is not None:
            data["device_scale"] = str(device_scale)
        
        if launch_args is not None:
            data["launch_args"] = launch_args
            
        return self._make_request('POST', endpoint, data)
    
    def stop_browser(self, profile_id: str) -> Dict:
        """Dừng trình duyệt của profile (API v2)"""
        endpoint = "/api/v2/browser-profile/stop"
        data = {"profile_id": profile_id}
        return self._make_request('POST', endpoint, data)
    
    def get_browser_status(self, profile_id: str) -> Dict:
        """Kiểm tra trạng thái trình duyệt (API v2)"""
        endpoint = "/api/v2/browser-profile/active"
        data = {"profile_id": profile_id}
        return self._make_request('GET', endpoint, data)
    
    def get_browser_list(self) -> Dict:
        """Lấy danh sách các trình duyệt đang chạy"""
        endpoint = "/api/v1/browser/list"
        return self._make_request('GET', endpoint)
    
    def create_profile(self, profile_data: Dict) -> Dict:
        """Tạo profile mới"""
        endpoint = "/api/v1/user/create"
        return self._make_request('POST', endpoint, profile_data)
    
    def update_profile(self, user_id: str, profile_data: Dict) -> Dict:
        """Cập nhật profile"""
        endpoint = "/api/v1/user/update"
        data = {"user_id": user_id, **profile_data}
        return self._make_request('POST', endpoint, data)
    
    def delete_profile(self, user_id: str) -> Dict:
        """Xóa profile"""
        endpoint = "/api/v1/user/delete"
        data = {"user_id": user_id}
        return self._make_request('POST', endpoint, data)
    
    def get_proxy_list(self) -> Dict:
        """Lấy danh sách proxy"""
        endpoint = "/api/v1/proxy/list"
        return self._make_request('GET', endpoint)
    
    def test_proxy(self, proxy_data: Dict) -> Dict:
        """Test proxy"""
        endpoint = "/api/v1/proxy/test"
        return self._make_request('POST', endpoint, proxy_data)
    
    def get_fingerprint_config(self, user_id: str) -> Dict:
        """Lấy cấu hình fingerprint của profile"""
        endpoint = "/api/v1/user/fingerprint"
        data = {"user_id": user_id}
        return self._make_request('GET', endpoint, data)
    
    def update_fingerprint_config(self, user_id: str, fingerprint_data: Dict) -> Dict:
        """Cập nhật cấu hình fingerprint"""
        endpoint = "/api/v1/user/fingerprint/update"
        data = {"user_id": user_id, **fingerprint_data}
        return self._make_request('POST', endpoint, data)
    
    def get_extension_list(self, user_id: str) -> Dict:
        """Lấy danh sách extension của profile"""
        endpoint = "/api/v1/user/extensions"
        data = {"user_id": user_id}
        return self._make_request('GET', endpoint, data)
    
    def install_extension(self, user_id: str, extension_id: str) -> Dict:
        """Cài đặt extension cho profile"""
        endpoint = "/api/v1/user/extension/install"
        data = {"user_id": user_id, "extension_id": extension_id}
        return self._make_request('POST', endpoint, data)
    
    def uninstall_extension(self, user_id: str, extension_id: str) -> Dict:
        """Gỡ cài đặt extension"""
        endpoint = "/api/v1/user/extension/uninstall"
        data = {"user_id": user_id, "extension_id": extension_id}
        return self._make_request('POST', endpoint, data)
    
    def get_cookies(self, user_id: str, domain: str = None) -> Dict:
        """Lấy cookies của profile"""
        endpoint = "/api/v1/user/cookies"
        data = {"user_id": user_id}
        if domain:
            data["domain"] = domain
        return self._make_request('GET', endpoint, data)
    
    def update_cookies(self, user_id: str, cookies: List[Dict], domain: str = None) -> Dict:
        """Cập nhật cookies cho profile"""
        endpoint = "/api/v1/user/cookies/update"
        data = {
            "user_id": user_id,
            "cookies": cookies
        }
        if domain:
            data["domain"] = domain
        return self._make_request('POST', endpoint, data)
    
    def clear_cookies(self, user_id: str, domain: str = None) -> Dict:
        """Xóa cookies của profile"""
        endpoint = "/api/v1/user/cookies/clear"
        data = {"user_id": user_id}
        if domain:
            data["domain"] = domain
        return self._make_request('POST', endpoint, data)
    
    def get_local_storage(self, user_id: str, domain: str = None) -> Dict:
        """Lấy local storage của profile"""
        endpoint = "/api/v1/user/local_storage"
        data = {"user_id": user_id}
        if domain:
            data["domain"] = domain
        return self._make_request('GET', endpoint, data)
    
    def update_local_storage(self, user_id: str, storage_data: Dict, domain: str = None) -> Dict:
        """Cập nhật local storage"""
        endpoint = "/api/v1/user/local_storage/update"
        data = {
            "user_id": user_id,
            "storage": storage_data
        }
        if domain:
            data["domain"] = domain
        return self._make_request('POST', endpoint, data)
    
    def clear_local_storage(self, user_id: str, domain: str = None) -> Dict:
        """Xóa local storage"""
        endpoint = "/api/v1/user/local_storage/clear"
        data = {"user_id": user_id}
        if domain:
            data["domain"] = domain
        return self._make_request('POST', endpoint, data)
    
    def get_session_storage(self, user_id: str, domain: str = None) -> Dict:
        """Lấy session storage của profile"""
        endpoint = "/api/v1/user/session_storage"
        data = {"user_id": user_id}
        if domain:
            data["domain"] = domain
        return self._make_request('GET', endpoint, data)
    
    def update_session_storage(self, user_id: str, storage_data: Dict, domain: str = None) -> Dict:
        """Cập nhật session storage"""
        endpoint = "/api/v1/user/session_storage/update"
        data = {
            "user_id": user_id,
            "storage": storage_data
        }
        if domain:
            data["domain"] = domain
        return self._make_request('POST', endpoint, data)
    
    def clear_session_storage(self, user_id: str, domain: str = None) -> Dict:
        """Xóa session storage"""
        endpoint = "/api/v1/user/session_storage/clear"
        data = {"user_id": user_id}
        if domain:
            data["domain"] = domain
        return self._make_request('POST', endpoint, data)
    
    def get_webdriver_url(self, profile_id: str) -> str:
        """Lấy WebDriver URL để kết nối với Playwright (API v2)"""
        try:
            status = self.get_browser_status(profile_id)
            if status.get('code') == 0 and status.get('data', {}).get('status') == 'Active':
                return status['data']['ws']['puppeteer']
            else:
                raise Exception(f"Browser not active for profile {profile_id}")
        except Exception as e:
            logger.error(f"Failed to get webdriver URL: {e}")
            raise
    
    def get_selenium_url(self, profile_id: str) -> str:
        """Lấy Selenium URL để kết nối với Selenium (API v2)"""
        try:
            status = self.get_browser_status(profile_id)
            if status.get('code') == 0 and status.get('data', {}).get('status') == 'Active':
                return status['data']['ws']['selenium']
            else:
                raise Exception(f"Browser not active for profile {profile_id}")
        except Exception as e:
            logger.error(f"Failed to get selenium URL: {e}")
            raise
    
    def get_webdriver_path(self, profile_id: str) -> str:
        """Lấy đường dẫn WebDriver (API v2)"""
        try:
            status = self.get_browser_status(profile_id)
            if status.get('code') == 0 and status.get('data', {}).get('status') == 'Active':
                return status['data']['webdriver']
            else:
                raise Exception(f"Browser not active for profile {profile_id}")
        except Exception as e:
            logger.error(f"Failed to get webdriver path: {e}")
            raise
    
    def wait_for_browser_ready(self, profile_id: str, timeout: int = 30) -> bool:
        """Chờ trình duyệt sẵn sàng (API v2)"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                status = self.get_browser_status(profile_id)
                if status.get('code') == 0 and status.get('data', {}).get('status') == 'Active':
                    return True
            except:
                pass
            time.sleep(1)
        return False
    
    def close(self):
        """Đóng session"""
        if self.session:
            self.session.close()
            logger.info("API session closed")
