# Personal Finance Tracker - Ứng dụng Theo dõi Chi tiêu Cá nhân

---

## 1. Tổng quan dự án

- **Tên ứng dụng:** Personal Finance Tracker (Ứng dụng Theo dõi Chi tiêu Cá nhân)
- **Mục tiêu:**
  - Giúp người dùng quản lý thu chi cá nhân hàng ngày
  - Theo dõi và phân loại các khoản thu/chi theo danh mục
  - Cung cấp báo cáo trực quan về tình hình tài chính
  - Cảnh báo khi chi tiêu vượt mức và gợi ý tiết kiệm
- **Công nghệ sử dụng:**
  - Backend: Django 4.x, Django REST Framework
  - Database: PostgreSQL 15
  - Frontend: HTML, CSS, JavaScript, Bootstrap 5
  - Charts: Chart.js hoặc ApexCharts
  - Deployment: Docker Compose
  - Tone màu: Xanh lá (chủ đạo) và Trắng

---

## 2. Tính năng chính

### A. Xác thực người dùng (Authentication)

- **Đăng ký tài khoản mới:**
  - Username (unique)
  - Email
  - Password (với xác nhận)
  - Tên hiển thị (display name)

- **Đăng nhập:**
  - Username/Email và Password
  - Session-based authentication
  - Remember me option

- **Đăng xuất**

- **Quản lý profile:**
  - Cập nhật thông tin cá nhân
  - Đổi mật khẩu
  - Avatar (optional)

### B. Quản lý Danh mục (Categories)

- **Danh mục cố định (pre-configured)** tương tự Money Lover:

  **Danh mục Chi tiêu (Expense Categories):**
  - 🍔 Ăn uống (Food & Beverage)
  - 🚗 Xăng xe (Transportation)
  - 🏠 Nhà cửa (Housing)
  - 👕 Mua sắm (Shopping)
  - 💊 Y tế (Healthcare)
  - 📚 Giáo dục (Education)
  - 🎬 Giải trí (Entertainment)
  - 📱 Điện thoại/Internet (Bills & Utilities)
  - 👨‍👩‍👧 Gia đình (Family)
  - 🎁 Quà tặng (Gifts & Donations)
  - ⚡ Khác (Other)

  **Danh mục Thu nhập (Income Categories):**
  - 💰 Lương (Salary)
  - 💼 Thưởng (Bonus)
  - 📈 Đầu tư (Investment)
  - 🎯 Thu nhập phụ (Side Income)
  - 🎁 Quà tặng (Gifts)
  - ⚡ Khác (Other)

- **Quản lý danh mục qua Django Admin:**
  - Admin có thể thêm/sửa/xóa danh mục
  - Mỗi danh mục có: tên, icon (emoji), loại (thu/chi), màu sắc
  - Người dùng thông thường không thể tạo danh mục mới (chỉ sử dụng danh mục có sẵn)

### C. Quản lý Giao dịch (Transactions) - CRUD

- **Tạo giao dịch mới:**
  - Loại: Thu hoặc Chi (Income/Expense)
  - Số tiền (amount) - số dương
  - Danh mục (category) - chọn từ danh sách có sẵn
  - Ngày giao dịch (date) - mặc định hôm nay
  - Ghi chú (note) - tùy chọn
  - Người dùng (user) - tự động lấy từ user đang đăng nhập

- **Xem danh sách giao dịch:**
  - Hiển thị dạng bảng/list
  - Phân trang (pagination)
  - Sắp xếp theo ngày (mới nhất trước)
  - Hiển thị: ngày, danh mục (icon + tên), số tiền (màu đỏ cho chi, xanh cho thu), ghi chú

- **Cập nhật giao dịch:**
  - Cho phép sửa tất cả thông tin
  - Chỉ user sở hữu giao dịch mới được sửa

- **Xóa giao dịch:**
  - Xác nhận trước khi xóa
  - Chỉ user sở hữu giao dịch mới được xóa

- **Lọc giao dịch:**
  - Theo khoảng thời gian (date range)
  - Theo danh mục
  - Theo loại (thu/chi)

### D. Báo cáo và Thống kê (Reports & Analytics)

- **Dashboard tổng quan:**
  - Tổng thu nhập trong tháng hiện tại
  - Tổng chi tiêu trong tháng hiện tại
  - Số dư (thu - chi)
  - Số lượng giao dịch

- **Thống kê theo thời gian:**
  - Chọn khoảng thời gian: Ngày, Tuần, Tháng, Năm
  - Hiển thị tổng thu/chi theo khoảng thời gian đã chọn

