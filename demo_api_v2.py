"""
Demo AdsPower Automation với API v2 - Tính năng mới
"""
from adspower_api_sync import AdsPowerAPISync
from browser_controller_sync import BrowserControllerSync
from loguru import logger
import time
from concurrent.futures import ThreadPoolExecutor


def demo_api_v2_features():
    """Demo các tính năng mới của API v2"""
    logger.info("🚀 Demo AdsPower Automation API v2")
    
    api = AdsPowerAPISync()
    profiles = create_mutiple_profiles(api)
    # profiles = api.get_profile_list()
    
    start_results = api.start_multiple_browsers(profiles)
    try:
        with ThreadPoolExecutor(max_workers=6) as executor:
            
            for profile in profiles:
                webdriver_url = start_results[profile]['data']['ws']['puppeteer']
                future = executor.submit(
                    automation_task,
                    profile,
                    webdriver_url,
                    api
                )
                    # Lấy danh sách profiles
      
        
    except Exception as e:
        logger.error(f"❌ Lỗi trong demo API v2: {e}")
    finally:
        api.close()
        logger.info("🔚 Đã đóng kết nối API")

def automation_task(profile_id: str,webdriver_url: str, api:AdsPowerAPISync):
    """Tác vụ tự động hóa"""
    with BrowserControllerSync(api) as browser:
        try:
            browser.connect_to_browser(profile_id, webdriver_url)
            # Điều hướng đến Google
            logger.info("🔍 Điều hướng đến Google...")
            browser.navigate_to("https://www.google.com")
            browser.wait_for_load_state("load")
            
            # Lấy thông tin trang
            page_info = browser.get_page_info()
            logger.info(f"📄 Trang hiện tại: {page_info['title']}")
            logger.info(f"🔗 URL: {page_info['url']}")
            
            # Tìm kiếm
            logger.info("🔍 Thực hiện tìm kiếm...")
            browser.fill_input("textarea[name='q']", "AdsPower automation")
            browser.click_element("input[name='btnK']")
            browser.wait_for_load_state("networkidle")
        except Exception as e:
            logger.error(f"❌ Lỗi trong demo API v2: {e}")
        finally:
            # browser.close()
            logger.info("🔚 Đã đóng kết nối API")

def create_mutiple_profiles(api:AdsPowerAPISync):
    """Tạo nhiều profile"""
    results = []
    for i in range(6):
        profile = api.create_profile(name=f"Test Profile {i}", user_proxy_config={"proxy_soft":"no_proxy"})
        results.append(profile['data']['profile_id'])
        time.sleep(0.5)
    api.close()
    logger.success("✅ Tất cả profile đã được tạo")
    return results

if __name__ == "__main__":
    # Chạy demo chính
    demo_api_v2_features()
