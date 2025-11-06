# Kế hoạch thực hiện - Personal Finance Tracker

## 1. Tổng quan
- **Mục tiêu:** Xây dựng ứng dụng quản lý thu chi cá nhân với giao diện hiện đại (màu xanh lá + trắng)
- **Tech stack:** Django 4.x, PostgreSQL, Bootstrap 5, Chart.js, Docker

## 2. Django Apps
- `accounts`: Quản lý đăng ký, đăng nhập, profile người dùng
- `transactions`: Quản lý giao dịch thu chi, danh mục, báo cáo

## 3. Models

### Category (transactions app)
- name: CharField(100)
- icon: CharField(50) - emoji
- transaction_type: CharField(10) - choices: income/expense
- color: CharField(7) - hex color code
- created_at: DateTimeField

### Transaction (transactions app)
- user: ForeignKey -> User
- amount: DecimalField(12, 2)
- transaction_type: CharField(10) - choices: income/expense
- category: ForeignKey -> Category
- date: DateField
- note: TextField (optional)
- created_at, updated_at: DateTimeField

### Budget (transactions app - Phase 2)
- user: ForeignKey -> User
- category: ForeignKey -> Category
- amount: DecimalField(12, 2)
- month: DateField

## 4. Views & URLs

### Public views
- `/` - HomeView - Trang giới thiệu
- `/login/` - LoginView - Đăng nhập
- `/register/` - RegisterView - Đăng ký
- `/logout/` - LogoutView - Đăng xuất

### Protected views (require login)
- `/dashboard/` - DashboardView - Tổng quan thu chi
- `/transactions/` - TransactionListView - Danh sách giao dịch
- `/transactions/add/` - TransactionCreateView - Thêm giao dịch
- `/transactions/<id>/edit/` - TransactionUpdateView - Sửa giao dịch
- `/transactions/<id>/delete/` - TransactionDeleteView - Xóa giao dịch
- `/reports/` - ReportView - Báo cáo & biểu đồ
- `/profile/` - ProfileView - Hồ sơ cá nhân

## 5. Templates

### Base templates
- `base.html` - Layout chính với navbar, sidebar
- `home.html` - Landing page

### accounts/
- `login.html` - Form đăng nhập
- `register.html` - Form đăng ký
- `profile.html` - Thông tin cá nhân

### transactions/
- `dashboard.html` - Trang tổng quan
- `transaction_list.html` - Danh sách giao dịch
- `transaction_form.html` - Form thêm/sửa giao dịch
- `transaction_confirm_delete.html` - Xác nhận xóa
- `reports.html` - Báo cáo & biểu đồ

## 6. Implementation Steps