- **Biểu đồ trực quan:**

  1. **Biểu đồ cột (Bar Chart):**
     - Hiển thị thu/chi theo ngày trong tuần/tháng
     - Trục X: Ngày
     - Trục Y: Số tiền
     - Hai cột: Thu (màu xanh lá) và Chi (màu đỏ/cam)

  2. **Biểu đồ tròn (Pie Chart):**
     - Chi tiêu theo danh mục (% của tổng chi)
     - Màu sắc theo từng danh mục
     - Hiển thị % và số tiền

  3. **Biểu đồ đường (Line Chart):**
     - Xu hướng thu/chi theo thời gian
     - Theo dõi sự thay đổi qua các tháng

  4. **Biểu đồ so sánh (Comparison Chart):**
     - So sánh thu/chi giữa các tháng
     - Giúp thấy xu hướng tăng/giảm

### E. Tính năng AI/Gợi ý (AI Suggestions - Optional/Future)

- **Cảnh báo chi tiêu vượt mức:**
  - Nếu chi tiêu trong tháng > 120% trung bình 3 tháng trước
  - Hiển thị thông báo warning

- **Gợi ý tiết kiệm:**
  - Phân tích danh mục chi tiêu nhiều nhất
  - Đưa ra gợi ý giảm chi tiêu trong danh mục đó

- **Dự đoán chi tiêu:**
  - Dựa trên lịch sử, dự đoán chi tiêu cuối tháng

*Lưu ý: Tính năng AI có thể triển khai ở giai đoạn sau, MVP tập trung vào CRUD và báo cáo cơ bản*

---

## 3. Cấu trúc dữ liệu (Models)

```python
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Danh mục thu/chi (ví dụ: Ăn uống, Xăng xe, Lương)."""

    CATEGORY_TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]

    name = models.CharField(max_length=100, verbose_name='Tên danh mục')
    icon = models.CharField(
        max_length=10,
        default='⚡',
        verbose_name='Icon (emoji)'
    )
    type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPE_CHOICES,
        verbose_name='Loại'
    )
    color = models.CharField(
        max_length=7,
        default='#22c55e',
        verbose_name='Màu sắc (hex)',
        help_text='Ví dụ: #22c55e'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.icon} {self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    """Giao dịch thu/chi của người dùng."""

    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Người dùng'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Danh mục'
    )
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Loại giao dịch'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Số tiền'
    )
    date = models.DateField(verbose_name='Ngày giao dịch')
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name='Ghi chú'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Giao dịch'
        verbose_name_plural = 'Giao dịch'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'type']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} VND - {self.date}"

    def save(self, *args, **kwargs):
        """Đảm bảo type của transaction khớp với type của category."""
        if self.category and self.category.type != self.type:
            raise ValueError(
                f"Category type ({self.category.type}) must match "
                f"transaction type ({self.type})"
            )
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """Thông tin mở rộng của người dùng."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Người dùng'
    )
    display_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Tên hiển thị'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Ảnh đại diện'
    )
    monthly_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Ngân sách tháng',
        help_text='Giới hạn chi tiêu hàng tháng'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hồ sơ người dùng'
        verbose_name_plural = 'Hồ sơ người dùng'

    def __str__(self):
        return f"Profile of {self.user.username}"
```

---

## 4. Các trang chính (Views & Templates)

### A. Authentication Pages

1. **Trang đăng ký (Register)** - `/register/`
   - Form đăng ký với username, email, password, confirm password
   - Validation và tạo user mới
   - Tự động tạo UserProfile khi user đăng ký

2. **Trang đăng nhập (Login)** - `/login/`
   - Form đăng nhập với username/email và password
   - Remember me checkbox
   - Link đến trang đăng ký

3. **Đăng xuất (Logout)** - `/logout/`
   - Redirect về trang login sau khi logout

### B. Main Application Pages

4. **Dashboard (Trang chủ)** - `/` hoặc `/dashboard/`
   - Tổng quan tài chính (tổng thu, tổng chi, số dư)
   - Biểu đồ nhanh (pie chart cho chi tiêu theo danh mục tháng này)
   - Danh sách giao dịch gần nhất (5-10 giao dịch)
   - Link nhanh: Thêm giao dịch, Xem báo cáo

5. **Danh sách giao dịch (Transactions List)** - `/transactions/`
   - Bảng hiển thị tất cả giao dịch
   - Phân trang
   - Bộ lọc: theo ngày, theo danh mục, theo loại
   - Nút: Thêm mới, Sửa, Xóa

6. **Thêm giao dịch (Add Transaction)** - `/transactions/add/`
   - Form nhập giao dịch mới
   - Chọn loại (thu/chi) → hiển thị danh mục tương ứng
   - Validation
   - Redirect về danh sách sau khi tạo thành công

