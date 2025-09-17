"""
Demo AdsPower Automation với API v2 - Tính năng mới
"""
from adspower_api_sync import AdsPowerAPISync
from browser_controller_sync import BrowserControllerSync
from loguru import logger


def demo_api_v2_features():
    """Demo các tính năng mới của API v2"""
    logger.info("🚀 Demo AdsPower Automation API v2")
    
    api = AdsPowerAPISync()
    
    try:
        # Lấy danh sách profiles
        logger.info("📋 Lấy danh sách profiles...")
        profiles = api.get_profile_list(page=1, page_size=5)
        
        if not profiles.get('data', {}).get('list'):
            logger.warning("⚠️ Không có profile nào. Vui lòng tạo profile trong AdsPower trước.")
            return
        
        profile_id = profiles['data']['list'][0]['user_id']
        logger.info(f"👤 Sử dụng profile: {profile_id}")
        
        # Demo 1: Khởi động browser với các tùy chọn mới
        logger.info("🔧 Demo 1: Khởi động browser với tùy chọn mới...")
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,  # Hiển thị browser
                last_opened_tabs=False,  # Không tiếp tục tab cuối
                proxy_detection=True,  # Mở trang proxy detection
                password_filling=False,  # Không tự động điền password
                password_saving=False,  # Không lưu password
                cdp_mask=True,  # Mask CDP detection
                delete_cache=False,  # Không xóa cache
                launch_args=[  # Thêm launch arguments
                    "--window-position=100,100",
                    "--disable-notifications",
                    "--disable-popup-blocking"
                ]
            )
            
            # Điều hướng đến trang test
            browser.navigate_to("https://httpbin.org/headers")
            browser.wait_for_load_state("load")
            
            # Lấy thông tin headers
            headers = browser.evaluate_script("""
                () => {
                    const headers = document.querySelector('pre').textContent;
                    return JSON.parse(headers);
                }
            """)
            
            logger.info("📊 Headers từ browser:")
            for key, value in headers.items():
                logger.info(f"   {key}: {value}")
            
            # Chụp ảnh màn hình
            browser.take_screenshot("demo_api_v2_headers.png")
            
        # Demo 2: Khởi động browser với device scale (cho mobile profiles)
        logger.info("📱 Demo 2: Test device scale...")
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                device_scale=1.5,  # Zoom 150%
                cdp_mask=True
            )
            
            browser.navigate_to("https://www.google.com")
            browser.wait_for_load_state("load")
            browser.take_screenshot("demo_api_v2_scale.png")
            
        # Demo 3: Test password filling và saving
        logger.info("🔐 Demo 3: Test password features...")
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                password_filling=True,  # Bật tự động điền password
                password_saving=True,  # Bật lưu password
                cdp_mask=True
            )
            
            browser.navigate_to("https://httpbin.org/forms/post")
            browser.wait_for_load_state("load")
            
            # Điền form để test password features
            browser.fill_input("input[name='custname']", "Test User")
            browser.fill_input("input[name='custemail']", "test@example.com")
            browser.fill_input("input[name='custtel']", "0123456789")
            
            browser.take_screenshot("demo_api_v2_password.png")
            
        # Demo 4: Test cache deletion
        logger.info("🗑️ Demo 4: Test cache deletion...")
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                delete_cache=True,  # Xóa cache khi đóng
                cdp_mask=True
            )
            
            browser.navigate_to("https://www.google.com")
            browser.wait_for_load_state("load")
            
            # Lưu một số data vào localStorage
            browser.set_local_storage("test_key", "test_value")
            browser.set_local_storage("demo_data", "API v2 demo")
            
            local_storage = browser.get_local_storage()
            logger.info(f"📦 Local storage trước khi đóng: {local_storage}")
            
            browser.take_screenshot("demo_api_v2_cache.png")
            
        # Demo 5: Test proxy detection
        logger.info("🌐 Demo 5: Test proxy detection...")
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                proxy_detection=True,  # Mở trang proxy detection
                cdp_mask=True
            )
            
            # Điều hướng đến trang kiểm tra IP
            browser.navigate_to("https://httpbin.org/ip")
            browser.wait_for_load_state("load")
            
            ip_info = browser.evaluate_script("""
                () => {
                    const ipData = document.querySelector('pre').textContent;
                    return JSON.parse(ipData);
                }
            """)
            
            logger.info(f"🌍 IP Address: {ip_info.get('origin', 'Unknown')}")
            browser.take_screenshot("demo_api_v2_proxy.png")
            
        logger.success("✅ Tất cả demo API v2 hoàn thành!")
        logger.info("📸 Các ảnh chụp màn hình đã được lưu:")
        logger.info("   - demo_api_v2_headers.png")
        logger.info("   - demo_api_v2_scale.png")
        logger.info("   - demo_api_v2_password.png")
        logger.info("   - demo_api_v2_cache.png")
        logger.info("   - demo_api_v2_proxy.png")
        
    except Exception as e:
        logger.error(f"❌ Lỗi trong demo API v2: {e}")
    finally:
        api.close()
        logger.info("🔚 Đã đóng kết nối API")


def demo_advanced_launch_args():
    """Demo các launch arguments nâng cao"""
    logger.info("🔧 Demo Launch Arguments nâng cao")
    
    api = AdsPowerAPISync()
    
    try:
        profiles = api.get_profile_list(page=1, page_size=1)
        if not profiles.get('data', {}).get('list'):
            logger.warning("⚠️ Không có profile nào.")
            return
        
        profile_id = profiles['data']['list'][0]['user_id']
        
        # Launch arguments nâng cao
        advanced_launch_args = [
            "--window-position=200,200",  # Vị trí cửa sổ
            "--window-size=1200,800",     # Kích thước cửa sổ
            "--disable-notifications",    # Tắt thông báo
            "--disable-popup-blocking",   # Tắt chặn popup
            "--disable-web-security",     # Tắt web security
            "--disable-features=VizDisplayCompositor",  # Tắt một số features
            "--blink-settings=imagesEnabled=false",  # Tắt load hình ảnh
            "--disable-extensions",       # Tắt extensions
            "--no-sandbox",              # Tắt sandbox
            "--disable-dev-shm-usage"    # Tắt dev shm usage
        ]
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                launch_args=advanced_launch_args,
                cdp_mask=True
            )
            
            browser.navigate_to("https://www.google.com")
            browser.wait_for_load_state("load")
            
            # Kiểm tra xem hình ảnh có bị tắt không
            images_disabled = browser.evaluate_script("""
                () => {
                    const images = document.querySelectorAll('img');
                    return images.length === 0;
                }
            """)
            
            logger.info(f"🖼️ Images disabled: {images_disabled}")
            browser.take_screenshot("demo_advanced_launch_args.png")
            
        logger.success("✅ Demo launch arguments hoàn thành!")
        
    except Exception as e:
        logger.error(f"❌ Lỗi trong demo launch arguments: {e}")
    finally:
        api.close()


if __name__ == "__main__":
    # Chạy demo chính
    demo_api_v2_features()
    
    # Chạy demo launch arguments
    demo_advanced_launch_args()
