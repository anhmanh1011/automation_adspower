"""
GoDaddy Automation - Tự động hóa mua domain và quản lý
"""
import time
import random
from typing import Dict, List, Optional, Tuple
from loguru import logger
from browser_controller_sync import BrowserControllerSync
from adspower_api_sync import AdsPowerAPISync
from utils import AdsPowerUtils
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class GoDaddyAutomation:
    """Class tự động hóa GoDaddy"""
    
    def __init__(self, browser_controller: BrowserControllerSync):
        self.browser = browser_controller
        self.base_url = "https://www.godaddy.com/en-ca"
        
    def navigate_to_godaddy(self) -> None:
        """Điều hướng đến GoDaddy"""
        logger.info("🌐 Điều hướng đến GoDaddy...")
        self.browser.navigate_to(self.base_url)
        self.browser.wait_for_load_state("load")
        AdsPowerUtils.random_delay(2, 4)
        
    def search_domain(self, domain_name: str) -> Dict:
        """Tìm kiếm domain"""
        logger.info(f"🔍 Tìm kiếm domain: {domain_name}")
        
        try:

            selector = "input[name='searchText']"
            
            search_input = self.browser.wait_for_element(selector, timeout=5000)
            
            if not search_input:
                raise Exception("Không tìm thấy ô tìm kiếm domain")
            
            # Nhập tên domain
            self.browser.fill_input(selector, domain_name)
            self.browser.send_key_enter(selector)

            AdsPowerUtils.random_delay(1, 2)
            
            # # Click nút tìm kiếm
            # search_button_selectors = [
            #     "button[data-cy='search-button']",
            #     "button[type='submit']",
            #     ".search-button",
            #     ".domain-search-button",
            #     "button:contains('Search')",
            #     "button:contains('Find')"
            # ]
            
            # for selector in search_button_selectors:
            #     try:
            #         self.browser.click_element(selector)
            #         break
            #     except:
            #         continue
            
            # Chờ kết quả tìm kiếm
            self.browser.wait_for_load_state("networkidle")
            AdsPowerUtils.random_delay(3, 5)
            
            # Lấy kết quả tìm kiếm
            results = self._get_search_results()
            logger.info(f"📊 Tìm thấy {len(results)} kết quả cho domain: {domain_name}")
            
            return {
                "domain": domain_name,
                "results": results,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"❌ Lỗi tìm kiếm domain {domain_name}: {e}")
            return {
                "domain": domain_name,
                "results": [],
                "status": "error",
                "error": str(e)
            }
    
    def _get_search_results(self) -> List[Dict]:
        """Lấy kết quả tìm kiếm domain"""
        try:
            results = self.browser.evaluate_script("""
                () => {
                    const results = [];
                    
                    // Tìm các element chứa kết quả domain
                    const domainElements = document.querySelectorAll([
                        '.domain-name',
                        '.domain-result',
                        '.search-result',
                        '[data-cy="domain-result"]',
                        '.domain-card'
                    ].join(', '));
                    
                    domainElements.forEach((element, index) => {
                        try {
                            const domainName = element.querySelector('.domain-name, .domain-text, h3, h4')?.textContent?.trim();
                            const priceElement = element.querySelector('.price, .domain-price, .cost, [data-cy="price"]');
                            const price = priceElement?.textContent?.trim();
                            const availability = element.querySelector('.available, .unavailable, .status')?.textContent?.trim();
                            
                            if (domainName) {
                                results.push({
                                    domain: domainName,
                                    price: price || 'N/A',
                                    availability: availability || 'Unknown',
                                    index: index
                                });
                            }
                        } catch (e) {
                            console.log('Error parsing domain element:', e);
                        }
                    });
                    
                    return results;
                }
            """)
            
            return results if results else []
            
        except Exception as e:
            logger.error(f"❌ Lỗi lấy kết quả tìm kiếm: {e}")
            return []
    
    def add_domain_to_cart(self, domain_name: str, duration: str = "1 year") -> bool:
        """Thêm domain vào giỏ hàng"""
        logger.info(f"🛒 Thêm domain {domain_name} vào giỏ hàng...")
        
        try:
            # Tìm nút "Add to Cart" cho domain cụ thể
            add_to_cart_selectors = [
                f"button[data-domain='{domain_name}']",
                f"button:contains('Add to Cart')",
                f"button:contains('Add')",
                ".add-to-cart-button",
                "[data-cy='add-to-cart']"
            ]
            
            added = False
            for selector in add_to_cart_selectors:
                try:
                    self.browser.click_element(selector)
                    added = True
                    break
                except:
                    continue
            
            if not added:
                # Thử click vào domain card trước
                domain_card_selectors = [
                    f"[data-domain='{domain_name}']",
                    f".domain-card:contains('{domain_name}')",
                    f".domain-result:contains('{domain_name}')"
                ]
                
                for selector in domain_card_selectors:
                    try:
                        self.browser.click_element(selector)
                        AdsPowerUtils.random_delay(1, 2)
                        
                        # Sau đó tìm nút Add to Cart
                        self.browser.click_element("button:contains('Add to Cart'), button:contains('Add')")
                        added = True
                        break
                    except:
                        continue
            
            if added:
                self.browser.wait_for_load_state("networkidle")
                AdsPowerUtils.random_delay(2, 3)
                logger.success(f"✅ Đã thêm domain {domain_name} vào giỏ hàng")
                return True
            else:
                logger.warning(f"⚠️ Không thể thêm domain {domain_name} vào giỏ hàng")
                return False
                
        except Exception as e:
            logger.error(f"❌ Lỗi thêm domain vào giỏ hàng: {e}")
            return False
    
    def proceed_to_checkout(self) -> bool:
        """Tiến hành thanh toán"""
        logger.info("💳 Tiến hành thanh toán...")
        
        try:
            # Tìm nút checkout
            checkout_selectors = [
                "button:contains('Checkout')",
                "button:contains('Continue to Checkout')",
                "button:contains('Proceed to Checkout')",
                ".checkout-button",
                "[data-cy='checkout']",
                "a:contains('Checkout')"
            ]
            
            for selector in checkout_selectors:
                try:
                    self.browser.click_element(selector)
                    self.browser.wait_for_load_state("networkidle")
                    AdsPowerUtils.random_delay(3, 5)
                    logger.success("✅ Đã chuyển đến trang thanh toán")
                    return True
                except:
                    continue
            
            logger.warning("⚠️ Không tìm thấy nút checkout")
            return False
            
        except Exception as e:
            logger.error(f"❌ Lỗi tiến hành thanh toán: {e}")
            return False
    
    def fill_billing_info(self, billing_info: Dict) -> bool:
        """Điền thông tin thanh toán"""
        logger.info("📝 Điền thông tin thanh toán...")
        
        try:
            # Điền thông tin cá nhân
            if "first_name" in billing_info:
                self.browser.fill_input("input[name='firstName'], input[name='first_name']", billing_info["first_name"])
            
            if "last_name" in billing_info:
                self.browser.fill_input("input[name='lastName'], input[name='last_name']", billing_info["last_name"])
            
            if "email" in billing_info:
                self.browser.fill_input("input[name='email'], input[type='email']", billing_info["email"])
            
            if "phone" in billing_info:
                self.browser.fill_input("input[name='phone'], input[name='phoneNumber']", billing_info["phone"])
            
            # Điền địa chỉ
            if "address" in billing_info:
                self.browser.fill_input("input[name='address'], input[name='street']", billing_info["address"])
            
            if "city" in billing_info:
                self.browser.fill_input("input[name='city']", billing_info["city"])
            
            if "state" in billing_info:
                self.browser.select_option("select[name='state'], select[name='region']", billing_info["state"])
            
            if "zip_code" in billing_info:
                self.browser.fill_input("input[name='zipCode'], input[name='postalCode']", billing_info["zip_code"])
            
            if "country" in billing_info:
                self.browser.select_option("select[name='country']", billing_info["country"])
            
            AdsPowerUtils.random_delay(2, 3)
            logger.success("✅ Đã điền thông tin thanh toán")
            return True
            
        except Exception as e:
            logger.error(f"❌ Lỗi điền thông tin thanh toán: {e}")
            return False
    
    def fill_payment_info(self, payment_info: Dict) -> bool:
        """Điền thông tin thanh toán"""
        logger.info("💳 Điền thông tin thanh toán...")
        
        try:
            # Điền thông tin thẻ
            if "card_number" in payment_info:
                self.browser.fill_input("input[name='cardNumber'], input[name='card_number']", payment_info["card_number"])
            
            if "expiry_month" in payment_info:
                self.browser.select_option("select[name='expiryMonth'], select[name='exp_month']", payment_info["expiry_month"])
            
            if "expiry_year" in payment_info:
                self.browser.select_option("select[name='expiryYear'], select[name='exp_year']", payment_info["expiry_year"])
            
            if "cvv" in payment_info:
                self.browser.fill_input("input[name='cvv'], input[name='securityCode']", payment_info["cvv"])
            
            if "cardholder_name" in payment_info:
                self.browser.fill_input("input[name='cardholderName'], input[name='cardholder_name']", payment_info["cardholder_name"])
            
            AdsPowerUtils.random_delay(2, 3)
            logger.success("✅ Đã điền thông tin thẻ")
            return True
            
        except Exception as e:
            logger.error(f"❌ Lỗi điền thông tin thẻ: {e}")
            return False
    
    def complete_purchase(self) -> bool:
        """Hoàn tất mua hàng"""
        logger.info("🛒 Hoàn tất mua hàng...")
        
        try:
            # Tìm nút hoàn tất mua hàng
            purchase_selectors = [
                "button:contains('Complete Purchase')",
                "button:contains('Place Order')",
                "button:contains('Buy Now')",
                "button:contains('Purchase')",
                ".purchase-button",
                "[data-cy='complete-purchase']"
            ]
            
            for selector in purchase_selectors:
                try:
                    self.browser.click_element(selector)
                    self.browser.wait_for_load_state("networkidle")
                    AdsPowerUtils.random_delay(5, 8)
                    logger.success("✅ Đã hoàn tất mua hàng")
                    return True
                except:
                    continue
            
            logger.warning("⚠️ Không tìm thấy nút hoàn tất mua hàng")
            return False
            
        except Exception as e:
            logger.error(f"❌ Lỗi hoàn tất mua hàng: {e}")
            return False
    
    def get_cart_summary(self) -> Dict:
        """Lấy thông tin giỏ hàng"""
        try:
            summary = self.browser.evaluate_script("""
                () => {
                    const summary = {
                        items: [],
                        total: null,
                        subtotal: null,
                        tax: null
                    };
                    
                    // Lấy danh sách items
                    const items = document.querySelectorAll('.cart-item, .order-item, .domain-item');
                    items.forEach(item => {
                        const name = item.querySelector('.item-name, .domain-name, .product-name')?.textContent?.trim();
                        const price = item.querySelector('.item-price, .domain-price, .product-price')?.textContent?.trim();
                        if (name) {
                            summary.items.push({ name, price });
                        }
                    });
                    
                    // Lấy tổng tiền
                    const totalElement = document.querySelector('.total, .order-total, .cart-total');
                    if (totalElement) {
                        summary.total = totalElement.textContent.trim();
                    }
                    
                    return summary;
                }
            """)
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Lỗi lấy thông tin giỏ hàng: {e}")
            return {"items": [], "total": None}
    
    def buy_domain_complete(self, domain_name: str, billing_info: Dict, payment_info: Dict) -> Dict:
        """Mua domain hoàn chỉnh"""
        logger.info(f"🚀 Bắt đầu mua domain: {domain_name}")
        
        result = {
            "domain": domain_name,
            "status": "pending",
            "steps_completed": [],
            "error": None
        }
        
        try:
            # Bước 1: Điều hướng đến GoDaddy
            self.navigate_to_godaddy()
            result["steps_completed"].append("navigate_to_godaddy")
            
            # Bước 2: Tìm kiếm domain
            search_result = self.search_domain(domain_name)
            if search_result["status"] != "success":
                result["status"] = "error"
                result["error"] = search_result.get("error", "Tìm kiếm domain thất bại")
                return result
            result["steps_completed"].append("search_domain")
            
            # Bước 3: Thêm domain vào giỏ hàng
            if not self.add_domain_to_cart(domain_name):
                result["status"] = "error"
                result["error"] = "Không thể thêm domain vào giỏ hàng"
                return result
            result["steps_completed"].append("add_to_cart")
            
            # Bước 4: Tiến hành thanh toán
            if not self.proceed_to_checkout():
                result["status"] = "error"
                result["error"] = "Không thể tiến hành thanh toán"
                return result
            result["steps_completed"].append("proceed_to_checkout")
            
            # Bước 5: Điền thông tin thanh toán
            if not self.fill_billing_info(billing_info):
                result["status"] = "error"
                result["error"] = "Không thể điền thông tin thanh toán"
                return result
            result["steps_completed"].append("fill_billing_info")
            
            # Bước 6: Điền thông tin thẻ
            if not self.fill_payment_info(payment_info):
                result["status"] = "error"
                result["error"] = "Không thể điền thông tin thẻ"
                return result
            result["steps_completed"].append("fill_payment_info")
            
            # Bước 7: Hoàn tất mua hàng (chỉ demo, không thực sự mua)
            logger.warning("⚠️ Dừng tại bước hoàn tất mua hàng để tránh mua thật")
            result["status"] = "completed_demo"
            result["steps_completed"].append("ready_to_purchase")
            
            logger.success(f"✅ Hoàn thành demo mua domain: {domain_name}")
            return result
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"❌ Lỗi trong quá trình mua domain: {e}")
            return result
    
    def search_multiple_domains(self, domain_list: List[str]) -> List[Dict]:
        """Tìm kiếm nhiều domain"""
        logger.info(f"🔍 Tìm kiếm {len(domain_list)} domains...")
        
        results = []
        for domain in domain_list:
            logger.info(f"🔍 Tìm kiếm: {domain}")
            result = self.search_domain(domain)
            results.append(result)
            AdsPowerUtils.random_delay(2, 4)  # Delay giữa các lần tìm kiếm
        
        return results
    
    def get_available_domains(self, search_results: List[Dict]) -> List[Dict]:
        """Lấy danh sách domain có sẵn"""
        available = []
        for result in search_results:
            if result["status"] == "success":
                for domain_result in result["results"]:
                    if "available" in domain_result.get("availability", "").lower():
                        available.append(domain_result)
        
        return available


def create_sample_billing_info() -> Dict:
    """Tạo thông tin thanh toán mẫu"""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "address": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "country": "US"
    }


def create_sample_payment_info() -> Dict:
    """Tạo thông tin thẻ mẫu"""
    return {
        "card_number": "4111111111111111",  # Test card number
        "expiry_month": "12",
        "expiry_year": "2025",
        "cvv": "123",
        "cardholder_name": "John Doe"
    }
