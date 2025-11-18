# SDD Skill Reference Guide

## Detailed Workflow Diagram

```
User Request
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: SPECIFICATION                                       │
│ Tool: /create-spec slash command                            │
│ Input: User requirements                                     │
│ Output: context/specs.md                                     │
│                                                              │
│ Contains:                                                    │
│ - Project overview                                           │
│ - Features list                                              │
│ - Data models                                                │
│ - Views/pages                                                │
│ - User flows                                                 │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: PLANNING                                            │
│ Agent: planning                                              │
│ Input: context/specs.md                                      │
│ Output: context/plan.md                                      │
│                                                              │
│ Contains:                                                    │
│ - Django apps structure                                      │
│ - Models with fields                                         │
│ - Views and URLs                                             │
│ - 5-7 implementation phases                                  │
│ - Timeline estimates                                         │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: TASK BREAKDOWN                                      │
│ Agent: breakdown-tasks                                       │
│ Input: context/plan.md                                       │
│ Output: context/tasks.md                                     │
│                                                              │
│ Contains:                                                    │
│ - Task table (ID, Description, Phase, Status, Estimate)     │
│ - Progress statistics                                        │
│ - Dependencies notes                                         │
│ - Each task: 0.5-4 hours                                     │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: IMPLEMENTATION                                      │
│ Agent: implement (multiple instances)                        │
│ Input: context/tasks.md                                      │
│ Output: Code, tests, updated tasks.md                        │
│                                                              │
│ Process:                                                     │
│ 1. Analyze dependencies                                      │
│ 2. Group into sequential/parallel tasks                      │
│ 3. Execute with TDD (RED-GREEN-REFACTOR)                     │
│ 4. Update task status after each completion                  │
│ 5. Run full test suite                                       │
└─────────────────────────────────────────────────────────────┘
    ↓
Completed Feature
```

## Task Dependency Analysis

### Dependency Types

1. **Hard Dependencies** (Must be sequential)
   - Model → Migration
   - Migration → View (using model)
   - View → Template (using view)
   - Parent Model → Child Model (ForeignKey)

2. **Soft Dependencies** (Can parallelize with caution)
   - Different models in same app
   - Different views using same model
   - Different test files

3. **No Dependencies** (Fully parallel)
   - Different Django apps
   - Tests for different models
   - Independent templates
   - Documentation tasks

### Dependency Detection Algorithm

```python
def analyze_task_dependencies(tasks):
    """
    Analyze tasks and group them for execution.

    Returns:
        List of task groups: [
            {'type': 'sequential', 'tasks': [...]},
            {'type': 'parallel', 'tasks': [...]},
        ]
    """
    groups = []

    # Phase 1: Setup (always sequential)
    setup_tasks = filter_tasks_by_phase(tasks, 'Setup')
    if setup_tasks:
        groups.append({'type': 'sequential', 'tasks': setup_tasks})

    # Phase 2: Models
    model_tasks = filter_tasks_by_phase(tasks, 'Models')
    model_creates = filter_by_keyword(model_tasks, 'Create', 'Implement')
    model_tests = filter_by_keyword(model_tasks, 'Write', 'Test')
    migration_tasks = filter_by_keyword(model_tasks, 'migration')

    # Models can be parallel if no FK relationships
    if has_no_fk_dependencies(model_creates):
        groups.append({'type': 'parallel', 'tasks': model_creates})
    else:
        groups.append({'type': 'sequential', 'tasks': model_creates})

    # Model tests can be parallel
    groups.append({'type': 'parallel', 'tasks': model_tests})

    # Migrations must be sequential
    groups.append({'type': 'sequential', 'tasks': migration_tasks})

    # Phase 3: Views
    view_tasks = filter_tasks_by_phase(tasks, 'Views')
    # Views can often be parallel
    groups.append({'type': 'parallel', 'tasks': view_tasks})

    # Continue for other phases...

    return groups
```

## Agent Invocation Patterns

### Pattern 1: Sequential Execution

```python
# For tasks that depend on each other
for task in sequential_tasks:
    invoke_agent(
        subagent_type="implement",
        prompt=f"Implement {task.id}: {task.description}. "
               f"Read context/tasks.md, complete the task using TDD, "
               f"and update the task status to 'done'."
    )
    wait_for_completion()
    verify_task_done(task.id)
```

### Pattern 2: Parallel Execution

```python
# For independent tasks - invoke all in single message
parallel_prompts = []
for task in parallel_tasks:
    parallel_prompts.append({
        'subagent_type': 'implement',
        'prompt': f"Implement {task.id}: {task.description}. "
                  f"Use TDD and update task status when done."
    })

# Send all at once
invoke_multiple_agents(parallel_prompts)
wait_for_all_completions()
verify_all_done([task.id for task in parallel_tasks])
```

