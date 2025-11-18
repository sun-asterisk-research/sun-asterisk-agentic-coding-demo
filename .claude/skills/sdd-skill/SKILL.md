---
name: sdd-skill
description: Specification-Driven Development workflow for Django projects. Orchestrates the complete development process from specs to implementation using planning, task breakdown, and TDD implementation. Use when user wants to build a Django feature from specifications or needs end-to-end development workflow.
---

# SDD (Specification-Driven Development) Skill

This skill orchestrates a complete development workflow for Django projects, taking user requirements through specification creation, planning, task breakdown, and implementation using Test-Driven Development.

## Overview

The SDD workflow consists of four main phases:

1. **Specification Creation** - Document requirements clearly
2. **Planning** - Break down specifications into implementation phases
3. **Task Breakdown** - Convert plan into granular, trackable tasks
4. **Implementation** - Execute tasks using TDD methodology

## Workflow Steps

### Phase 1: Create Specification

**Objective**: Transform user requirements into a structured specification document.

**Process**:
1. Ask user to describe their feature/project requirements
2. Use the `/create-spec` slash command to generate specification
3. Create `context/specs.md` with structured requirements including:
   - Project overview and objectives
   - Main features and functionality
   - Data models (Django models)
   - Main views and pages
   - User flows
   - Technical requirements

**Output**: `context/specs.md` file with complete feature specification

**Example**:
```
User: "I want to build a personal finance tracker"
Assistant: [Uses /create-spec to create specification with all requirements]
Output: context/specs.md created
```

### Phase 2: Planning

**Objective**: Create an implementation plan with clear phases and tasks.

**Process**:
1. Invoke the `planning` sub-agent
2. Agent reads `context/specs.md`
3. Agent creates `context/plan.md` with:
   - Overview and tech stack
   - Django apps to create
   - Models to implement
   - Views and URLs
   - Templates needed
   - 5-7 implementation phases
   - Timeline estimates

**Output**: `context/plan.md` with structured implementation plan

**Agent Invocation**:
```
Use the Task tool with subagent_type="planning" to create implementation plan from specs.
```

### Phase 3: Task Breakdown

**Objective**: Convert high-level plan into specific, trackable tasks.

**Process**:
1. Invoke the `breakdown-tasks` sub-agent
2. Agent reads `context/plan.md`
3. Agent creates `context/tasks.md` with:
   - Task table with IDs (T001, T002, ...)
   - Task descriptions
   - Phase assignments
   - Status tracking (pending/in_progress/done)
   - Time estimates (0.5-4h per task)
   - Progress statistics

**Output**: `context/tasks.md` with complete task list

**Agent Invocation**:
```
Use the Task tool with subagent_type="breakdown-tasks" to create task list from plan.
```

### Phase 4: Implementation

**Objective**: Implement all tasks using Test-Driven Development.

**Process**:
1. Review all tasks in `context/tasks.md`
2. Identify tasks that can be executed in parallel (independent tasks)
3. For each task or group of tasks:
   - Invoke the `implement` sub-agent
   - Agent follows TDD cycle: RED → GREEN → REFACTOR
   - Agent writes tests first
   - Agent implements minimal code to pass tests
   - Agent refactors for quality
   - Agent updates task status in `context/tasks.md`

**Parallelization Strategy**:
- **Sequential tasks** (dependencies): Models → Migrations → Views → Templates
- **Parallel tasks** (independent):
  - Multiple model tests can be written simultaneously
  - Multiple view implementations (if models exist)
  - Multiple template creations
  - Different Django apps

**Output**: Fully implemented feature with tests, code updated tasks.md

**Agent Invocation**:
```
For sequential tasks:
Use the Task tool with subagent_type="implement" for each task one by one.

For parallel tasks:
Use multiple Task tool calls in single message with subagent_type="implement" for independent tasks.
```

## Complete Workflow Example

