
import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# --- CẤU HÌNH ---
FINANCE_URL = "https://www.google.com/finance/quote/JPY-VND"
CSS_SELECTOR = "div.YMlKec.fxKbKc"

# --- LẤY TOKEN TỪ CASPIO (OAuth 2.0) ---
def get_caspio_token():
    """
    Sử dụng Client ID và Client Secret để lấy access token từ Caspio.
    """
    print("\n--- BƯỚC 1: LẤY TOKEN XÁC THỰC ---")
    print("Đang kết nối đến Caspio để lấy access token...")
    
    token_url = os.getenv("CASPIO_TOKEN_ENDPOINT_URL")
    client_id = os.getenv("CASPIO_CLIENT_ID")
    client_secret = os.getenv("CASPIO_CLIENT_SECRET")

    if not all([token_url, client_id, client_secret]):
        print("❌ Lỗi: Vui lòng thiết lập CASPIO_TOKEN_ENDPOINT_URL, CASPIO_CLIENT_ID, và CASPIO_CLIENT_SECRET.")
        return None

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload, timeout=15)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if access_token:
            print("✅ Lấy access token thành công!")
            return access_token
        else:
            print(f"❌ Lỗi: Không nhận được access_token từ Caspio. Phản hồi: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi lấy access token: {e}")
        if e.response is not None:
            print(f"   Phản hồi từ Caspio: {e.response.text}")
        return None

# --- LẤY DỮ LIỆU TỈ GIÁ ---
def get_exchange_rate():
    """
    Truy cập vào trang Google Finance và lấy tỉ giá JPY-VND.
    """
    print("\n--- BƯỚC 2: LẤY TỈ GIÁ TỪ GOOGLE FINANCE ---")
    print(f"Đang truy cập URL: {FINANCE_URL}...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(FINANCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        rate_element = soup.select_one(CSS_SELECTOR)
        
        if rate_element:
            rate_text = rate_element.get_text(strip=True)
            rate_text_standardized = rate_text.replace(',', '.')
            rate_value = float(rate_text_standardized)
            print(f"✅ Lấy tỉ giá thành công: 1 JPY = {rate_value} VND")
            return rate_value
        else:
            print("❌ Lỗi: Không tìm thấy element chứa tỉ giá trên trang web.")
            return None
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi lấy tỉ giá: {e}")
        return None

# --- TẠO BẢN GHI MỚI TRONG CASPIO ---
def create_record_caspio(rate, access_token):
    """
    Gửi tỉ giá đến Caspio API để TẠO một bản ghi mới.
    """
    print("\n--- BƯỚC 3: TẠO BẢN GHI MỚI TRÊN CASPIO ---")
    
    caspio_table_api_url = os.getenv("CASPIO_TABLE_API_URL")

    if not caspio_table_api_url:
        print("❌ Lỗi: Vui lòng thiết lập CASPIO_TABLE_API_URL.")
        return False

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "tigiaYEN_VND": rate
    }
    
    print(f"Đang gửi dữ liệu đến Caspio: {payload}")
    
    try:
        response = requests.post(caspio_table_api_url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        print(f"✅ Tạo bản ghi mới thành công! (Mã phản hồi: {response.status_code})")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gọi Caspio API: {e}")
        if e.response is not None:
            print(f"   Mã phản hồi: {e.response.status_code}")
            print(f"   Nội dung lỗi: {e.response.text}")
        return False

# --- HÀM CHÍNH ĐỂ CHẠY ---
if __name__ == "__main__":
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("==================================================")
    print(f" BẮT ĐẦU TÁC VỤ CẬP NHẬT TỈ GIÁ - {start_time}")
    print("==================================================")

    token = get_caspio_token()
    
    if token:
        current_rate = get_exchange_rate()
        if current_rate is not None:
            create_record_caspio(current_rate, token)
    
    print("\n==================================================")
    print(" HOÀN THÀNH TÁC VỤ")
    print("==================================================")
