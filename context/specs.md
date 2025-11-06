# Personal Finance Tracker - Ứng dụng Theo dõi Chi tiêu Cá nhân

---

## 1. Tổng quan dự án

- **Tên ứng dụng:** Personal Finance Tracker
- **Mục tiêu:** Giúp người dùng quản lý thu chi cá nhân hiệu quả, theo dõi chi tiêu hàng ngày và nhận được gợi ý tiết kiệm thông minh
- **Công nghệ sử dụng:** 
  - Backend: Django 4.x
  - Database: PostgreSQL (via Docker)
  - Frontend: Bootstrap 5, Chart.js (biểu đồ)
  - AI: OpenAI API hoặc tương tự (cho gợi ý thông minh)
  - Deployment: Docker, Docker Compose

---

## 2. Tính năng chính

### A. Quản lý người dùng

- **Đăng ký tài khoản:**
  - Email, mật khẩu, họ tên
  - Xác thực email (optional)
  
- **Đăng nhập:**
  - Email/Username và mật khẩu
  - Remember me option
  - Đăng xuất

### B. Quản lý thu chi (CRUD)

- **Thêm khoản thu/chi:**
  - Số tiền (required)
  - Loại giao dịch: Thu hoặc Chi (required)
  - Danh mục (Category) - chọn từ danh sách có sẵn (required)
  - Ngày giao dịch (mặc định là hôm nay)
  - Ghi chú (optional)
  
- **Xem danh sách giao dịch:**
  - Hiển thị dạng bảng với phân trang
  - Lọc theo: loại (thu/chi), danh mục, khoảng thời gian
  - Sắp xếp theo ngày (mới nhất trước)
  
- **Sửa giao dịch:**
  - Cho phép chỉnh sửa tất cả các trường
  
- **Xóa giao dịch:**
  - Có xác nhận trước khi xóa

### C. Danh mục (Categories)

**Danh mục Chi tiêu (tham khảo Money Lover):**
- 🍔 Ăn uống
- 🚗 Di chuyển & Xăng xe
- 🏠 Nhà cửa & Sinh hoạt
- 🎬 Giải trí
- 👕 Mua sắm
- 💊 Sức khỏe
- 📚 Giáo dục
- 👨‍👩‍👧 Gia đình & Con cái
- 💝 Quà tặng & Quyên góp
- 💼 Công việc
- 📱 Điện thoại & Internet
- ✈️ Du lịch
- 💰 Khác

**Danh mục Thu nhập:**
- 💵 Lương
- 💼 Thưởng
- 🎁 Quà tặng
- 📈 Đầu tư
- 💰 Thu nhập khác

**Quản lý:**
- Admin có thể thêm/sửa/xóa danh mục
- User chỉ được chọn từ danh sách có sẵn

### D. Tổng hợp & Thống kê

- **Dashboard tổng quan:**
  - Tổng thu, tổng chi, số dư trong tháng hiện tại
  - Top 5 danh mục chi tiêu nhiều nhất
  - Xu hướng chi tiêu so với tháng trước
  
- **Báo cáo theo thời gian:**
  - Xem theo ngày (hôm nay, hôm qua)
  - Xem theo tuần
  - Xem theo tháng
  - Xem theo khoảng thời gian tùy chọn
  
- **Biểu đồ trực quan:**
  - Biểu đồ cột: Thu vs Chi theo ngày/tháng
  - Biểu đồ tròn: Phân bổ chi tiêu theo danh mục
  - Biểu đồ đường: Xu hướng chi tiêu theo thời gian
  - Biểu đồ thanh: So sánh chi tiêu các tháng

### E. Tính năng AI (Future Enhancement)

- **Gợi ý tiết kiệm:**
  - Phân tích thói quen chi tiêu
  - Đưa ra lời khuyên dựa trên dữ liệu
  
- **Cảnh báo vượt mức:**
  - Thiết lập ngân sách cho từng danh mục
  - Thông báo khi sắp vượt ngân sách
  - Cảnh báo chi tiêu bất thường

---

## 3. Cấu trúc dữ liệu (Models)

