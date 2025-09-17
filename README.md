# AdsPower Automation - Sync API

Dự án Python để tự động hóa trình duyệt AdsPower thông qua Local API và điều khiển bằng Playwright (connect_over_cdp) - **Sync API Version**.

## Tính năng

- ✅ Tương tác với AdsPower Local API (Sync)
- ✅ Điều khiển trình duyệt thông qua Playwright CDP (Sync)
- ✅ Quản lý profiles, cookies, local storage
- ✅ Tự động hóa web với nhiều tab
- ✅ Trích xuất dữ liệu từ trang web
- ✅ Quản lý fingerprint và proxy
- ✅ Logging chi tiết với Loguru
- ✅ Cấu hình linh hoạt với Pydantic
- ✅ Đơn giản, không cần async/await
- ✅ **GoDaddy Automation**: Tự động hóa mua domain

## Yêu cầu hệ thống

- Python 3.10+
- AdsPower đã cài đặt và chạy
- Local API của AdsPower đang hoạt động (mặc định: http://127.0.0.1:50325)

## Cài đặt

1. **Clone repository:**
```bash
git clone <repository-url>
cd adspower-automation
```

2. **Tạo virtual environment:**
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Cài đặt Playwright browsers:**
```bash
playwright install chromium
```

## ⚠️ Lỗi thường gặp

### Lỗi Pydantic BaseSettings
Nếu gặp lỗi:
```
pydantic.errors.PydanticImportError: `BaseSettings` has been moved to the `pydantic-settings` package.
```

**Cách khắc phục:**
```bash
pip install pydantic-settings==2.1.0
```

## Cấu hình

### 1. File .env (tùy chọn)
Tạo file `.env` trong thư mục gốc để cấu hình:

```env
ADSPOWER_API_URL=http://127.0.0.1:50325
ADSPOWER_API_KEY=your_api_key_here
BROWSER_TIMEOUT=30000
PAGE_TIMEOUT=30000
NAVIGATION_TIMEOUT=60000
LOG_LEVEL=INFO
LOG_FILE=adspower_automation.log
HEADLESS=false
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
```

### 2. Cấu hình trong code
Bạn có thể cấu hình trực tiếp trong file `config.py`:

```python
from config import config

# Thay đổi cấu hình
config.adspower_api_url = "http://127.0.0.1:50325"
config.headless = True
config.viewport_width = 1366
config.viewport_height = 768
```

## Sử dụng

### 1. Ví dụ cơ bản

```python
from adspower_api_sync import AdsPowerAPISync
from browser_controller_sync import BrowserControllerSync

# Khởi tạo API
api = AdsPowerAPISync()

try:
    # Lấy danh sách profiles
    profiles = api.get_profile_list()
    profile_id = profiles['data']['list'][0]['user_id']
    
    # Kết nối đến trình duyệt với API v2
    with BrowserControllerSync(api) as browser:
        browser.connect_to_browser(
            profile_id=profile_id,
            headless=False,
            last_opened_tabs=True,
            proxy_detection=True,
            cdp_mask=True
        )
        
        # Điều hướng đến trang
        browser.navigate_to("https://www.google.com")
        
        # Chụp ảnh màn hình
        browser.take_screenshot("screenshot.png")
        
finally:
    api.close()
```

### 2. Tự động hóa web

```python
def web_automation():
    api = AdsPowerAPISync()
    
    try:
        profiles = api.get_profile_list()
        profile_id = profiles['data']['list'][0]['user_id']
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(profile_id)
            
            # Điều hướng đến trang đăng nhập
            browser.navigate_to("https://example.com/login")
            
            # Chờ form xuất hiện
            browser.wait_for_element("input[name='username']")
            
            # Điền thông tin
            browser.fill_input("input[name='username']", "your_username")
            browser.fill_input("input[name='password']", "your_password")
            
            # Click đăng nhập
            browser.click_element("button[type='submit']")
            
            # Chờ chuyển trang
            browser.wait_for_load_state("networkidle")
            
    finally:
        api.close()
```

### 3. Trích xuất dữ liệu

```python
def data_extraction():
    api = AdsPowerAPISync()
    
    try:
        profiles = api.get_profile_list()
        profile_id = profiles['data']['list'][0]['user_id']
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(profile_id)
            
            browser.navigate_to("https://quotes.toscrape.com/")
            browser.wait_for_load_state("load")
            
            # Trích xuất dữ liệu
            quotes = browser.evaluate_script("""
                () => {
                    const quotes = [];
                    document.querySelectorAll('.quote').forEach(quote => {
                        quotes.push({
                            text: quote.querySelector('.text').textContent,
                            author: quote.querySelector('.author').textContent
                        });
                    });
                    return quotes;
                }
            """)
            
            print(f"Trích xuất được {len(quotes)} quotes")
            
    finally:
        api.close()
```

### 4. Quản lý cookies và storage

```python
def cookie_management():
    api = AdsPowerAPISync()
    
    try:
        profiles = api.get_profile_list()
        profile_id = profiles['data']['list'][0]['user_id']
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(profile_id)
            
            browser.navigate_to("https://example.com")
            
            # Lấy cookies
            cookies = browser.get_cookies()
            print(f"Có {len(cookies)} cookies")
            
            # Set cookies mới
            new_cookies = [{
                'name': 'test_cookie',
                'value': 'test_value',
                'domain': 'example.com',
                'path': '/'
            }]
            browser.set_cookies(new_cookies)
            
            # Quản lý local storage
            browser.set_local_storage("key", "value")
            local_storage = browser.get_local_storage()
            print(f"Local storage: {local_storage}")
            
    finally:
        api.close()
```

### 5. Nhiều tab

```python
def multi_tab_example():
    api = AdsPowerAPISync()
    
    try:
        profiles = api.get_profile_list()
        profile_id = profiles['data']['list'][0]['user_id']
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(profile_id)
            
            # Tạo nhiều tab
            urls = ["https://google.com", "https://github.com", "https://stackoverflow.com"]
            
            for i, url in enumerate(urls):
                browser.navigate_to(url, page_index=i)
                page_info = browser.get_page_info(i)
                print(f"Tab {i+1}: {page_info['title']}")
            
    finally:
        api.close()
```

### 6. GoDaddy Automation

```python
from godaddy_auto import GoDaddyAutomation, create_sample_billing_info, create_sample_payment_info

def godaddy_automation():
    api = AdsPowerAPISync()
    
    try:
        profiles = api.get_profile_list()
        profile_id = profiles['data']['list'][0]['user_id']
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(profile_id)
            
            # Khởi tạo GoDaddy Automation
            godaddy = GoDaddyAutomation(browser)
            
            # Tìm kiếm domain
            result = godaddy.search_domain("my-awesome-domain.com")
            print(f"Kết quả: {result}")
            
            # Thêm vào giỏ hàng
            if result["status"] == "success":
                godaddy.add_domain_to_cart("my-awesome-domain.com")
            
            # Mua domain (demo)
            billing_info = create_sample_billing_info()
            payment_info = create_sample_payment_info()
            
            purchase_result = godaddy.buy_domain_complete(
                domain_name="demo-domain.com",
                billing_info=billing_info,
                payment_info=payment_info
            )
            
            print(f"Kết quả mua: {purchase_result}")
            
    finally:
        api.close()
```

## API Reference

### AdsPowerAPISync

#### Quản lý Profiles
- `get_profile_list(page, page_size)` - Lấy danh sách profiles
- `get_profile_detail(user_id)` - Lấy thông tin chi tiết profile
- `create_profile(profile_data)` - Tạo profile mới
- `update_profile(user_id, profile_data)` - Cập nhật profile
- `delete_profile(user_id)` - Xóa profile

#### Quản lý Browser (API v2)
- `start_browser(profile_id, headless, last_opened_tabs, proxy_detection, password_filling, password_saving, cdp_mask, delete_cache, device_scale, launch_args)` - Khởi động trình duyệt
- `stop_browser(profile_id)` - Dừng trình duyệt
- `get_browser_status(profile_id)` - Kiểm tra trạng thái trình duyệt
- `get_browser_list()` - Lấy danh sách trình duyệt đang chạy
- `get_webdriver_url(profile_id)` - Lấy WebDriver URL cho Playwright
- `get_selenium_url(profile_id)` - Lấy Selenium URL
- `get_webdriver_path(profile_id)` - Lấy đường dẫn WebDriver

#### Quản lý Cookies & Storage
- `get_cookies(user_id, domain)` - Lấy cookies
- `update_cookies(user_id, cookies, domain)` - Cập nhật cookies
- `clear_cookies(user_id, domain)` - Xóa cookies
- `get_local_storage(user_id, domain)` - Lấy local storage
- `update_local_storage(user_id, storage_data, domain)` - Cập nhật local storage
- `get_session_storage(user_id, domain)` - Lấy session storage

### GoDaddyAutomation

#### Tìm kiếm Domain
- `search_domain(domain_name)` - Tìm kiếm domain đơn lẻ
- `search_multiple_domains(domain_list)` - Tìm kiếm nhiều domain
- `get_available_domains(search_results)` - Lấy domain có sẵn

#### Quản lý Giỏ hàng
- `add_domain_to_cart(domain_name, duration)` - Thêm domain vào giỏ hàng
- `get_cart_summary()` - Lấy thông tin giỏ hàng
- `proceed_to_checkout()` - Tiến hành thanh toán

#### Thanh toán
- `fill_billing_info(billing_info)` - Điền thông tin thanh toán
- `fill_payment_info(payment_info)` - Điền thông tin thẻ
- `complete_purchase()` - Hoàn tất mua hàng
- `buy_domain_complete(domain_name, billing_info, payment_info)` - Mua domain hoàn chỉnh

### BrowserControllerSync

#### Kết nối và Quản lý (API v2)
- `connect_to_browser(profile_id, headless, last_opened_tabs, proxy_detection, password_filling, password_saving, cdp_mask, delete_cache, device_scale, launch_args)` - Kết nối đến trình duyệt
- `create_context(**kwargs)` - Tạo browser context
- `new_page(**kwargs)` - Tạo trang mới
- `get_page(index)` - Lấy trang theo index

#### Điều hướng
- `navigate_to(url, page_index, **kwargs)` - Điều hướng đến URL
- `wait_for_load_state(state, page_index)` - Chờ trang load
- `wait_for_network_idle(page_index, timeout)` - Chờ network idle

#### Tương tác với Elements
- `wait_for_element(selector, page_index, timeout)` - Chờ element xuất hiện
- `click_element(selector, page_index, **kwargs)` - Click element
- `fill_input(selector, text, page_index, **kwargs)` - Điền text vào input
- `get_text(selector, page_index)` - Lấy text từ element
- `get_attribute(selector, attribute, page_index)` - Lấy attribute
- `hover_element(selector, page_index)` - Hover vào element
- `scroll_to_element(selector, page_index)` - Scroll đến element
- `select_option(selector, value, page_index)` - Chọn option

#### JavaScript
- `evaluate_script(script, page_index)` - Thực thi JavaScript
- `inject_script(script, page_index)` - Inject JavaScript

#### File Operations
- `upload_file(selector, file_path, page_index)` - Upload file
- `download_file(url, download_path, page_index)` - Download file

#### Screenshot và Thông tin
- `take_screenshot(path, page_index, **kwargs)` - Chụp ảnh màn hình
- `get_page_info(page_index)` - Lấy thông tin trang

## Xử lý lỗi

### Lỗi thường gặp

1. **"Browser not active"**
   - Kiểm tra AdsPower đang chạy
   - Kiểm tra Local API đang hoạt động
   - Đảm bảo profile tồn tại

2. **"Connection refused"**
   - Kiểm tra URL API trong config
   - Kiểm tra firewall/antivirus
   - Thử khởi động lại AdsPower

3. **"Element not found"**
   - Tăng timeout trong config
   - Kiểm tra selector có đúng không
   - Chờ trang load hoàn tất

### Debug

Bật debug logging:

```python
from loguru import logger
logger.add("debug.log", level="DEBUG")
```

## Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## License

Dự án này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## Hỗ trợ

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra [Issues](../../issues) hiện có
2. Tạo issue mới với thông tin chi tiết
3. Cung cấp log file và cấu hình

## Changelog

### v2.0.0 - API v2 Integration
- ✅ Tích hợp AdsPower Local API v2 (Sync)
- ✅ Hỗ trợ tất cả tính năng mới của API v2
- ✅ Launch arguments tùy chỉnh
- ✅ Device scale cho mobile profiles
- ✅ Password filling và saving
- ✅ Cache deletion options
- ✅ Proxy detection
- ✅ CDP mask protection
- ✅ **GoDaddy Automation**: Tự động hóa mua domain
- ✅ Điều khiển Playwright qua CDP (Sync)
- ✅ Quản lý profiles và browser
- ✅ Tự động hóa web cơ bản
- ✅ Quản lý cookies và storage
- ✅ Logging và cấu hình
- ✅ Đơn giản, không cần async/await

### v1.0.0
- ✅ Tích hợp AdsPower Local API (Sync)
- ✅ Điều khiển Playwright qua CDP (Sync)
- ✅ Quản lý profiles và browser
- ✅ Tự động hóa web cơ bản
- ✅ Quản lý cookies và storage
- ✅ Logging và cấu hình
- ✅ Đơn giản, không cần async/await