### Phase 1: Setup Project
**Tasks:**
1. Tạo Django apps: accounts, transactions
2. Cấu hình settings.py (PostgreSQL, static files, crispy forms)
3. Setup base template với Bootstrap 5 (màu xanh lá #4CAF50)
4. Cấu hình URL routing cơ bản
5. Tạo home.html landing page

**Kiểm tra:**
- [ ] Django apps được tạo thành công
- [ ] Base template hiển thị đúng với màu xanh lá
- [ ] Home page accessible tại /

---

### Phase 2: Models & Database
**Tasks:**
1. Tạo Category model với các trường cần thiết
2. Tạo Transaction model với relationships
3. Chạy makemigrations và migrate
4. Tạo data migration hoặc fixture cho categories mặc định (Money Lover style)
5. Register models trong admin.py
6. Test CRUD trong Django admin

**Kiểm tra:**
- [ ] Models được tạo đúng với đầy đủ fields
- [ ] Migrations chạy thành công
- [ ] Categories mặc định có trong database (Chi: Ăn uống, Di chuyển..., Thu: Lương, Thưởng...)
- [ ] Admin interface hoạt động tốt

---

### Phase 3: Authentication
**Tasks:**
1. Tạo forms: RegisterForm, LoginForm
2. Implement RegisterView với validation
3. Implement LoginView, LogoutView (Django built-in)
4. Tạo templates: login.html, register.html
5. Setup URL routing cho auth
6. Add password validation và error messages
7. Redirect sau login về dashboard

**Kiểm tra:**
- [ ] User có thể đăng ký tài khoản mới
- [ ] User có thể đăng nhập thành công
- [ ] User có thể đăng xuất
- [ ] Validation hoạt động (email format, password strength)
- [ ] Redirect đúng sau login/logout

---

### Phase 4: Transaction CRUD
**Tasks:**
1. Tạo TransactionForm với crispy-forms
2. Implement TransactionListView với pagination
3. Implement TransactionCreateView
4. Implement TransactionUpdateView
5. Implement TransactionDeleteView
6. Tạo templates: transaction_list.html, transaction_form.html
7. Add filters: theo loại, danh mục, ngày
8. Add sorting: mới nhất trước
9. Ensure user chỉ thấy giao dịch của mình

**Kiểm tra:**
- [ ] User có thể thêm giao dịch mới
- [ ] User có thể xem danh sách giao dịch với pagination
- [ ] User có thể sửa giao dịch của mình
- [ ] User có thể xóa giao dịch với confirmation
- [ ] Filters và sorting hoạt động đúng
- [ ] Security: User không thể xem/sửa giao dịch của người khác

---

### Phase 5: Dashboard
**Tasks:**
1. Tạo DashboardView với context data
2. Tính toán: tổng thu, tổng chi, số dư tháng hiện tại
3. Query top 5 categories chi tiêu nhiều nhất
4. Query 10 giao dịch gần nhất
5. Tạo dashboard.html với:
   - Summary cards (tổng thu, chi, số dư)
   - Biểu đồ tròn chi tiêu theo category (Chart.js)
   - Bảng giao dịch gần nhất
   - Quick add transaction form
6. Style với màu xanh lá theme

**Kiểm tra:**
- [ ] Dashboard hiển thị số liệu chính xác
- [ ] Biểu đồ tròn render đúng với data
- [ ] 10 giao dịch gần nhất hiển thị
- [ ] Quick add form hoạt động
- [ ] Responsive trên mobile

---

### Phase 6: Reports & Charts
**Tasks:**
1. Tạo ReportView với date range filter
2. Implement logic tính toán theo ngày/tuần/tháng
3. Chuẩn bị data cho các biểu đồ:
   - Biểu đồ cột: Thu vs Chi theo thời gian
   - Biểu đồ tròn: Phân bổ chi tiêu theo category
   - Biểu đồ đường: Xu hướng chi tiêu
4. Tạo reports.html với Chart.js
5. Add date range picker
6. Add export options (optional)

**Kiểm tra:**
- [ ] Report page hiển thị đúng dữ liệu theo filter
- [ ] Biểu đồ cột Thu vs Chi hoạt động
- [ ] Biểu đồ tròn phân bổ chi tiêu chính xác
- [ ] Biểu đồ đường xu hướng hiển thị đúng
- [ ] Date range picker hoạt động
- [ ] Charts responsive

---

### Phase 7: UI/UX Polish & Testing
**Tasks:**
1. Tạo custom CSS với theme xanh lá (#4CAF50)
2. Add icons (Font Awesome/Material Icons)
3. Implement toast notifications cho actions
4. Add loading states
5. Add empty states với CTA
6. Optimize forms với better UX
7. Add form validation messages
8. Test toàn bộ flow trên mobile
9. Fix responsive issues
10. Write basic unit tests

**Kiểm tra:**
- [ ] Theme xanh lá + trắng consistent
- [ ] Icons hiển thị đẹp
- [ ] Toast notifications hoạt động
- [ ] Loading states khi cần
- [ ] Empty states có CTA rõ ràng
- [ ] Forms có validation messages thân thiện
- [ ] Mobile responsive hoàn hảo
- [ ] Core tests pass

---

## Timeline Summary

- **Phase 1**: Setup Project - 1-2h
- **Phase 2**: Models & Database - 2-3h
- **Phase 3**: Authentication - 2-3h
- **Phase 4**: Transaction CRUD - 4-5h
- **Phase 5**: Dashboard - 3-4h
- **Phase 6**: Reports & Charts - 4-5h
- **Phase 7**: UI/UX Polish & Testing - 3-4h

**Total MVP: 19-26 hours**

---

## Future Enhancements (Phase 8+)

- Budget management với alerts
- AI-powered insights (OpenAI integration)
- Email notifications
- Export reports (PDF/Excel)
- Recurring transactions
- Multiple wallets
- Mobile app
- Social sharing

---

## Technical Notes

### Dependencies cần install:
```
Django==4.2
psycopg2-binary==2.9
django-crispy-forms==2.0
crispy-bootstrap5==0.7
python-dotenv==1.0
Pillow==10.0
```

### Chart.js setup:
- Thêm Chart.js CDN vào base.html
- Tạo charts.js file cho custom configurations
- Pass data từ Django context dạng JSON

### Color scheme:
- Primary: #4CAF50 (xanh lá)
- Primary hover: #45A049
- Secondary: #FFFFFF (trắng)
- Text: #333333, #666666
- Background: #F5F5F5
- Success: #4CAF50
- Danger: #F44336
- Warning: #FF9800

### Security checklist:
- ✅ CSRF protection
- ✅ Password hashing
- ✅ Login required decorators
- ✅ User isolation (chỉ xem data của mình)
- ✅ Input validation
- ✅ SQL injection protection (Django ORM)