7. **Sửa giao dịch (Edit Transaction)** - `/transactions/<id>/edit/`
   - Form tương tự add, đã điền sẵn thông tin
   - Chỉ user sở hữu mới truy cập được
   - Redirect về danh sách sau khi cập nhật

8. **Xóa giao dịch (Delete Transaction)** - `/transactions/<id>/delete/`
   - Trang xác nhận xóa
   - Chỉ user sở hữu mới truy cập được
   - Redirect về danh sách sau khi xóa

9. **Báo cáo & Biểu đồ (Reports)** - `/reports/`
   - Bộ lọc thời gian: Ngày, Tuần, Tháng, Năm, Tùy chỉnh
   - Thống kê tổng hợp
   - Nhiều loại biểu đồ:
     - Bar chart: Thu/Chi theo thời gian
     - Pie chart: Chi tiêu theo danh mục
     - Line chart: Xu hướng theo tháng
     - Comparison chart: So sánh các tháng

10. **Profile/Cài đặt (Profile & Settings)** - `/profile/`
    - Xem/Cập nhật thông tin cá nhân
    - Đổi mật khẩu
    - Thiết lập ngân sách tháng
    - Upload avatar

### C. Admin Pages

11. **Django Admin** - `/admin/`
    - Quản lý Categories (thêm/sửa/xóa danh mục)
    - Xem tất cả Users
    - Xem tất cả Transactions (nếu cần)

---

## 5. Luồng sử dụng

### A. Luồng đăng ký và đăng nhập

1. User truy cập trang chủ → chuyển hướng đến trang login (nếu chưa đăng nhập)
2. User click "Đăng ký" → điền form → submit
3. Hệ thống tạo User và UserProfile → chuyển đến trang login
4. User đăng nhập → chuyển đến Dashboard

### B. Luồng thêm giao dịch

1. User đã đăng nhập → click "Thêm giao dịch" từ Dashboard hoặc Transactions
2. Chọn loại giao dịch: Thu hoặc Chi
3. Hệ thống hiển thị danh sách danh mục tương ứng với loại đã chọn
4. User điền thông tin: số tiền, chọn danh mục, ngày, ghi chú
5. Submit form → Hệ thống validation → Lưu vào database
6. Hiển thị thông báo thành công → Redirect về danh sách giao dịch

### C. Luồng xem báo cáo

1. User vào trang Reports
2. Chọn khoảng thời gian muốn xem (ví dụ: Tháng này)
3. Hệ thống truy vấn database, tính toán thống kê
4. Hiển thị:
   - Tổng thu, tổng chi, số dư
   - Biểu đồ cột: Thu/Chi theo ngày
   - Biểu đồ tròn: Chi tiêu theo danh mục
   - Biểu đồ đường: Xu hướng
5. User có thể thay đổi khoảng thời gian → Cập nhật lại báo cáo

### D. Luồng quản lý danh mục (Admin)

1. Admin đăng nhập vào Django Admin
2. Vào phần "Categories"
3. Xem danh sách danh mục hiện có
4. Có thể:
   - Thêm danh mục mới (tên, icon, loại, màu)
   - Sửa danh mục hiện có
   - Xóa danh mục (nếu không có giao dịch nào sử dụng)
5. Danh mục mới sẽ hiện trong dropdown khi user tạo giao dịch

---

## 6. Yêu cầu khác

### A. UI/UX Requirements