```
User: "Build a todo list application with categories"

Step 1: Create Specification
→ Run: /create-spec
→ Output: context/specs.md created with:
  - Todo model (title, description, done, category)
  - Category model (name, color)
  - Views: list, create, update, delete
  - User authentication

Step 2: Planning
→ Invoke planning agent
→ Output: context/plan.md with 6 phases:
  Phase 1: Project setup
  Phase 2: Models (Category, Todo)
  Phase 3: Views (CRUD operations)
  Phase 4: Templates (list, form, detail)
  Phase 5: Testing
  Phase 6: Polish

Step 3: Task Breakdown
→ Invoke breakdown-tasks agent
→ Output: context/tasks.md with 25 tasks:
  T001: Create todo app [Setup] [1h]
  T002: Create Category model [Models] [1h]
  T003: Create Todo model [Models] [2h]
  T004: Write Category tests [Models] [1h]
  ... (21 more tasks)

Step 4: Implementation
→ Invoke implement agent for tasks:

  Parallel group 1 (Models):
  - T002: Create Category model
  - T004: Write Category tests

  Sequential:
  - T003: Create Todo model (depends on Category)
  - T005: Write Todo tests
  - T006: Generate migrations
  - T007: Apply migrations

  Parallel group 2 (Views):
  - T008: Implement TodoListView
  - T009: Implement CategoryListView

  ... continue until all tasks done

→ Output: Fully working todo app with tests
```

## Instructions for Claude

When this skill is invoked, follow these steps:

### 1. Initial Assessment
- Confirm user wants to use SDD workflow
- Ask for project/feature description if not provided
- Verify `context/` directory exists (create if needed)

### 2. Execute Phase 1: Specification
```
1. Gather requirements from user
2. Run slash command: /create-spec
3. Verify context/specs.md was created
4. Show summary to user
5. Ask for approval before proceeding
```

### 3. Execute Phase 2: Planning
```
1. Invoke planning sub-agent:
   Use Task tool with:
   - subagent_type: "planning"
   - prompt: "Read context/specs.md and create a detailed implementation plan in context/plan.md. Follow the planning agent guidelines for Django projects."

2. Wait for agent completion
3. Read and verify context/plan.md
4. Show plan summary to user
5. Ask for approval before proceeding
```

### 4. Execute Phase 3: Task Breakdown
```
1. Invoke breakdown-tasks sub-agent:
   Use Task tool with:
   - subagent_type: "breakdown-tasks"
   - prompt: "Read context/plan.md and break it down into granular tasks in context/tasks.md. Each task should be 0.5-4 hours. Follow the task breakdown guidelines."

2. Wait for agent completion
3. Read and verify context/tasks.md
4. Count total tasks
5. Show task summary to user
6. Ask for approval before proceeding
```

### 5. Execute Phase 4: Implementation
```
1. Read all tasks from context/tasks.md
2. Analyze dependencies between tasks
3. Group tasks into:
   - Sequential groups (must run in order)
   - Parallel groups (can run simultaneously)

4. For each group:

   If sequential:
   - For each task in order:
     - Invoke implement agent with specific task ID
     - Wait for completion
     - Verify task marked as done
     - Continue to next task

   If parallel:
   - Invoke multiple implement agents simultaneously
   - Use single message with multiple Task tool calls
   - Each agent works on different task
   - Wait for all to complete
   - Verify all tasks marked as done

5. After all tasks complete:
   - Run full test suite
   - Verify all tests pass
   - Show completion summary
   - List completed features
```

### 6. Completion Report
```
Provide user with:
- Total tasks completed
- Total time spent
- Test coverage achieved
- Files created/modified
- Next steps (deployment, documentation, etc.)
```

## Key Principles

### ✅ DO:
1. **Follow sequence** - Don't skip phases
2. **Wait for approval** - User confirms before each phase
3. **Parallelize when safe** - Speed up independent tasks
4. **Verify outputs** - Check files created correctly
5. **Update progress** - Keep user informed
6. **Run tests frequently** - Verify nothing breaks
7. **Use Docker commands** - All Django commands via docker compose

### ❌ DON'T:
1. **Skip specification** - Always start with clear specs
2. **Rush to code** - Planning saves time
3. **Ignore dependencies** - Respect task order
4. **Forget to update tasks.md** - Track progress always
5. **Skip tests** - TDD is mandatory
6. **Create migrations manually** - Use Django commands

## Error Handling

### If specification is unclear:
- Ask clarifying questions
- Request more details from user
- Don't proceed with ambiguous requirements

### If planning fails:
- Review specs for completeness
- Ask user for technical preferences
- Restart planning phase

### If task breakdown produces tasks >4h:
- Request breakdown-tasks agent to split them
- Ensure all tasks are manageable

