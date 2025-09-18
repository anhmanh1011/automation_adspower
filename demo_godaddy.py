"""
Demo GoDaddy Automation - Tự động hóa mua domain
"""
from adspower_api_sync import AdsPowerAPISync
from browser_controller_sync import BrowserControllerSync
from godaddy_auto import GoDaddyAutomation, create_sample_billing_info, create_sample_payment_info
from loguru import logger


def demo_search_domains():
    """Demo tìm kiếm domain"""
    logger.info("🔍 Demo tìm kiếm domain")
    
    api = AdsPowerAPISync()
    
    try:
        profile_id = "k14ryirf"
        
        with BrowserControllerSync(api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                cdp_mask=True
            )
            
            godaddy = GoDaddyAutomation(browser)
            
            # Tìm kiếm một domain
            domain_to_search = "my-awesome-domain-2024.com"
            result = godaddy.search_domain(domain_to_search)
            
            if result["status"] == "success":
                logger.info(f"✅ Tìm kiếm thành công: {domain_to_search}")
                for domain_result in result["results"]:
                    logger.info(f"   - {domain_result['domain']}: {domain_result['price']} ({domain_result['availability']})")
            else:
                logger.warning(f"⚠️ Tìm kiếm thất bại: {result.get('error')}")
            
            browser.take_screenshot("godaddy_search.png")
            
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
    finally:
        api.close()


def demo_bulk_search():
    """Demo tìm kiếm hàng loạt domain"""
    logger.info("📋 Demo tìm kiếm hàng loạt domain")
    
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
            
            # Danh sách domain cần tìm kiếm
            domain_list = [
                "best-domain-ever.com",
                "awesome-website.net",
                "cool-site.org",
                "my-business.info",
                "startup-idea.co"
            ]
            
            results = godaddy.search_multiple_domains(domain_list)
            
            logger.info("📊 Kết quả tìm kiếm:")
            available_count = 0
            
            for result in results:
                if result["status"] == "success":
                    available_domains = [r for r in result["results"] if "available" in r.get("availability", "").lower()]
                    if available_domains:
                        available_count += len(available_domains)
                        logger.info(f"   ✅ {result['domain']}: {len(available_domains)} domain có sẵn")
                        for domain in available_domains:
                            logger.info(f"      - {domain['domain']}: {domain['price']}")
                    else:
                        logger.info(f"   🔴 {result['domain']}: Không có domain nào có sẵn")
                else:
                    logger.info(f"   ❌ {result['domain']}: {result.get('error')}")
            
            logger.info(f"📈 Tổng cộng: {available_count} domain có sẵn")
            browser.take_screenshot("godaddy_bulk_search.png")
            
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
    finally:
        api.close()


def demo_add_to_cart():
    """Demo thêm domain vào giỏ hàng"""
    logger.info("🛒 Demo thêm domain vào giỏ hàng")
    
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
            
            # Tìm kiếm domain
            domain_to_search = "test-domain-for-cart.com"
            result = godaddy.search_domain(domain_to_search)
            
            if result["status"] == "success" and result["results"]:
                # Thêm domain đầu tiên vào giỏ hàng
                first_domain = result["results"][0]
                domain_name = first_domain["domain"]
                
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
            else:
                logger.warning("⚠️ Không tìm thấy domain để thêm vào giỏ hàng")
            
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
    finally:
        api.close()


def demo_purchase_flow():
    """Demo quy trình mua domain (không thực sự mua)"""
    logger.info("💳 Demo quy trình mua domain")
    
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
            
            # Thông tin mẫu
            billing_info = create_sample_billing_info()
            payment_info = create_sample_payment_info()
            
            # Domain để demo mua
            demo_domain = "demoflow.com"
            
            logger.info(f"🚀 Bắt đầu demo mua domain: {demo_domain}")
            result = godaddy.buy_domain_complete(
                domain_name=demo_domain,
                billing_info=billing_info,
                payment_info=payment_info
            )
            
            logger.info("📊 Kết quả demo:")
            logger.info(f"   - Domain: {result['domain']}")
            logger.info(f"   - Status: {result['status']}")
            logger.info(f"   - Steps completed: {len(result['steps_completed'])}")
            
            for step in result['steps_completed']:
                logger.info(f"      ✅ {step}")
            
            if result["error"]:
                logger.info(f"   - Error: {result['error']}")
            
            browser.take_screenshot("godaddy_purchase_flow.png")
            
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
    finally:
        api.close()


def demo_custom_billing():
    """Demo với thông tin thanh toán tùy chỉnh"""
    logger.info("👤 Demo với thông tin thanh toán tùy chỉnh")
    
    api = AdsPowerAPISync()
    
    try:
        profile_id = "k14ft6fi"
        
        with BrowserControllerSync(adspower_api=api) as browser:
            browser.connect_to_browser(
                profile_id=profile_id,
                headless=False,
                cdp_mask=True
            )
            
            godaddy = GoDaddyAutomation(browser)
            
            # Thông tin thanh toán tùy chỉnh
            custom_billing_info = {
                "first_name": "Nguyen",
                "last_name": "Van A",
                "email": "nguyenvana@example.com",
                "phone": "+84901234567",
                "address": "123 Nguyen Hue Street",
                "city": "Ho Chi Minh City",
                "state": "HCM",
                "zip_code": "700000",
                "country": "VN"
            }
            
            custom_payment_info = {
                "card_number": "4111111111111111",
                "expiry_month": "06",
                "expiry_year": "2026",
                "cvv": "456",
                "cardholder_name": "NGUYEN VAN A"
            }
            
            # Domain để demo
            demo_domain = "vietnam-domain-demo.com"
            
            logger.info(f"🚀 Demo mua domain với thông tin Việt Nam: {demo_domain}")
            result = godaddy.buy_domain_complete(
                domain_name=demo_domain,
                billing_info=custom_billing_info,
                payment_info=custom_payment_info
            )
            
            logger.info("📊 Kết quả demo:")
            logger.info(f"   - Domain: {result['domain']}")
            logger.info(f"   - Status: {result['status']}")
            logger.info(f"   - Steps completed: {', '.join(result['steps_completed'])}")
            
            browser.take_screenshot("godaddy_custom_billing.png")
            
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
    finally:
        api.close()



def main():
    """Chạy tất cả demo GoDaddy"""
    logger.info("🌐 Bắt đầu tất cả demo GoDaddy Automation")
    
    # demos = [
    #     ("Tìm kiếm domain", demo_search_domains),
    #     ("Tìm kiếm hàng loạt", demo_bulk_search),
    #     ("Thêm vào giỏ hàng", demo_add_to_cart),
    #     ("Quy trình mua domain", demo_purchase_flow),
    #     ("Thông tin thanh toán tùy chỉnh", demo_custom_billing)
    # ]
    
    # for name, demo_func in demos:
    #     try:
    #         logger.info(f"🎯 Bắt đầu: {name}")
    #         demo_func()
    #         logger.success(f"✅ Hoàn thành: {name}")
    #         logger.info("⏳ Chờ 3 giây trước demo tiếp theo...")
    #         import time
    #         time.sleep(3)
    #     except Exception as e:
    #         logger.error(f"❌ Lỗi trong {name}: {e}")
    
    # logger.success("🎉 Tất cả demo GoDaddy đã hoàn thành!")

    demo_purchase_flow()


if __name__ == "__main__":
    main()