- **Giao diện hiện đại (Modern UI):**
  - Sử dụng Bootstrap 5 cho responsive design
  - Tone màu chủ đạo: **Xanh lá (#22c55e, #16a34a, #15803d)** và **Trắng (#ffffff, #f9fafb)**
  - Màu phụ: Xám nhạt cho background (#f3f4f6), Đỏ/Cam cho chi tiêu (#ef4444)
  - Font: Inter, Roboto hoặc tương tự (clean, dễ đọc)

- **Components:**
  - Cards với shadow nhẹ cho các phần tử chính
  - Buttons với rounded corners
  - Icons sử dụng emoji hoặc Bootstrap Icons
  - Tables với striped rows và hover effects
  - Forms với labels rõ ràng và validation messages

- **Responsive:**
  - Mobile-first design
  - Hoạt động tốt trên mobile, tablet, desktop
  - Navigation menu collapse trên mobile

- **User-friendly:**
  - Feedback rõ ràng cho mọi action (toast notifications)
  - Confirmation dialogs cho các action quan trọng (xóa)
  - Loading states khi fetch data
  - Empty states khi chưa có dữ liệu

### B. Technical Requirements

- **Django 4.x:**
  - Class-Based Views cho CRUD operations
  - Forms với validation
  - Django ORM cho database operations
  - Django Admin để quản lý categories

- **PostgreSQL:**
  - Database chạy trong Docker container
  - Migrations quản lý schema changes

- **Docker Compose:**
  - Application chạy trên port **8005**
  - Database trong container riêng
  - Tất cả commands chạy qua `docker compose exec web`

- **Charts:**
  - Sử dụng Chart.js hoặc ApexCharts
  - Load data qua AJAX hoặc Django context
  - Interactive và có animation

- **Security:**
  - CSRF protection (Django default)
  - SQL injection protection (Django ORM)
  - XSS protection (Django template escaping)
  - Authentication required cho tất cả trang (trừ login/register)
  - Users chỉ thấy/sửa/xóa giao dịch của chính họ

### C. Performance Requirements

- **Query Optimization:**
  - Sử dụng `select_related()` và `prefetch_related()` cho foreign keys
  - Indexes trên các trường thường xuyên query (user, date, category)
  - Pagination cho danh sách giao dịch (20-50 items/page)

- **Caching (Optional):**
  - Cache dashboard statistics nếu có nhiều giao dịch
  - Cache categories (ít thay đổi)

### D. Code Quality Requirements

- **PEP 8 Compliance:**
  - Code style theo PEP 8
  - Docstrings cho tất cả models, views, functions
  - Type hints khuyến khích

- **Testing:**
  - Unit tests cho models (validation, methods)
  - Tests cho views (responses, permissions)
  - Tests cho forms (validation)
  - Minimum 80% test coverage
  - Chạy tests: `docker compose exec web python manage.py test`

- **Documentation:**
  - README.md với hướng dẫn setup và chạy project
  - Comments cho logic phức tạp
  - Docstrings cho functions/classes

---

## 7. Ghi chú kỹ thuật

### A. Data Seeding

- **Initial Categories:**
  - Tạo management command để seed categories ban đầu
  - Command: `docker compose exec web python manage.py seed_categories`
  - Bao gồm tất cả categories như Money Lover (11 expense + 6 income)

### B. Currency

- **Đơn vị tiền tệ:**
  - Mặc định: VND (Việt Nam Đồng)
  - Display: 1.000.000 VND (có dấu chấm phân cách nghìn)
  - Lưu database: Decimal(12, 2) để hỗ trợ số lớn và chính xác

### C. Date Handling

- **Timezone:**
  - Sử dụng timezone-aware datetimes
  - Default timezone: Asia/Ho_Chi_Minh
  - Display format: DD/MM/YYYY hoặc YYYY-MM-DD

### D. Future Enhancements

- **Phase 2 (Optional):**
  - Budgets: Thiết lập ngân sách cho từng danh mục
  - Recurring transactions: Giao dịch định kỳ (lương hàng tháng, etc.)
  - Multiple accounts: Nhiều tài khoản (ví, ngân hàng, thẻ)
  - Export: Xuất dữ liệu ra CSV/Excel
  - Import: Nhập dữ liệu từ file
  - Notifications: Email/Push notifications cho cảnh báo
  - Multi-language: Hỗ trợ tiếng Anh

- **AI Features (Phase 3):**
  - Machine learning để dự đoán chi tiêu
  - Gợi ý tiết kiệm thông minh hơn
  - Phát hiện giao dịch bất thường

### E. MVP Scope

**Tập trung vào MVP (Minimum Viable Product):**

1. ✅ Authentication (đăng ký, đăng nhập, đăng xuất)
2. ✅ CRUD Transactions với categories cố định
3. ✅ Dashboard với thống kê cơ bản
4. ✅ Reports page với 2-3 loại biểu đồ chính
5. ✅ Responsive UI với tone màu xanh lá - trắng
6. ✅ Django Admin để quản lý categories

**Có thể bỏ qua trong MVP:**
- ❌ AI suggestions (cảnh báo, gợi ý tiết kiệm)
- ❌ Avatar upload
- ❌ Monthly budget tracking
- ❌ Export/Import
- ❌ Recurring transactions

---

## 8. Definition of Done

Một feature được coi là hoàn thành khi:

1. ✅ Code đã implement đầy đủ theo specs
2. ✅ Unit tests được viết và pass (coverage >= 80%)
3. ✅ Code tuân thủ PEP 8
4. ✅ UI responsive và đúng tone màu
5. ✅ Chạy được trong Docker Compose trên port 8005
6. ✅ Không có lỗi trong console/logs
7. ✅ Migrations đã được tạo và apply thành công
8. ✅ Đã test manually các luồng chính
9. ✅ Documentation (docstrings, comments) đầy đủ

---

**Tổng kết:** Personal Finance Tracker là ứng dụng web Django giúp người dùng quản lý thu chi cá nhân với giao diện hiện đại (xanh lá - trắng), categories cố định tương tự Money Lover, và báo cáo trực quan qua biểu đồ. MVP tập trung vào CRUD transactions, dashboard, và reports cơ bản.