### Pattern 3: Hybrid Execution

```python
# Mix of sequential and parallel
# Group 1: Setup (sequential)
execute_sequential(['T001', 'T002'])

# Group 2: Models (parallel)
execute_parallel(['T003', 'T004', 'T005'])

# Group 3: Migrations (sequential)
execute_sequential(['T006', 'T007'])

# Group 4: Views (parallel)
execute_parallel(['T008', 'T009', 'T010'])
```

## Real-World Example: Blog Application

### User Request
"Build a blog with posts, comments, and categories"

### Phase 1: Specification Output
```markdown
# Blog Application Specification

## Overview
Simple blog with posts, comments, categories, and user authentication.

## Models
1. Category: name, slug, description
2. Post: title, slug, content, author(FK), category(FK), published_date
3. Comment: post(FK), author(FK), content, created_date

## Views
- Post list (homepage)
- Post detail (with comments)
- Post create/edit/delete
- Category list
- Comment create

## Features
- User registration/login
- Rich text editor for posts
- Comment moderation
- Category filtering
```

### Phase 2: Planning Output
```markdown
# Blog Implementation Plan

## Django Apps
- blog: Main blog functionality
- accounts: User management (extend Django auth)

## Models

### Category
- name: CharField(100)
- slug: SlugField(unique)
- description: TextField

### Post
- title: CharField(200)
- slug: SlugField(unique)
- content: RichTextField
- author: ForeignKey(User)
- category: ForeignKey(Category)
- published_date: DateTimeField
- is_published: BooleanField

### Comment
- post: ForeignKey(Post)
- author: ForeignKey(User)
- content: TextField
- created_date: DateTimeField
- is_approved: BooleanField

## Implementation Phases

### Phase 1: Project Setup (1-2h)
- Create blog and accounts apps
- Configure settings
- Setup base templates

### Phase 2: Models (3-4h)
- Create Category model
- Create Post model
- Create Comment model
- Write model tests
- Generate and apply migrations

### Phase 3: Views (4-5h)
- Post list view
- Post detail view
- Post create/edit/delete views
- Comment create view
- Category filter view

### Phase 4: Templates (3-4h)
- Base template with navigation
- Post list template
- Post detail template
- Post form template
- Category list template

### Phase 5: User Authentication (2-3h)
- Login/logout views
- Registration view
- User profile view

### Phase 6: Testing & Polish (2-3h)
- Integration tests
- UI improvements
- Error handling
```

### Phase 3: Task Breakdown Output
```markdown
# Task Tracking - Blog Application

**Last Updated:** 2025-01-15 10:00
**Progress:** Done: 0 | In Progress: 0 | Pending: 28

## Tasks

| ID | Task | Phase | Status | Est |
|----|------|-------|--------|-----|
| T001 | Create blog app | Setup | pending | 0.5h |
| T002 | Create accounts app | Setup | pending | 0.5h |
| T003 | Configure installed apps | Setup | pending | 0.5h |
| T004 | Setup base template structure | Setup | pending | 1h |
| T005 | Create Category model | Models | pending | 1h |
| T006 | Create Post model | Models | pending | 2h |
| T007 | Create Comment model | Models | pending | 1h |
| T008 | Add __str__ and Meta to models | Models | pending | 0.5h |
| T009 | Write Category model tests | Models | pending | 1h |
| T010 | Write Post model tests | Models | pending | 2h |
| T011 | Write Comment model tests | Models | pending | 1h |
| T012 | Generate migrations | Models | pending | 0.5h |
| T013 | Apply migrations | Models | pending | 0.5h |
| T014 | Register models in admin | Models | pending | 0.5h |
| T015 | Create PostListView | Views | pending | 2h |
| T016 | Create PostDetailView | Views | pending | 2h |
| T017 | Create PostCreateView | Views | pending | 2h |
| T018 | Create PostUpdateView | Views | pending | 1h |
| T019 | Create PostDeleteView | Views | pending | 1h |
| T020 | Create CommentCreateView | Views | pending | 2h |
| T021 | Configure URL patterns | Views | pending | 1h |
| T022 | Write view tests | Views | pending | 3h |
| T023 | Create base.html template | Templates | pending | 2h |
| T024 | Create post_list.html | Templates | pending | 2h |
| T025 | Create post_detail.html | Templates | pending | 2h |
| T026 | Create post_form.html | Templates | pending | 1h |
| T027 | Add Bootstrap styling | Templates | pending | 2h |
| T028 | Final integration testing | Testing | pending | 2h |

## Notes
- T006 depends on T005 (Post has FK to Category)
- T007 depends on T006 (Comment has FK to Post)
- T012-T013 must run after all models created
- T015-T020 depend on T013 (migrations applied)
- T023-T027 depend on T015-T020 (templates use views)
```

