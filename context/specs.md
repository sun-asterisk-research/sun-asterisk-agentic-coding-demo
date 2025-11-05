# Personal Finance Tracker - Dự án Demo với Django & Django Template

---

## 1. Tổng quan dự án

- **Tên ứng dụng:** Personal Finance Tracker
- **Mục tiêu:** Cho phép người dùng cá nhân ghi lại thu/chi hàng ngày, theo dõi báo cáo tài chính, nhận cảnh báo và gợi ý tiết kiệm từ AI agent.
- **Công nghệ sử dụng:** Django (Backend, ORM, Auth), Django Template Language (Frontend), SQLite (database mặc định), Chart.js (biểu đồ), Bootstrap (giao diện).

---

## 2. Tính năng chính

### A. Xác thực người dùng

- Đăng ký tài khoản (username, email, password).
- Đăng nhập/Đăng xuất.
- Quản lý phiên đăng nhập (session-based).

### B. Quản lý khoản thu/chi (Transaction CRUD)

- Thêm mới khoản thu/chi:
    - Số tiền (amount)
    - Loại giao dịch (Type): Thu hoặc Chi
    - Danh mục (Category): chọn từ danh sách cố định (ví dụ: Ăn uống, Học tập, Xăng xe, Giải trí, v.v.)
    - Ngày giao dịch (Date): mặc định là hôm nay, có thể chọn lại
    - Ghi chú (Note): tùy chọn
- Sửa/Xóa khoản thu/chi đã nhập.
- Hiển thị danh sách các khoản thu/chi theo ngày, có phân trang hoặc cuộn vô hạn.

### C. Danh mục thu/chi

- Danh sách category cố định (cài trong admin, người dùng không chỉnh sửa được):
    - Ăn uống, Học tập, Xăng xe, Giải trí, Mua sắm, Y tế, Lương, Thưởng, Khác,...
- Có thể thêm category mới từ admin Django (cho phép mở rộng sau này).

### D. Báo cáo & Thống kê

- Xem tổng hợp chi tiêu và thu nhập:
    - Tổng thu/chi trong ngày, tuần, tháng, năm
    - Tổng từng danh mục theo từng khoảng thời gian
- Lọc giao dịch theo ngày, tháng, năm, loại (thu/chi), và danh mục.

### E. Biểu đồ trực quan

- Biểu đồ tròn (pie chart): Tỉ lệ các loại chi tiêu từng danh mục trong tháng.
- Biểu đồ cột/đường (bar/line chart): Biến động chi tiêu/thu nhập theo ngày/tháng.
- Sử dụng Chart.js nhúng vào Django Template.

### G. Giao diện người dùng

- Sử dụng Bootstrap hoặc Tailwind CSS, tone màu **xanh lá cây** và **trắng**.
- Responsive, hiển thị tốt trên mobile và desktop.
- Giao diện hiện đại, tối giản, dễ sử dụng.

---

## 3. Cấu trúc dữ liệu (Models)

```python
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name}: {self.amount} ({self.date})"
```


## 4. Các trang chính (Views & Templates)

-   Trang đăng ký/đăng nhập
-   Dashboard: Tổng quan tài chính, các biểu đồ, cảnh báo/gợi ý từ AI agent.
-   Trang danh sách giao dịch: Hiển thị, lọc và thao tác CRUD.
-   Trang thêm/sửa giao dịch: Form nhập liệu.
-   Trang báo cáo: Lọc, thống kê, biểu đồ chi tiết.
-   Giao diện profile user (nếu cần).

----------

## 5. Luồng sử dụng

1.  Đăng ký/Đăng nhập
2.  Thêm mới các khoản thu/chi hàng ngày
3.  Xem thống kê tổng quan và biểu đồ
4.  Nhận gợi ý/cảnh báo từ AI agent (dưới dạng thông báo trên dashboard)
5.  Chỉnh sửa/xoá các khoản mục khi cần

----------

## 6. Yêu cầu khác

-   Không cần API, tất cả xử lý bằng Django view và template
-   Tối ưu UX/UI đơn giản, hiện đại
-   Code clean, dễ đọc, dễ mở rộng