---
mode: 'chat'
description: 'Create a simple specification file for Django project features'
---
# Create Specification

Your goal is to create a clear and concise specification file for `${input:SpecPurpose}`.

The specification should be saved in the [/context/](/context/) directory and named descriptively (e.g., `specs.md`, `feature-specs.md`).

## Best Practices for Specifications

- Write in clear, simple language (Vietnamese or English based on user preference)
- Use structured formatting with headings and bullet points
- Include practical examples and code snippets where helpful
- Focus on what needs to be built, not how to build it
- Keep it concise and easy to understand
- Include data models when relevant

## Template Structure

Use the following simple template for specifications:

```md
# [Project/Feature Name] - [Brief Description]

---

## 1. Tổng quan dự án

- **Tên ứng dụng:** [Application Name]
- **Mục tiêu:** [Main goals and purpose]
- **Công nghệ sử dụng:** [Tech stack: Django, PostgreSQL, Bootstrap, etc.]

---

## 2. Tính năng chính

### A. [Feature Group 1]

- [Feature description]
- [Sub-features]:
  - [Detail 1]
  - [Detail 2]
  - [Detail 3]

### B. [Feature Group 2]

- [Feature description]
- [Requirements and details]

### C. [Additional Features]

- [Continue listing all major feature groups]

---

## 3. Cấu trúc dữ liệu (Models)

```python
from django.contrib.auth.models import User
from django.db import models

class ModelName(models.Model):
    """Brief description of the model."""

    field1 = models.CharField(max_length=100)
    field2 = models.ForeignKey(User, on_delete=models.CASCADE)
    # ... other fields

    def __str__(self):
        return self.field1
```

[Include all relevant models with clear field definitions]

---

## 4. Các trang chính (Views & Templates)

- Trang 1: [Purpose and functionality]
- Trang 2: [Purpose and functionality]
- Trang 3: [Purpose and functionality]
- [List all main pages/views]

---

## 5. Luồng sử dụng

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Continue with user journey]

---

## 6. Yêu cầu khác

- [Technical requirements]
- [UI/UX requirements]
- [Performance requirements]
- [Security requirements]
- [Code quality requirements]

---

## 7. Ghi chú kỹ thuật (Optional)

- [Any technical notes]
- [Constraints or limitations]
- [Future enhancements]
```

## Instructions

1. Analyze the user's requirement for `${input:SpecPurpose}`
2. Create a specification file following the template above
3. Adapt sections based on the specific needs (you can skip sections that aren't relevant)
4. Use code examples for models and important logic
5. Keep the language consistent (Vietnamese or English throughout)
6. Make it practical and actionable for developers

## Key Points

- **Simple over complex**: This is not a formal requirements document
- **Developer-focused**: Written for developers who will implement it
- **Django-specific**: Include Django models, views, templates structure
- **Visual elements**: Mention UI/UX requirements and design preferences
- **Data models first**: Always include clear model definitions
- **User journey**: Describe how users will interact with the system
