"""
Demo đơn giản cho AdsPower Automation - Sync API
Tích hợp GoDaddy Automation
"""
from adspower_api_sync import AdsPowerAPISync
from browser_controller_sync import BrowserControllerSync
from godaddy_auto import GoDaddyAutomation, create_sample_billing_info, create_sample_payment_info
from loguru import logger


def demo_basic_usage():
    """Demo cơ bản"""
    logger.info("🚀 Bắt đầu demo AdsPower Automation")
    
    # Khởi tạo API
    api = AdsPowerAPISync()
    
    try:
        # Lấy danh sách profiles
        # logger.info("📋 Lấy danh sách profiles...")
        # profiles = api.get_profile_list(page=1, page_size=5)
        
        # if not profiles.get('data', {}).get('list'):
        #     logger.warning("⚠️ Không có profile nào. Vui lòng tạo profile trong AdsPower trước.")
        #     return
        
        # # Lấy profile đầu tiên
        # first_profile = profiles['data']['list'][0]
        # profile_id = first_profile['user_id']  # user_id trong API v1 tương đương profile_id trong API v2
        # logger.info(f"👤 Sử dụng profile: {first_profile.get('name', profile_id)}")
        profile_id = "k14ryirf"
        # Kết nối đến trình duyệt với API v2
        with BrowserControllerSync(api) as browser:
            logger.info("🌐 Kết nối đến trình duyệt...")
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,  # Hiển thị browser
                last_opened_tabs=True,  # Tiếp tục tab cuối
                proxy_detection=True,  # Mở trang proxy detection
                cdp_mask=True  # Mask CDP detection
            )
            
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
            browser.fill_input("input[name='q']", "AdsPower automation")
            browser.click_element("input[name='btnK']")
            browser.wait_for_load_state("networkidle")
            
            # Chụp ảnh màn hình
            logger.info("📸 Chụp ảnh màn hình...")
            browser.take_screenshot("demo_screenshot.png")
            
            # Lấy kết quả tìm kiếm
            results = browser.evaluate_script("""
                () => {
                    const results = [];
                    document.querySelectorAll('h3').forEach(h3 => {
                        if (h3.textContent) {
                            results.push(h3.textContent);
                        }
                    });
                    return results.slice(0, 5);
                }
            """)
            
            logger.info("🔍 Kết quả tìm kiếm:")
            for i, result in enumerate(results, 1):
                logger.info(f"   {i}. {result}")
            
            logger.success("✅ Demo hoàn thành thành công!")
            
    except Exception as e:
        logger.error(f"❌ Lỗi trong demo: {e}")
    finally:
        api.close()
        logger.info("🔚 Đã đóng kết nối API")