```python
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Danh mục thu chi."""
    
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon (emoji)")
    transaction_type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="Loại giao dịch"
    )
    color = models.CharField(max_length=7, default="#4CAF50", verbose_name="Màu sắc")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['transaction_type', 'name']
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class Transaction(models.Model):
    """Giao dịch thu chi."""
    
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Người dùng"
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Số tiền"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="Loại giao dịch"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name="Danh mục"
    )
    date = models.DateField(default=timezone.now, verbose_name="Ngày giao dịch")
    note = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Giao dịch"
        verbose_name_plural = "Giao dịch"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'transaction_type']),
        ]
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount:,} VNĐ - {self.date}"


class Budget(models.Model):
    """Ngân sách cho từng danh mục (Optional - Phase 2)."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.DateField(verbose_name="Tháng")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ngân sách"
        verbose_name_plural = "Ngân sách"
        unique_together = ['user', 'category', 'month']
    
    def __str__(self):
        return f"{self.category.name} - {self.amount:,} VNĐ - {self.month.strftime('%m/%Y')}"
```

---

## 4. Các trang chính (Views & Templates)

### Trang công khai (không cần đăng nhập)
- **Trang chủ (`/`)**: Giới thiệu ứng dụng, call-to-action đăng ký/đăng nhập
- **Đăng nhập (`/login/`)**: Form đăng nhập
- **Đăng ký (`/register/`)**: Form đăng ký tài khoản mới

### Trang yêu cầu đăng nhập
- **Dashboard (`/dashboard/`)**: 
  - Tổng quan thu chi tháng hiện tại
  - Biểu đồ tròn chi tiêu theo danh mục
  - Danh sách 10 giao dịch gần nhất
  - Quick actions: Thêm thu/chi nhanh
  
- **Danh sách giao dịch (`/transactions/`)**: 
  - Bảng hiển thị tất cả giao dịch
  - Bộ lọc và tìm kiếm
  - Nút thêm mới, sửa, xóa
  
- **Thêm giao dịch (`/transactions/add/`)**: Form thêm mới
- **Sửa giao dịch (`/transactions/<id>/edit/`)**: Form chỉnh sửa
- **Xóa giao dịch (`/transactions/<id>/delete/`)**: Xác nhận xóa

- **Báo cáo (`/reports/`)**: 
  - Chọn khoảng thời gian
  - Hiển thị biểu đồ:
    - Biểu đồ cột thu chi theo ngày
    - Biểu đồ tròn phân bổ chi tiêu
    - Biểu đồ đường xu hướng
  - Bảng thống kê chi tiết

- **Hồ sơ (`/profile/`)**: Xem/sửa thông tin cá nhân, đổi mật khẩu

---

## 5. Luồng sử dụng

### Luồng đăng ký và bắt đầu
1. User truy cập trang chủ
2. Nhấn "Đăng ký" → Điền form đăng ký
3. Sau khi đăng ký thành công → Tự động đăng nhập
4. Chuyển đến Dashboard (lần đầu sẽ trống)
5. Hướng dẫn thêm giao dịch đầu tiên

### Luồng thêm giao dịch
1. Từ Dashboard hoặc menu, nhấn "Thêm giao dịch"
2. Chọn loại: Thu hoặc Chi
3. Nhập số tiền
4. Chọn danh mục (danh sách phụ thuộc vào loại đã chọn)
5. Chọn ngày (mặc định hôm nay)
6. Thêm ghi chú (tùy chọn)
7. Nhấn "Lưu" → Quay về Dashboard với thông báo thành công

### Luồng xem báo cáo
1. Từ menu, chọn "Báo cáo"
2. Chọn khoảng thời gian (hoặc dùng preset: tuần này, tháng này)
3. Xem các biểu đồ và thống kê
4. Có thể export dữ liệu (PDF/Excel - optional)

### Luồng quản lý giao dịch
1. Từ menu, chọn "Giao dịch"
2. Xem danh sách tất cả giao dịch
3. Sử dụng bộ lọc để tìm giao dịch cụ thể
4. Nhấn "Sửa" để chỉnh sửa hoặc "Xóa" để xóa
5. Xác nhận thay đổi

---

## 6. Yêu cầu khác