### Phase 4: Implementation Execution Plan

#### Group 1: Setup (Sequential)
```
Execute sequentially:
- T001: Create blog app
- T002: Create accounts app
- T003: Configure installed apps
- T004: Setup base template structure

Estimated: 2.5 hours
```

#### Group 2: Model Creation (Sequential - FK dependencies)
```
Execute sequentially:
- T005: Create Category model (independent)
- T006: Create Post model (depends on T005)
- T007: Create Comment model (depends on T006)
- T008: Add __str__ and Meta (depends on all models)

Estimated: 4.5 hours
```

#### Group 3: Model Tests (Parallel)
```
Execute in parallel:
- T009: Write Category model tests
- T010: Write Post model tests
- T011: Write Comment model tests

Estimated: 2 hours (parallel execution)
```

#### Group 4: Migrations (Sequential)
```
Execute sequentially:
- T012: Generate migrations
- T013: Apply migrations
- T014: Register models in admin

Estimated: 1.5 hours
```

#### Group 5: Views (Parallel where possible)
```
Execute in parallel:
- T015: Create PostListView
- T016: Create PostDetailView
- T020: Create CommentCreateView

Then execute:
- T017: Create PostCreateView
- T018: Create PostUpdateView
- T019: Create PostDeleteView
- T021: Configure URL patterns

Then:
- T022: Write view tests

Estimated: 6 hours (with parallelization)
```

#### Group 6: Templates (Parallel)
```
Execute in parallel:
- T023: Create base.html
- T024: Create post_list.html
- T025: Create post_detail.html
- T026: Create post_form.html

Then:
- T027: Add Bootstrap styling

Estimated: 4 hours (with parallelization)
```

#### Group 7: Final Testing (Sequential)
```
Execute:
- T028: Final integration testing

Estimated: 2 hours
```

**Total Estimated Time:**
- Sequential execution: ~40 hours
- With parallelization: ~22 hours
- Time saved: ~45%

## Error Recovery Strategies

### Scenario 1: Test Failures During Implementation

**Problem**: Task T010 (Write Post model tests) fails

**Recovery**:
```
1. Agent reports: "Test T010 failing: Post model validation error"
2. Review test output
3. Identify issue: Missing field validation
4. Fix Post model
5. Re-run tests
6. Verify tests pass
7. Mark T010 as done
8. Continue to next task
```

### Scenario 2: Dependency Conflict

**Problem**: Attempted parallel execution of T006 and T007, but T007 needs T006

**Recovery**:
```
1. Detect error: "Comment model references undefined Post model"
2. Analyze dependency graph
3. Identify T007 depends on T006
4. Cancel T007 execution
5. Complete T006 first
6. Restart T007
7. Update dependency notes in tasks.md
```

### Scenario 3: Specification Ambiguity

**Problem**: Comment moderation requirements unclear

**Recovery**:
```
1. Agent reports: "Unclear specification for comment moderation"
2. Ask user: "Should comments be auto-approved or require manual approval?"
3. User responds: "Manual approval for non-staff users"
4. Update context/specs.md with clarification
5. Update context/plan.md if needed
6. Continue implementation
```

## Performance Metrics

### Example Metrics After Completion

```
Blog Application - Completion Report

Total Tasks: 28
├─ Completed: 28
├─ Failed: 0
└─ Skipped: 0

Time Spent:
├─ Estimated: 40 hours (sequential)
├─ Actual: 23 hours (with parallelization)
└─ Efficiency: 42.5% time saved

Test Results:
├─ Total Tests: 45
├─ Passing: 45
├─ Failing: 0
└─ Coverage: 89%

Files Created:
├─ Models: 3 files
├─ Views: 6 files
├─ Templates: 5 files
├─ Tests: 8 files
└─ Total: 22 files

Code Quality:
├─ PEP 8 Compliance: 100%
├─ Docstring Coverage: 95%
├─ Type Hints: 100%
└─ Complexity: Low (avg cyclomatic 3.2)
```

## Best Practices Summary

1. **Always start with clear specs** - Time invested here saves hours later
2. **Review plan before tasks** - Catch issues early
3. **Parallelize intelligently** - Speed up without breaking dependencies
4. **Test continuously** - Don't wait until the end
5. **Update tasks.md religiously** - Track progress accurately
6. **Communicate clearly** - Keep user informed
7. **Handle errors gracefully** - Have recovery strategies
8. **Document decisions** - Future you will thank present you

## Integration with CI/CD

After SDD completion, the codebase is ready for:

```bash
# Run full test suite
docker compose exec web python manage.py test

# Check coverage
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report

# Lint code
docker compose exec web flake8 .

# Run Django checks
docker compose exec web python manage.py check

# Create deployment
docker compose exec web python manage.py collectstatic
```

All tests should pass and be ready for deployment!
