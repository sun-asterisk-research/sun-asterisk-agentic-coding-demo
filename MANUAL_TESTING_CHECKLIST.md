# Manual Testing Checklist - Personal Finance Tracker

## Test Environment Setup
- [ ] Application running on http://localhost:8005
- [ ] Database seeded with categories
- [ ] Superuser account created (admin/admin)

## 1. User Registration and Login

### Registration
- [ ] Navigate to registration page
- [ ] Register with valid credentials
- [ ] Verify password strength validation
- [ ] Verify email format validation
- [ ] Verify username uniqueness check
- [ ] Check automatic UserProfile creation
- [ ] Verify redirect to dashboard after registration

### Login
- [ ] Login with valid credentials
- [ ] Verify redirect to dashboard
- [ ] Test "Remember me" functionality
- [ ] Test invalid credentials error message
- [ ] Verify logout functionality

## 2. User Profile Management

### View Profile
- [ ] Navigate to profile page
- [ ] Verify user information displayed correctly
- [ ] Check display name and monthly budget fields

### Edit Profile
- [ ] Update display name
- [ ] Update monthly budget
- [ ] Save changes successfully
- [ ] Verify changes reflected on dashboard
- [ ] Test validation for negative budget

## 3. Transaction Management

### Create Transaction
- [ ] Navigate to "Add Transaction" page
- [ ] Create income transaction
  - [ ] Select category
  - [ ] Enter amount (positive decimal)
  - [ ] Select date
  - [ ] Add note (optional)
  - [ ] Submit successfully
- [ ] Create expense transaction
  - [ ] Select category
  - [ ] Enter amount
  - [ ] Select date
  - [ ] Add note
  - [ ] Submit successfully
- [ ] Test validation:
  - [ ] Amount cannot be zero or negative
  - [ ] Category is required
  - [ ] Date is required
  - [ ] Type is required

### View Transactions
- [ ] Navigate to transaction list
- [ ] Verify all transactions displayed
- [ ] Check pagination (if >20 transactions)
- [ ] Verify transaction details shown correctly

### Filter Transactions
- [ ] Filter by date range (from/to)
- [ ] Filter by category
- [ ] Filter by type (income/expense)
- [ ] Combine multiple filters
- [ ] Clear filters
- [ ] Verify results update correctly

### Edit Transaction
- [ ] Click edit on a transaction
- [ ] Modify amount
- [ ] Change category
- [ ] Update date
- [ ] Edit note
- [ ] Save changes
- [ ] Verify changes reflected in list

### Delete Transaction
- [ ] Click delete on a transaction
- [ ] Verify confirmation modal appears
- [ ] Confirm deletion
- [ ] Verify transaction removed from list
- [ ] Test cancel deletion

## 4. Dashboard

### Statistics Display
- [ ] Verify current month statistics shown:
  - [ ] Total income
  - [ ] Total expense
  - [ ] Balance (income - expense)
- [ ] Check color coding (green for positive, red for negative)
- [ ] Verify currency formatting (VND)

### Recent Transactions
- [ ] Verify recent transactions displayed (up to 10)
- [ ] Check transactions ordered by date (newest first)
- [ ] Verify transaction details:
  - [ ] Category icon and name
  - [ ] Amount with formatting
  - [ ] Date
  - [ ] Type (income/expense)

### Quick Actions
- [ ] "Add Transaction" button works
- [ ] "View All Transactions" link works
- [ ] Navigation to reports works

## 5. Reports and Analytics

### Time Range Selection
- [ ] Select "Today"
- [ ] Select "This Week"
- [ ] Select "This Month"
- [ ] Select "This Year"
- [ ] Select "Custom" with date range
- [ ] Verify statistics update for each range

### Statistics
- [ ] Verify total income for selected period
- [ ] Verify total expense for selected period
- [ ] Verify balance calculation
- [ ] Check percentage breakdown by category

### Charts

#### Bar Chart
- [ ] Verify chart loads correctly
- [ ] Check income bars (green)
- [ ] Check expense bars (red)
- [ ] Hover over bars shows details
- [ ] Chart responsive to window resize

#### Pie Chart
- [ ] Verify expense breakdown by category
- [ ] Check category colors match
- [ ] Hover shows percentage and amount
- [ ] Legend displayed correctly

