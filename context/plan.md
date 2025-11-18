# Kế hoạch Triển khai - Personal Finance Tracker

## 1. Tổng quan

**Mục tiêu:** Xây dựng ứng dụng web Django để theo dõi và quản lý thu chi cá nhân với giao diện hiện đại, hỗ trợ báo cáo trực quan.

**Tech Stack:**
- Backend: Django 4.x
- Database: PostgreSQL 15 (Docker)
- Frontend: Bootstrap 5, Chart.js
- Deployment: Docker Compose (port 8005)
- Tone màu: Xanh lá (#22c55e) và Trắng

**Phạm vi MVP:**
- Authentication (đăng ký, đăng nhập, profile)
- CRUD Transactions với categories cố định
- Dashboard với thống kê tổng quan
- Reports với biểu đồ trực quan
- Admin panel quản lý categories

---

## 2. Cấu trúc Django Apps

### `accounts` - Quản lý người dùng
- Authentication (đăng ký, đăng nhập, đăng xuất)
- User profile management
- Đổi mật khẩu

### `transactions` - Quản lý giao dịch
- CRUD operations cho transactions
- Filtering và pagination
- Category management

### `reports` - Báo cáo và thống kê
- Dashboard tổng quan
- Charts và analytics
- Time-based filtering

---

## 3. Models

### UserProfile (app: accounts)
```
- user: OneToOneField(User, CASCADE, related_name='profile')
- display_name: CharField(max_length=100, blank=True)
- avatar: ImageField(upload_to='avatars/', blank=True, null=True)
- monthly_budget: DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)
```

### Category (app: transactions)
```
- name: CharField(max_length=100)
- icon: CharField(max_length=10, default='⚡')
- type: CharField(max_length=10, choices=[('income', 'Thu nhập'), ('expense', 'Chi tiêu')])
- color: CharField(max_length=7, default='#22c55e')
- created_at: DateTimeField(auto_now_add=True)
```

### Transaction (app: transactions)
```
- user: ForeignKey(User, CASCADE, related_name='transactions')
- category: ForeignKey(Category, PROTECT, related_name='transactions')
- type: CharField(max_length=10, choices=[('income', 'Thu nhập'), ('expense', 'Chi tiêu')])
- amount: DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
- date: DateField()
- note: TextField(blank=True, null=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)
- Meta: indexes trên [user, date], [user, type], [category]
```

---

## 4. Views & URLs

### Authentication (app: accounts)
- `/register/` - RegisterView - Đăng ký tài khoản mới
- `/login/` - LoginView - Đăng nhập
- `/logout/` - LogoutView - Đăng xuất
- `/profile/` - ProfileView - Xem/cập nhật profile
- `/profile/password/` - PasswordChangeView - Đổi mật khẩu

### Transactions (app: transactions)
- `/transactions/` - TransactionListView - Danh sách giao dịch (paginated, filtered)
- `/transactions/add/` - TransactionCreateView - Thêm giao dịch mới
- `/transactions/<id>/edit/` - TransactionUpdateView - Sửa giao dịch
- `/transactions/<id>/delete/` - TransactionDeleteView - Xóa giao dịch
- `/api/categories/<type>/` - CategoryAPIView - Lấy categories theo type (AJAX)

### Reports & Dashboard (app: reports)
- `/` hoặc `/dashboard/` - DashboardView - Trang chủ với thống kê tổng quan
- `/reports/` - ReportsView - Báo cáo chi tiết với biểu đồ
- `/api/chart-data/` - ChartDataAPIView - API trả data cho charts (JSON)

### Admin
- `/admin/` - Django Admin - Quản lý Categories, Users, Transactions

---

## 5. Templates

### Base Templates
- `base.html` - Template gốc với navbar, footer, Bootstrap 5
- `includes/navbar.html` - Navigation bar với user menu
- `includes/messages.html` - Toast notifications

### Accounts Templates
- `accounts/register.html` - Form đăng ký
- `accounts/login.html` - Form đăng nhập
- `accounts/profile.html` - Thông tin profile
- `accounts/password_change.html` - Form đổi mật khẩu

### Transactions Templates
- `transactions/transaction_list.html` - Bảng danh sách giao dịch với filters
- `transactions/transaction_form.html` - Form thêm/sửa giao dịch
- `transactions/transaction_confirm_delete.html` - Xác nhận xóa

### Reports Templates
- `reports/dashboard.html` - Dashboard tổng quan
- `reports/reports.html` - Trang báo cáo với charts
- `reports/includes/stats_cards.html` - Cards hiển thị thống kê
- `reports/includes/charts.html` - Container cho biểu đồ

---

## 6. Các Bước Triển Khai

### Phase 1: Khởi tạo Project và Apps
**Mục tiêu:** Thiết lập cấu trúc project cơ bản và các Django apps

**Các task:**
1. Tạo các Django apps cần thiết
   ```bash
   docker compose exec web python manage.py startapp accounts
   docker compose exec web python manage.py startapp transactions
   docker compose exec web python manage.py startapp reports
   ```
2. Đăng ký apps vào `INSTALLED_APPS` trong settings
3. Cấu hình settings:
   - Timezone: `Asia/Ho_Chi_Minh`
   - Language: `vi`
   - Static files và media files
   - Authentication URLs
4. Tạo cấu trúc thư mục templates và static
5. Tạo `base.html` template với Bootstrap 5 CDN
6. Cấu hình URL routing cơ bản

**Kiểm tra:**
- [ ] 3 apps được tạo và đăng ký thành công
- [ ] Docker containers chạy trên port 8005
- [ ] Base template render được
- [ ] Settings đã cấu hình đúng timezone và language

**Thời gian ước tính:** 1-2 giờ

---

### Phase 2: Xây dựng Models và Migrations
**Mục tiêu:** Tạo database schema cho toàn bộ ứng dụng

**Các task:**
1. Tạo model `Category` trong `transactions/models.py`
   - Các trường: name, icon, type, color, created_at
   - Method `__str__` và Meta class
2. Tạo model `Transaction` trong `transactions/models.py`
   - Các trường: user, category, type, amount, date, note, timestamps
   - Custom `save()` method để validate category type
   - Indexes cho performance
3. Tạo model `UserProfile` trong `accounts/models.py`
   - OneToOne với User
   - Các trường: display_name, avatar, monthly_budget, timestamps
4. Tạo signals để auto-create UserProfile khi User đăng ký
5. Generate và apply migrations
   ```bash
   docker compose exec web python manage.py makemigrations
   docker compose exec web python manage.py migrate
   ```
6. Đăng ký models vào Django Admin
7. Tạo management command `seed_categories` để populate categories ban đầu
8. Viết unit tests cho models

**Kiểm tra:**
- [ ] Tất cả models được tạo đúng specs
- [ ] Migrations generated và applied thành công
- [ ] Models hiển thị trong Django Admin
- [ ] Command `seed_categories` chạy được và tạo đủ 17 categories
- [ ] Model tests pass với coverage >= 80%

**Thời gian ước tính:** 3-4 giờ

---

### Phase 3: Authentication System
**Mục tiêu:** Xây dựng hệ thống đăng ký, đăng nhập và quản lý profile

**Các task:**
1. Tạo forms:
   - `UserRegistrationForm` với validation
   - `UserProfileForm` để cập nhật profile
   - `CustomAuthenticationForm`
2. Tạo views:
   - `RegisterView` (CreateView)
   - `LoginView` (Django built-in)
   - `LogoutView` (Django built-in)
   - `ProfileView` (UpdateView)
   - `PasswordChangeView` (Django built-in)
3. Cấu hình URLs cho accounts app
4. Tạo templates:
   - `register.html` với form Bootstrap
   - `login.html` với remember me checkbox
   - `profile.html` với form cập nhật
   - `password_change.html`
5. Implement signal để auto-create UserProfile khi User mới đăng ký
6. Thêm `@login_required` decorator
7. Viết tests cho authentication flow

**Kiểm tra:**
- [ ] User có thể đăng ký tài khoản mới
- [ ] UserProfile được tạo tự động
- [ ] Đăng nhập/đăng xuất hoạt động đúng
- [ ] Profile có thể cập nhật được
- [ ] Đổi mật khẩu thành công
- [ ] Redirect đúng sau mỗi action
- [ ] Auth tests pass với coverage >= 80%

**Thời gian ước tính:** 3-4 giờ

---

### Phase 4: Transaction CRUD Operations
**Mục tiêu:** Xây dựng chức năng quản lý giao dịch đầy đủ

**Các task:**
1. Tạo forms:
   - `TransactionForm` với dynamic category filtering theo type
   - Custom validation cho amount (phải > 0)
2. Tạo views:
   - `TransactionListView` (ListView) với pagination và filtering
   - `TransactionCreateView` (CreateView)
   - `TransactionUpdateView` (UpdateView) với permission check
   - `TransactionDeleteView` (DeleteView) với permission check
3. Implement filtering:
   - Theo date range
   - Theo category
   - Theo type (income/expense)
4. Cấu hình URLs cho transactions app
5. Tạo templates:
   - `transaction_list.html` với bảng responsive và filters
   - `transaction_form.html` với AJAX category loading
   - `transaction_confirm_delete.html`
6. Thêm JavaScript cho dynamic category dropdown
7. Implement pagination (20 items/page)
8. Viết tests cho CRUD operations và permissions

**Kiểm tra:**
- [ ] Thêm giao dịch mới thành công
- [ ] Category dropdown filter theo type đúng
- [ ] Danh sách giao dịch hiển thị đúng với pagination
- [ ] Filters hoạt động chính xác
- [ ] Chỉ owner mới sửa/xóa được giao dịch
- [ ] Validation hoạt động (amount > 0, category type match)
- [ ] Transaction tests pass với coverage >= 80%

**Thời gian ước tính:** 4-5 giờ

---

### Phase 5: Dashboard và Reports
**Mục tiêu:** Xây dựng dashboard và trang báo cáo với biểu đồ

**Các task:**
1. Tạo `DashboardView`:
   - Query thống kê: tổng thu, tổng chi, số dư tháng hiện tại
   - 5-10 giao dịch gần nhất
   - Data cho mini pie chart
2. Tạo `ReportsView`:
   - Time range selector (ngày, tuần, tháng, năm, custom)
   - Query data theo time range
   - Tính toán statistics
3. Tạo API views cho chart data:
   - `ChartDataAPIView` trả JSON cho:
     - Bar chart: Thu/Chi theo ngày
     - Pie chart: Chi tiêu theo category
     - Line chart: Xu hướng theo tháng
4. Cấu hình URLs cho reports app
5. Tạo templates:
   - `dashboard.html` với stats cards và quick actions
   - `reports.html` với time filters và chart containers
6. Integrate Chart.js:
   - Bar chart với 2 datasets (income/expense)
   - Pie chart với màu theo category
   - Line chart theo tháng
7. Optimize queries với `select_related` và `prefetch_related`
8. Thêm empty states khi chưa có data
9. Viết tests cho views và data calculations

**Kiểm tra:**
- [ ] Dashboard hiển thị stats đúng
- [ ] Charts render và load data thành công
- [ ] Time filters hoạt động chính xác
- [ ] Data calculations chính xác
- [ ] Performance tốt với nhiều transactions
- [ ] Empty states hiển thị đúng
- [ ] Reports tests pass với coverage >= 80%

**Thời gian ước tính:** 5-6 giờ

---

### Phase 6: UI/UX và Styling
**Mục tiêu:** Hoàn thiện giao diện với tone màu xanh lá - trắng

**Các task:**
1. Tạo custom CSS file với color scheme:
   - Primary: #22c55e, #16a34a, #15803d
   - Background: #f9fafb, #f3f4f6
   - Expense color: #ef4444
2. Styling cho tất cả components:
   - Cards với shadow và rounded corners
   - Buttons với hover effects
   - Tables với striped rows
   - Forms với clear labels
3. Implement responsive navbar:
   - Logo và brand name
   - User dropdown menu
   - Collapse menu cho mobile
4. Thêm toast notifications cho user feedback:
   - Success messages (màu xanh)
   - Error messages (màu đỏ)
   - Warning messages (màu vàng)
5. Implement loading states và spinners
6. Thêm confirmation modals cho delete actions
7. Icons sử dụng Bootstrap Icons hoặc emoji
8. Test responsive trên mobile, tablet, desktop
9. Optimize CSS và remove unused styles

**Kiểm tra:**
- [ ] Toàn bộ UI đúng tone màu xanh lá - trắng
- [ ] Responsive tốt trên tất cả devices
- [ ] Toast notifications hiển thị đúng
- [ ] Loading states hoạt động
- [ ] Confirmation dialogs xuất hiện khi xóa
- [ ] Không có lỗi CSS trong console
- [ ] UI/UX thân thiện và dễ sử dụng

**Thời gian ước tính:** 3-4 giờ

---

### Phase 7: Testing và Quality Assurance
**Mục tiêu:** Đảm bảo code quality và test coverage >= 80%

**Các task:**
1. Viết comprehensive tests:
   - Model tests: validation, methods, signals
   - View tests: responses, permissions, redirects
   - Form tests: validation, cleaning
   - Integration tests: complete user flows
2. Run tests và check coverage:
   ```bash
   docker compose exec web python manage.py test
   docker compose exec web coverage run --source='.' manage.py test
   docker compose exec web coverage report
   ```
3. Code review và refactoring:
   - Follow PEP 8 strictly
   - Add docstrings và type hints
   - Remove code duplication
4. Test edge cases:
   - Empty database
   - Invalid inputs
   - Permission violations
   - Concurrent requests
5. Performance testing:
   - Query optimization
   - N+1 query check
   - Load testing với nhiều transactions
6. Security audit:
   - CSRF protection
   - SQL injection prevention
   - XSS protection
   - Permission checks

**Kiểm tra:**
- [ ] Tất cả tests pass
- [ ] Test coverage >= 80%
- [ ] Không có PEP 8 violations
- [ ] Docstrings đầy đủ
- [ ] Không có N+1 queries
- [ ] Security checks pass
- [ ] Edge cases được handle đúng

**Thời gian ước tính:** 4-5 giờ

---

### Phase 8: Polish và Deployment Preparation
**Mục tiêu:** Hoàn thiện và chuẩn bị deploy

**Các task:**
1. Tạo superuser và seed initial data:
   ```bash
   docker compose exec web python manage.py createsuperuser
   docker compose exec web python manage.py seed_categories
   ```
2. Kiểm tra Django Admin:
   - Customize admin cho Category, Transaction, UserProfile
   - Add list filters và search fields
   - Inline editing nếu cần
3. Error handling:
   - Custom 404 page
   - Custom 500 page
   - Graceful error messages
4. Logging configuration:
   - Configure Django logging
   - Log errors và warnings
5. Environment variables:
   - Move sensitive data to .env
   - SECRET_KEY, DATABASE_URL, DEBUG
6. Documentation:
   - README.md với setup instructions
   - API documentation nếu có
   - Code comments cho logic phức tạp
7. Final manual testing:
   - Test toàn bộ user flows
   - Test trên nhiều browsers
   - Test error scenarios
8. Performance optimization:
   - Enable database indexes
   - Optimize static files
   - Check query performance

**Kiểm tra:**
- [ ] Django Admin hoạt động tốt
- [ ] Error pages hiển thị đúng
- [ ] Logging hoạt động
- [ ] Environment variables đã setup
- [ ] README.md đầy đủ
- [ ] Manual testing pass tất cả flows
- [ ] Performance acceptable
- [ ] Sẵn sàng để deploy

**Thời gian ước tính:** 2-3 giờ

---

## 7. Timeline Tổng hợp

| Phase | Nội dung | Thời gian ước tính |
|-------|----------|-------------------|
| Phase 1 | Khởi tạo Project và Apps | 1-2 giờ |
| Phase 2 | Models và Migrations | 3-4 giờ |
| Phase 3 | Authentication System | 3-4 giờ |
| Phase 4 | Transaction CRUD | 4-5 giờ |
| Phase 5 | Dashboard và Reports | 5-6 giờ |
| Phase 6 | UI/UX và Styling | 3-4 giờ |
| Phase 7 | Testing và QA | 4-5 giờ |
| Phase 8 | Polish và Deployment Prep | 2-3 giờ |
| **TỔNG** | **MVP hoàn chỉnh** | **25-33 giờ** |

---

## 8. Phụ thuộc giữa các Phase

```
Phase 1 (Setup)
    ↓
Phase 2 (Models) ← Cần hoàn thành trước khi làm Phase 3, 4, 5
    ↓
Phase 3 (Auth) ← Có thể làm song song với Phase 4
    ↓
Phase 4 (Transactions) ← Cần hoàn thành trước Phase 5
    ↓
Phase 5 (Reports) ← Cần Transaction data
    ↓
Phase 6 (UI/UX) ← Có thể làm song song với Phase 7
    ↓
Phase 7 (Testing) ← Test tất cả phases trước
    ↓
Phase 8 (Polish) ← Finalize mọi thứ
```

---

## 9. Checklist Hoàn thành MVP

### Functionality
- [ ] User có thể đăng ký và đăng nhập
- [ ] User có thể thêm/sửa/xóa giao dịch
- [ ] Categories được seed sẵn (17 categories)
- [ ] Dashboard hiển thị thống kê tổng quan
- [ ] Reports page với 3 loại biểu đồ chính
- [ ] Filtering và pagination hoạt động
- [ ] Admin có thể quản lý categories

### Technical
- [ ] Chạy được trên Docker Compose port 8005
- [ ] PostgreSQL database hoạt động
- [ ] Migrations đã apply đầy đủ
- [ ] Test coverage >= 80%
- [ ] PEP 8 compliant
- [ ] No console errors

### UI/UX
- [ ] Responsive trên mobile/tablet/desktop
- [ ] Tone màu xanh lá - trắng đúng specs
- [ ] Toast notifications cho user feedback
- [ ] Loading states và empty states
- [ ] Confirmation dialogs cho delete actions

### Security
- [ ] CSRF protection enabled
- [ ] SQL injection prevention (Django ORM)
- [ ] XSS protection (template escaping)
- [ ] Permission checks (user chỉ thấy data của mình)
- [ ] Sensitive data trong .env

---

## 10. Ghi chú quan trọng

### Commands thường dùng

```bash
# Start application
docker compose up

# Create migrations
docker compose exec web python manage.py makemigrations

# Apply migrations
docker compose exec web python manage.py migrate

# Seed categories
docker compose exec web python manage.py seed_categories

# Create superuser
docker compose exec web python manage.py createsuperuser

# Run tests
docker compose exec web python manage.py test

# Run tests with coverage
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report

# Django shell
docker compose exec web python manage.py shell

# Access container shell
docker compose exec web bash
```

### Best Practices cần tuân thủ

1. **ALWAYS** run commands via Docker Compose
2. **NEVER** create migrations manually
3. **ALWAYS** write tests before implementation (TDD)
4. **ALWAYS** follow PEP 8
5. **ALWAYS** add docstrings và type hints
6. **ALWAYS** check permissions (user chỉ thấy data của mình)
7. **ALWAYS** validate user input
8. **ALWAYS** use Django ORM (không raw SQL)

### Categories cần seed

**Expense Categories (11):**
- 🍔 Ăn uống (Food & Beverage) - #ef4444
- 🚗 Xăng xe (Transportation) - #f97316
- 🏠 Nhà cửa (Housing) - #eab308
- 👕 Mua sắm (Shopping) - #ec4899
- 💊 Y tế (Healthcare) - #06b6d4
- 📚 Giáo dục (Education) - #8b5cf6
- 🎬 Giải trí (Entertainment) - #f43f5e
- 📱 Điện thoại/Internet (Bills) - #10b981
- 👨‍👩‍👧 Gia đình (Family) - #f59e0b
- 🎁 Quà tặng (Gifts) - #ec4899
- ⚡ Khác (Other) - #6b7280

**Income Categories (6):**
- 💰 Lương (Salary) - #22c55e
- 💼 Thưởng (Bonus) - #16a34a
- 📈 Đầu tư (Investment) - #15803d
- 🎯 Thu nhập phụ (Side Income) - #10b981
- 🎁 Quà tặng (Gifts) - #14b8a6
- ⚡ Khác (Other) - #22c55e

---

**Kế hoạch này sẽ được sử dụng làm blueprint cho việc triển khai Personal Finance Tracker MVP.**