def demo_godaddy_automation():
    """Demo GoDaddy Automation"""
    logger.info("🌐 Bắt đầu demo GoDaddy Automation")
    
    api = AdsPowerAPISync()
    
    try:
        profile_id = "k14ft6fi"
        
        with BrowserControllerSync(api) as browser:
            logger.info("🌐 Kết nối đến trình duyệt...")
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                last_opened_tabs=True,
                proxy_detection=True,
                cdp_mask=True
            )
            
            # Khởi tạo GoDaddy Automation
            godaddy = GoDaddyAutomation(browser)
            
            # Demo 1: Tìm kiếm domain đơn lẻ
            logger.info("🔍 Demo 1: Tìm kiếm domain đơn lẻ")
            domain_to_search = "example-domain-2024.com"
            search_result = godaddy.search_domain(domain_to_search)
            
            if search_result["status"] == "success":
                logger.info(f"📊 Kết quả tìm kiếm cho {domain_to_search}:")
                for result in search_result["results"]:
                    logger.info(f"   - {result['domain']}: {result['price']} ({result['availability']})")
            else:
                logger.warning(f"⚠️ Không thể tìm kiếm domain: {search_result.get('error')}")
            
            # Chụp ảnh màn hình
            browser.take_screenshot("godaddy_search_result.png")
            
            # Demo 2: Tìm kiếm nhiều domain
            logger.info("🔍 Demo 2: Tìm kiếm nhiều domain")
            domain_list = [
                "my-awesome-site.com",
                "best-domain-ever.net",
                "cool-website.org"
            ]
            
            multiple_results = godaddy.search_multiple_domains(domain_list)
            
            logger.info("📊 Kết quả tìm kiếm nhiều domain:")
            for result in multiple_results:
                if result["status"] == "success":
                    logger.info(f"   ✅ {result['domain']}: {len(result['results'])} kết quả")
                else:
                    logger.info(f"   ❌ {result['domain']}: {result.get('error')}")
            
            # Demo 3: Lấy danh sách domain có sẵn
            logger.info("📋 Demo 3: Lấy danh sách domain có sẵn")
            available_domains = godaddy.get_available_domains(multiple_results)
            
            if available_domains:
                logger.info("🟢 Domains có sẵn:")
                for domain in available_domains:
                    logger.info(f"   - {domain['domain']}: {domain['price']}")
            else:
                logger.info("🔴 Không có domain nào có sẵn")
            
            # Demo 4: Thêm domain vào giỏ hàng (demo)
            if available_domains:
                logger.info("🛒 Demo 4: Thêm domain vào giỏ hàng")
                first_available = available_domains[0]
                domain_name = first_available["domain"]
                
                if godaddy.add_domain_to_cart(domain_name):
                    logger.success(f"✅ Đã thêm {domain_name} vào giỏ hàng")
                    
                    # Lấy thông tin giỏ hàng
                    cart_summary = godaddy.get_cart_summary()
                    logger.info("🛒 Thông tin giỏ hàng:")
                    for item in cart_summary["items"]:
                        logger.info(f"   - {item['name']}: {item['price']}")
                    if cart_summary["total"]:
                        logger.info(f"   💰 Tổng: {cart_summary['total']}")
                    
                    browser.take_screenshot("godaddy_cart.png")
                else:
                    logger.warning(f"⚠️ Không thể thêm {domain_name} vào giỏ hàng")
            
            # Demo 5: Demo mua domain hoàn chỉnh (không thực sự mua)
            logger.info("💳 Demo 5: Demo mua domain hoàn chỉnh")
            
            # Tạo thông tin mẫu
            billing_info = create_sample_billing_info()
            payment_info = create_sample_payment_info()
            
            # Chọn domain để demo mua
            demo_domain = "demo-purchase-domain.com"
            
            logger.info(f"🚀 Bắt đầu demo mua domain: {demo_domain}")
            purchase_result = godaddy.buy_domain_complete(
                domain_name=demo_domain,
                billing_info=billing_info,
                payment_info=payment_info
            )
            
            logger.info(f"📊 Kết quả demo mua domain:")
            logger.info(f"   - Domain: {purchase_result['domain']}")
            logger.info(f"   - Status: {purchase_result['status']}")
            logger.info(f"   - Steps completed: {', '.join(purchase_result['steps_completed'])}")
            
            if purchase_result["error"]:
                logger.info(f"   - Error: {purchase_result['error']}")
            
            # Chụp ảnh màn hình cuối
            browser.take_screenshot("godaddy_final_demo.png")
            
            logger.success("✅ Demo GoDaddy Automation hoàn thành!")
            
    except Exception as e:
        logger.error(f"❌ Lỗi trong demo GoDaddy: {e}")
    finally:
        api.close()
        logger.info("🔚 Đã đóng kết nối API")


def demo_godaddy_quick_search():
    """Demo tìm kiếm nhanh GoDaddy"""
    logger.info("⚡ Demo tìm kiếm nhanh GoDaddy")
    
    api = AdsPowerAPISync()
    
    try:
        profile_id = "k14ft6fi"
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                cdp_mask=True
            )
            
            godaddy = GoDaddyAutomation(browser)
            
            # Tìm kiếm nhanh một domain
            quick_domain = "quick-test-domain.com"
            result = godaddy.search_domain(quick_domain)
            
            if result["status"] == "success":
                logger.info(f"✅ Tìm kiếm thành công: {quick_domain}")
                for domain_result in result["results"]:
                    logger.info(f"   - {domain_result['domain']}: {domain_result['price']}")
            else:
                logger.warning(f"⚠️ Tìm kiếm thất bại: {result.get('error')}")
            
            browser.take_screenshot("godaddy_quick_search.png")
            
    except Exception as e:
        logger.error(f"❌ Lỗi trong demo tìm kiếm nhanh: {e}")
    finally:
        api.close()


if __name__ == "__main__":
    # Chạy demo cơ bản
    demo_basic_usage()
    
    # Chạy demo GoDaddy
    demo_godaddy_automation()
    
    # Chạy demo tìm kiếm nhanh
    demo_godaddy_quick_search()