#### Line Chart
- [ ] Verify monthly trend chart
- [ ] Check income line (green)
- [ ] Check expense line (red)
- [ ] Verify data points accurate
- [ ] Chart shows last 6 months by default

### Category Breakdown
- [ ] Income breakdown by category displayed
- [ ] Expense breakdown by category displayed
- [ ] Amounts formatted correctly
- [ ] Categories sorted by amount (highest first)

## 6. Responsive Design

### Desktop (>1200px)
- [ ] Layout looks professional
- [ ] All elements properly aligned
- [ ] Tables readable
- [ ] Charts display well

### Tablet (768px - 1200px)
- [ ] Navigation collapses appropriately
- [ ] Tables remain readable
- [ ] Forms display well
- [ ] Charts resize properly

### Mobile (<768px)
- [ ] Hamburger menu works
- [ ] Tables scroll horizontally if needed
- [ ] Forms stack vertically
- [ ] Charts remain interactive
- [ ] Buttons easily tappable
- [ ] Text readable without zooming

## 7. Permissions and Security

### Authentication
- [ ] Unauthenticated users redirected to login
- [ ] Cannot access dashboard without login
- [ ] Cannot view transactions without login
- [ ] Cannot access profile without login

### Authorization
- [ ] Users can only view their own transactions
- [ ] Users can only edit their own transactions
- [ ] Users can only delete their own transactions
- [ ] Users cannot access other users' data via URL manipulation

### CSRF Protection
- [ ] Forms include CSRF token
- [ ] POST requests without token rejected
- [ ] CSRF token validation working

## 8. Django Admin

### Access
- [ ] Login with superuser credentials
- [ ] Navigate to admin dashboard
- [ ] Verify all models registered

### User Management
- [ ] View users list
- [ ] Search users by username/email
- [ ] Filter by date joined
- [ ] Edit user profile
- [ ] View user's transactions

### Transaction Management
- [ ] View transactions list
- [ ] Search by username, note, category
- [ ] Filter by type, category, date, user
- [ ] Use date hierarchy navigation
- [ ] Edit transaction
- [ ] Delete transaction
- [ ] Verify formatted amount display
- [ ] Check note preview truncation

### Category Management
- [ ] View categories list
- [ ] Filter by type
- [ ] Search by name
- [ ] Edit category
- [ ] Add new category

## 9. Error Handling

### 404 Page Not Found
- [ ] Navigate to non-existent URL
- [ ] Verify custom 404 page displays
- [ ] Check "Go to Dashboard" button works
- [ ] Check "Go Back" button works

### 500 Server Error
- [ ] Custom 500 page exists (test in DEBUG=False mode)
- [ ] Verify error page has proper styling
- [ ] Check "Try Again" button works

### Form Validation Errors
- [ ] Submit form with invalid data
- [ ] Verify error messages display clearly
- [ ] Check field-specific errors highlighted
- [ ] Verify form retains valid input

## 10. Performance

### Page Load Times
- [ ] Dashboard loads < 2 seconds
- [ ] Transaction list loads < 2 seconds
- [ ] Reports page loads < 2 seconds
- [ ] Charts render quickly

### Database Queries
- [ ] No N+1 query problems (check logs)
- [ ] select_related used for foreign keys
- [ ] prefetch_related used where appropriate
- [ ] Indexes on frequently queried fields

## 11. Logging

### Application Logs
- [ ] Check logs/django.log exists
- [ ] Verify requests logged
- [ ] Check log rotation works (10MB limit)

### Error Logs
- [ ] Check logs/django_error.log exists
- [ ] Trigger an error and verify it's logged
- [ ] Verify stack traces included

## 12. Environment Configuration

### Environment Variables
- [ ] .env.example file exists
- [ ] All sensitive data in environment variables
- [ ] DEBUG setting works from .env
- [ ] Database settings from .env
- [ ] SECRET_KEY from .env

## Test Results Summary

**Date:** _________
**Tester:** _________
**Browser:** _________
**OS:** _________

**Pass:** _____ / _____
**Fail:** _____ / _____

### Critical Issues Found:
1.
2.
3.

### Minor Issues Found:
1.
2.
3.

### Notes:



### Sign-off:
- [ ] All critical features working
- [ ] No blocking bugs
- [ ] Ready for deployment

**Tester Signature:** _________
**Date:** _________