### Giao diện (UI/UX)
- **Tone màu chủ đạo:**
  - Primary: Xanh lá (#4CAF50)
  - Secondary: Trắng (#FFFFFF)
  - Accent: Xanh đậm hơn cho hover/active states
  - Text: Đen (#333333) và xám (#666666)
  
- **Thiết kế:**
  - Modern, clean, minimal
  - Responsive (mobile-first)
  - Sử dụng Bootstrap 5 components
  - Icons: Font Awesome hoặc Material Icons
  - Smooth transitions và animations

- **Trải nghiệm:**
  - Navigation rõ ràng với sidebar/menu
  - Form validation thân thiện
  - Toast notifications cho actions
  - Loading states cho async operations
  - Empty states với call-to-action

### Hiệu năng
- Pagination cho danh sách giao dịch (20 items/page)
- Lazy loading cho biểu đồ
- Cache dashboard data (5 phút)
- Optimize database queries (select_related, prefetch_related)

### Bảo mật
- CSRF protection (Django default)
- Password hashing (Django default)
- Login required decorators cho protected views
- User chỉ xem được giao dịch của mình
- Input validation và sanitization

### Code Quality
- Follow PEP 8 (Python)
- Comments tiếng Việt cho business logic
- Docstrings cho functions/classes
- Unit tests cho core functionality
- Git commit messages có ý nghĩa

### Docker & Deployment
- Dockerfile cho Django app
- docker-compose.yml với services:
  - web (Django)
  - db (PostgreSQL)
- Environment variables cho sensitive data
- Volume cho persistent data

---

## 7. Ghi chú kỹ thuật

### Phase 1 (MVP)
- ✅ Authentication (register, login, logout)
- ✅ CRUD Transactions
- ✅ Dashboard với thống kê cơ bản
- ✅ Biểu đồ cơ bản (Chart.js)
- ✅ Pre-defined Categories
- ✅ Responsive UI với tone màu xanh lá

### Phase 2 (Future Enhancements)
- 🔲 Budget management
- 🔲 AI-powered insights và suggestions
- 🔲 Export reports (PDF, Excel)
- 🔲 Email notifications
- 🔲 Multiple wallets/accounts
- 🔲 Recurring transactions
- 🔲 Mobile app (React Native)

### Dependencies chính
```
Django==4.2
psycopg2-binary==2.9
django-crispy-forms==2.0
crispy-bootstrap5==0.7
python-dotenv==1.0
Pillow==10.0
```

### Biểu đồ (Chart.js)
- CDN hoặc npm install
- Sử dụng trong template với data từ Django context
- Types: Line, Bar, Pie, Doughnut

### API Structure (Optional for future mobile app)
```
/api/v1/transactions/          # List, Create
/api/v1/transactions/<id>/     # Retrieve, Update, Delete
/api/v1/categories/            # List
/api/v1/reports/summary/       # Dashboard data
/api/v1/reports/chart-data/    # Chart data
```

---

## 8. Cấu trúc thư mục đề xuất

```
app/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                  # App quản lý user
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── transactions/              # App chính
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templatetags/
│       └── transaction_extras.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── charts.js
│   └── images/
└── templates/
    ├── base.html
    ├── home.html
    ├── accounts/
    │   ├── login.html
    │   └── register.html
    └── transactions/
        ├── dashboard.html
        ├── transaction_list.html
        ├── transaction_form.html
        └── reports.html
```

---

## 9. Sample Data

**Categories mặc định** (sẽ tạo bằng migration hoặc fixture):

```python
# Chi tiêu
['🍔 Ăn uống', '🚗 Di chuyển & Xăng xe', '🏠 Nhà cửa & Sinh hoạt', 
 '🎬 Giải trí', '👕 Mua sắm', '💊 Sức khỏe', '📚 Giáo dục',
 '👨‍👩‍👧 Gia đình & Con cái', '💝 Quà tặng & Quyên góp', '💼 Công việc',
 '📱 Điện thoại & Internet', '✈️ Du lịch', '💰 Chi tiêu khác']

# Thu nhập
['💵 Lương', '💼 Thưởng', '🎁 Quà tặng', '📈 Đầu tư', '💰 Thu nhập khác']
```

---

**Kết thúc Specification**

Spec này cung cấp đầy đủ thông tin để developer bắt đầu implement Personal Finance Tracker. Có thể điều chỉnh và bổ sung theo nhu cầu thực tế trong quá trình phát triển.