### If implementation tests fail:
- Debug the issue
- Fix the code
- Re-run tests
- Don't mark task as done until tests pass

### If parallel tasks conflict:
- Identify the conflict
- Make tasks sequential
- Retry implementation

## Parallelization Guidelines

### Safe to Parallelize:
- Writing tests for different models
- Creating different Django apps
- Implementing independent views
- Creating independent templates
- Writing different test files

### Must Be Sequential:
- Models before migrations
- Migrations before views using models
- Views before templates using views
- Parent models before child models (FK relationships)
- Setup tasks before implementation tasks

### Example Parallel Execution:
```
# In a single message, invoke multiple implement agents:

Task 1: "Implement T004: Write Category model tests"
Task 2: "Implement T007: Write Transaction model tests"
Task 3: "Implement T010: Create base template"

All three run simultaneously because they're independent.
```

## File Structure After Completion

```
project/
├── context/
│   ├── specs.md          # Created in Phase 1
│   ├── plan.md           # Created in Phase 2
│   └── tasks.md          # Created in Phase 3, updated in Phase 4
├── app_name/
│   ├── models.py         # Created in Phase 4
│   ├── views.py          # Created in Phase 4
│   ├── urls.py           # Created in Phase 4
│   ├── forms.py          # Created in Phase 4 (if needed)
│   ├── templates/        # Created in Phase 4
│   └── tests/            # Created in Phase 4
│       ├── test_models.py
│       ├── test_views.py
│       └── test_forms.py
└── ...
```

## Usage Examples

### Example 1: Simple Feature
```
User: "Use SDD skill to add user profile feature"

Assistant workflow:
1. Run /create-spec to create context/specs.md
2. Invoke planning agent → context/plan.md
3. Invoke breakdown-tasks agent → context/tasks.md (8 tasks)
4. Implement tasks sequentially:
   - T001: Create profile app
   - T002: Create Profile model
   - T003-T008: Views, templates, tests
5. Run tests, verify completion
6. Report: "User profile feature complete with 8 tasks, all tests passing"
```

### Example 2: Complex Feature with Parallelization
```
User: "Use SDD skill to build an inventory management system"

Assistant workflow:
1. Run /create-spec → context/specs.md
2. Invoke planning agent → context/plan.md (7 phases)
3. Invoke breakdown-tasks agent → context/tasks.md (35 tasks)
4. Implement with parallelization:

   Sequential Phase 1 (Setup):
   - T001: Create inventory app
   - T002: Configure settings

   Parallel Phase 2 (Models):
   - T003: Category model + tests (parallel)
   - T005: Product model + tests (parallel)
   - T007: Warehouse model + tests (parallel)

   Sequential Phase 3 (Relationships):
   - T009: Stock model (depends on Product, Warehouse)
   - T010: Migrations

   Parallel Phase 4 (Views):
   - T011: Product views (parallel)
   - T013: Category views (parallel)
   - T015: Warehouse views (parallel)

   ... continue through all 35 tasks

5. Final test suite: All 45 tests passing
6. Report: "Inventory system complete - 35 tasks, 45 tests, 92% coverage"
```

### Example 3: Quick Prototype
```
User: "SDD workflow for a simple blog"

Assistant workflow:
1. /create-spec → Basic blog specs
2. Planning → 5 phases
3. Breakdown → 15 tasks
4. Implement → Focus on MVP features
5. Complete in ~4 hours
```

## Tips for Success

### For Users:
1. **Be clear about requirements** - Better specs = better results
2. **Review each phase** - Verify plan and tasks before implementation
3. **Trust the process** - Don't skip phases
4. **Ask questions** - Clarify before agents proceed

### For Claude:
1. **Validate at each step** - Verify files created correctly
2. **Smart parallelization** - Analyze dependencies carefully
3. **Clear communication** - Keep user informed of progress
4. **Error recovery** - Handle failures gracefully
5. **Test frequently** - Run tests after each task group

## Version History

- **v1.0** (2025-01-15): Initial SDD skill creation
  - Four-phase workflow
  - Parallel task execution support
  - Integration with planning, breakdown-tasks, and implement agents

## Notes

- This skill requires the sub-agents (planning, breakdown-tasks, implement) to be configured
- Always uses Docker Compose for Django commands
- Enforces TDD methodology throughout implementation
- Tracks progress in context/tasks.md
- Suitable for both new features and complete projects