# Dự án Tự động cập nhật Tỉ giá JPY-VND vào Caspio

Dự án này sử dụng Python để lấy tỉ giá Yên Nhật (JPY) sang Đồng Việt Nam (VND) từ Google Finance và tự động **tạo một bản ghi mới** trong bảng dữ liệu trên Caspio thông qua REST API.

Quá trình này được tự động hóa bằng GitHub Actions để chạy hàng ngày.

## Cách hoạt động

-   **GitHub Actions** sẽ tự động kích hoạt vào lúc 05:00 sáng giờ Việt Nam mỗi ngày (hoặc khi được chạy thủ công).
-   Nó sẽ chạy tệp `main.py`.
-   Script sẽ thực hiện 3 bước:
    1.  **Lấy Token**: Kết nối đến Caspio bằng `Client ID` và `Client Secret` để lấy token xác thực tạm thời.
    2.  **Lấy Tỉ giá**: Truy cập Google Finance, lấy tỉ giá mới nhất và chuẩn hóa dữ liệu.
    3.  **Tạo Bản ghi**: Gửi yêu cầu `POST` đến Caspio API để tạo một bản ghi mới trong bảng `tigia` với tỉ giá vừa lấy được.

## Cài đặt và Sử dụng

### 1. Chuẩn bị trên Caspio

-   **Bảng Dữ liệu**: Đảm bảo bạn có một bảng tên là `tigia` trong Caspio.
-   **Cột Dữ liệu**: Trong bảng `tigia`, phải có một cột tên là `tigiaYEN_VND` với kiểu dữ liệu là `Number` hoặc tương đương.
-   **Lấy thông tin xác thực**:
    -   Vào phần quản lý API của tài khoản Caspio của bạn (Authentication).
    -   Tạo một bộ credentials mới (API Key).
    -   Copy lại các giá trị: **Client ID**, **Client secret**, và **Token endpoint URL**.

### 2. Thiết lập trên GitHub

1.  **Đưa mã nguồn lên GitHub**: Tạo một repository mới trên GitHub và tải tất cả các tệp (`main.py`, `requirements.txt`, `.github/workflows/daily_update.yml`, `README.md`) lên.

2.  **Cấu hình GitHub Secrets**: Đây là bước quan trọng nhất để bảo mật thông tin nhạy cảm.
    -   Vào repository của bạn, đi đến `Settings` > `Secrets and variables` > `Actions`.
    -   Nhấn `New repository secret` và tạo 4 secrets sau:

| Tên Secret | Giá trị mẫu (Lấy từ tài khoản Caspio của bạn) |
| :--- | :--- |
| `CASPIO_CLIENT_ID` | `abc...xyz` (Giá trị Client ID bạn đã copy) |
| `CASPIO_CLIENT_SECRET` | `123...789` (Giá trị Client secret bạn đã copy) |
| `CASPIO_TOKEN_ENDPOINT_URL` | `https://c1xyz890.caspio.com/oauth/token` (Giá trị Token endpoint URL) |
| `CASPIO_TABLE_API_URL` | `https://c1xyz890.caspio.com/rest/v2/tables/tigia/records` (URL của API cho bảng `tigia`) |

### Lưu ý

-   **Thay đổi cấu trúc web**: Google có thể thay đổi cấu trúc HTML của trang Finance. Nếu script ngừng hoạt động, bạn có thể cần phải cập nhật lại giá trị của `CSS_SELECTOR` trong `main.py`.
-   **Tệp `.env`**: Tệp `.env` chỉ dùng để kiểm thử trên máy tính cá nhân và không nên được đưa lên GitHub. Hãy chắc chắn rằng bạn đã thêm `.env` vào tệp `.gitignore`.
