# 🌐 GoDaddy Automation Guide

Hướng dẫn sử dụng GoDaddy Automation để tự động hóa mua domain.

## 📋 Tổng quan

GoDaddy Automation cho phép bạn:
- ✅ Tìm kiếm domain tự động
- ✅ Thêm domain vào giỏ hàng
- ✅ Điền thông tin thanh toán
- ✅ Hoàn tất quy trình mua domain
- ✅ Tìm kiếm hàng loạt domain
- ✅ Lọc domain có sẵn

## 🚀 Cài đặt

### 1. Yêu cầu
- Python 3.10+
- AdsPower đã cài đặt và chạy
- Profile AdsPower đã tạo

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 📖 Cách sử dụng

### 1. Demo cơ bản

```python
from adspower_api_sync import AdsPowerAPISync
from browser_controller_sync import BrowserControllerSync
from godaddy_auto import GoDaddyAutomation

# Khởi tạo
api = AdsPowerAPISync()
profile_id = "your-profile-id"

with BrowserControllerSync(api) as browser:
    browser.connect_to_browser(profile_id)
    
    # Khởi tạo GoDaddy Automation
    godaddy = GoDaddyAutomation(browser)
    
    # Tìm kiếm domain
    result = godaddy.search_domain("my-awesome-domain.com")
    print(result)
```

### 2. Tìm kiếm nhiều domain

```python
domain_list = [
    "best-domain-ever.com",
    "awesome-website.net",
    "cool-site.org"
]

results = godaddy.search_multiple_domains(domain_list)

# Lấy domain có sẵn
available = godaddy.get_available_domains(results)
for domain in available:
    print(f"✅ {domain['domain']}: {domain['price']}")
```

### 3. Thêm domain vào giỏ hàng

```python
# Tìm kiếm domain
result = godaddy.search_domain("my-domain.com")

if result["status"] == "success":
    # Thêm vào giỏ hàng
    success = godaddy.add_domain_to_cart("my-domain.com")
    
    if success:
        # Lấy thông tin giỏ hàng
        cart = godaddy.get_cart_summary()
        print(f"Giỏ hàng: {cart}")
```

### 4. Mua domain hoàn chỉnh

```python
from godaddy_auto import create_sample_billing_info, create_sample_payment_info

# Thông tin thanh toán
billing_info = create_sample_billing_info()
payment_info = create_sample_payment_info()

# Mua domain (demo - không thực sự mua)
result = godaddy.buy_domain_complete(
    domain_name="demo-domain.com",
    billing_info=billing_info,
    payment_info=payment_info
)

print(f"Kết quả: {result['status']}")
print(f"Steps completed: {result['steps_completed']}")
```

## 🔧 Cấu hình

### Thông tin thanh toán mẫu

```python
billing_info = {
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

payment_info = {
    "card_number": "4111111111111111",  # Test card
    "expiry_month": "12",
    "expiry_year": "2025",
    "cvv": "123",
    "cardholder_name": "John Doe"
}
```

### Thông tin Việt Nam

```python
vietnam_billing_info = {
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
```

## 📊 API Reference

### GoDaddyAutomation Class

#### Methods chính:

**Tìm kiếm Domain:**
- `search_domain(domain_name)` - Tìm kiếm domain đơn lẻ
- `search_multiple_domains(domain_list)` - Tìm kiếm nhiều domain
- `get_available_domains(search_results)` - Lấy domain có sẵn

**Quản lý Giỏ hàng:**
- `add_domain_to_cart(domain_name, duration)` - Thêm domain vào giỏ hàng
- `get_cart_summary()` - Lấy thông tin giỏ hàng
- `proceed_to_checkout()` - Tiến hành thanh toán

**Thanh toán:**
- `fill_billing_info(billing_info)` - Điền thông tin thanh toán
- `fill_payment_info(payment_info)` - Điền thông tin thẻ
- `complete_purchase()` - Hoàn tất mua hàng
- `buy_domain_complete(domain_name, billing_info, payment_info)` - Mua domain hoàn chỉnh

## 🎯 Demo Scripts

### 1. Chạy tất cả demo
```bash
python demo_godaddy.py
```

### 2. Demo riêng lẻ
```python
# Tìm kiếm domain
python -c "from demo_godaddy import demo_search_domains; demo_search_domains()"

# Tìm kiếm hàng loạt
python -c "from demo_godaddy import demo_bulk_search; demo_bulk_search()"

# Thêm vào giỏ hàng
python -c "from demo_godaddy import demo_add_to_cart; demo_add_to_cart()"

# Quy trình mua
python -c "from demo_godaddy import demo_purchase_flow; demo_purchase_flow()"
```

## ⚠️ Lưu ý quan trọng

### 1. Demo Mode
- Tất cả demo đều dừng trước bước hoàn tất mua hàng thực sự
- Không sử dụng thông tin thẻ thật trong demo
- Luôn test với domain không quan trọng

### 2. Rate Limiting
- GoDaddy có thể giới hạn số lượng request
- Sử dụng delay giữa các request
- Không spam tìm kiếm domain

### 3. Selectors
- GoDaddy có thể thay đổi giao diện
- Cần cập nhật selectors nếu có lỗi
- Sử dụng multiple selectors để tăng độ tin cậy

### 4. Proxy và Fingerprint
- Sử dụng AdsPower để tránh bị block
- Thay đổi profile thường xuyên
- Sử dụng proxy chất lượng

## 🐛 Troubleshooting

### Lỗi thường gặp:

**1. Không tìm thấy ô tìm kiếm:**
```python
# Thử các selector khác
search_selectors = [
    "input[data-cy='search-input']",
    "input[placeholder*='domain']",
    "input[name='domainToCheck']"
]
```

**2. Không thể thêm vào giỏ hàng:**
```python
# Kiểm tra domain có sẵn không
available = godaddy.get_available_domains(results)
if not available:
    print("Không có domain nào có sẵn")
```

**3. Lỗi thanh toán:**
```python
# Kiểm tra thông tin thẻ
if not payment_info.get("card_number"):
    print("Thiếu thông tin thẻ")
```

## 📈 Tips tối ưu

### 1. Tìm kiếm hiệu quả
```python
# Tìm kiếm domain có pattern
domains = [f"domain-{i}.com" for i in range(1, 10)]
results = godaddy.search_multiple_domains(domains)
```

### 2. Lọc domain tốt
```python
# Lọc domain theo giá
available = godaddy.get_available_domains(results)
cheap_domains = [d for d in available if "$" in d["price"] and float(d["price"].replace("$", "")) < 10]
```

### 3. Batch processing
```python
# Xử lý hàng loạt
def process_domains(domain_list):
    results = []
    for domain in domain_list:
        result = godaddy.search_domain(domain)
        results.append(result)
        time.sleep(2)  # Delay giữa các request
    return results
```

## 🔒 Bảo mật

### 1. Thông tin nhạy cảm
- Không commit thông tin thẻ thật
- Sử dụng environment variables
- Mã hóa thông tin thanh toán

### 2. Rate limiting
- Không spam GoDaddy
- Sử dụng delay hợp lý
- Monitor response time

### 3. Error handling
- Luôn có try-catch
- Log lỗi chi tiết
- Retry mechanism

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra log file
2. Test với domain đơn giản
3. Cập nhật selectors
4. Tạo issue trên GitHub

---

**Lưu ý:** Đây là tool demo, không nên sử dụng để mua domain thật mà không kiểm tra kỹ lưỡng.
