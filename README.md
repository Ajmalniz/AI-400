# AI-400: Cloud-Native AI — Learn Dapr, Docker & Kubernetes with AIDD

This repository contains my progress and work for the **AI-400** course from Panaversity.

**Course Page:** [AI-400 - Cloud-Native AI](https://panaversity.org/flagship-program/courses/AI-400)

## Course Overview

**Cloud-Native AI** teaches you how to build cloud infrastructure for AI agents using Specification-Driven Development and AI-Driven Development (AIDD). You'll learn to take AI projects from local experiments to production-grade systems that scale automatically, recover gracefully, and run anywhere.

**Duration:** 3 months  
**Prerequisites:** AI-300 (AI-Driven Development with Python and Agentic AI)

## Course Description

The way we build and run AI is changing. It's no longer just about running agents on your laptop—it's about deploying intelligent systems that live and scale in the cloud. Cloud-Native AI gives you the skills to take your AI projects from local experiments to production-grade systems.

In this course, you'll learn how to build cloud infrastructure for AI agents using Specification-Driven Development and AI-Driven Development (AIDD). You'll start with FastAPI and Docker, packaging your applications into portable containers. Then move to Kubernetes, learning how to run and manage those containers at scale. Finally, you'll explore Dapr, the layer that makes your AI systems cloud-agnostic, with built-in support for state management, pub/sub messaging, and service communication.

## Key Learning Modules

### Module 1: Foundations: Cloud Native Infrastructure for AI
- Master Context Engineering to structure AI collaboration for infrastructure design
- Partner with Claude Code to understand containerization (Docker), orchestration (Kubernetes), and cloud-agnostic abstractions (Dapr)
- Learn Spec-Driven Development (SDD) fundamentals
- Establish professional thinking patterns for production deployment

**Status:** 🚧 In Progress

**Progress:**
- ✅ Built Task Management API with FastAPI
- ✅ Implemented comprehensive test suite (41 tests, 100% coverage)
- ✅ Applied TDD principles and agent-specific testing patterns
- 🚧 Working on FastAPI skill enhancements (agent integration)
- 📝 Learning Context Engineering and AI collaboration patterns

---

### Module 2: Docker Fundamentals: Containerizing AI Applications
- Containerize FastAPI services using Docker with AIDD and SDD
- Multi-stage builds, Python dependencies, layer optimization
- Master container networking, health checks, and Docker Compose for local development
- Focus on specification and validation, not Dockerfile syntax memorization

**Status:** ⏳ Not Started

---

### Module 3: Kubernetes Basics: Orchestrating Agent Systems
- Orchestrate agent systems on Kubernetes with AIDD and SDD using kubectl-ai and kagent
- Specify deployment requirements—pods, services, ConfigMaps, StatefulSets
- Master Kubernetes primitives through specifications
- Event-driven patterns with Kafka and production-grade configurations

**Status:** ⏳ Not Started

---

### Module 4: DAPR Core: Cloud-Agnostic Abstractions
- Implement Dapr Core and Dapr Workflows for cloud-agnostic communication and long-running processes
- Specify requirements—state stores, pub/sub, service invocation, durable workflows
- Master cloud-portable patterns: state works with any database, pub/sub with any broker
- Write once, deploy anywhere

**Status:** ⏳ Not Started

---

### Module 5: Production Operations: Observability, Scaling & CI/CD
- Build production-ready AI systems using SDD for operations and monitoring
- Specify observability requirements—OpenTelemetry traces, metrics, cost dashboards
- Master autoscaling, CI/CD with Testcontainers and GitHub Actions
- Infrastructure-as-Code with Terraform

**Status:** ⏳ Not Started

---

## Course Outcomes

Upon completion, I will be able to:

- ✅ Apply Context Engineering to structure effective AI collaboration for infrastructure design
- ✅ Partner with Claude Code to generate production-ready cloud configurations from specifications
- ✅ Master Spec-Driven Development (SDD) to design infrastructure through clear intent, not manual YAML
- ✅ Containerize AI applications with Docker using AIDD and SDD for multi-stage builds and optimization
- ✅ Orchestrate agent systems on Kubernetes with AIDD and SDD using kubectl-ai and kagent
- ✅ Implement Dapr Core and Dapr Workflows for cloud-agnostic state, pub/sub, and long-running processes
- ✅ Build observable, scalable AI systems with OpenTelemetry, autoscaling, and automated CI/CD pipelines

## Progress Tracker

| Module | Status | Start Date | Completion Date | Notes |
|--------|--------|------------|-----------------|-------|
| Module 1: Foundations | 🚧 In Progress | 2026-01-09 | - | FastAPI project + testing completed |
| Module 2: Docker Fundamentals | ⏳ Not Started | - | - | - |
| Module 3: Kubernetes Basics | ⏳ Not Started | - | - | - |
| Module 4: DAPR Core | ⏳ Not Started | - | - | - |
| Module 5: Production Operations | ⏳ Not Started | - | - | - |

**Overall Progress:** 0/5 Modules Completed (0%)

## Skills Development & Learning Notes

### Skill Design Best Practices

**Key Principle:** Use progressive disclosure with domain-specific organization for complex skills.

**Example - E-commerce Skill Structure:**
```
ecommerce/
├── SKILL.md (overview, workflow, navigation)
└── references/
    ├── products.md (catalog, inventory, categories)
    ├── cart.md (shopping cart, session management)
    ├── orders.md (order processing, fulfillment)
    ├── payments.md (payment gateways, transactions)
    ├── users.md (authentication, profiles, addresses)
    ├── shipping.md (delivery, tracking, zones)
    └── admin.md (dashboard, analytics, management)
```

**Guidelines:**
- Keep SKILL.md under 500 lines (concise is key)
- Use one skill for cohesive domains (e.g., e-commerce as one system)
- Split complex domains into reference files (loaded only when needed)
- Separate skills only if truly independent (different deployment cycles/teams)

**Skills to Build:**
- [x] FastAPI skill (enhanced with agent integration) - In progress
- [ ] E-commerce development skill (planned)
- [ ] _(Add more skills as they come up)_

### Module 1 Accomplishments

#### Task Management API Project
Built a production-ready FastAPI application demonstrating cloud-native AI foundations:

**Features:**
- ✅ FastAPI application with root, tasks, and search endpoints
- ✅ Path parameters and query parameters implemented
- ✅ Proper error handling and validation
- ✅ API documentation via FastAPI's auto-generated docs

**Testing:**
- ✅ **41 comprehensive tests** covering all endpoints
- ✅ **100% code coverage** on main application code
- ✅ Agent-specific testing patterns (schema stability, contract consistency)
- ✅ TDD principles applied (red-green-refactor)
- ✅ Test suite organized with pytest classes and fixtures
- ✅ Integration tests and pagination consistency tests

**Project Structure:**
```
task-management-api/
├── main.py              # FastAPI application (100% tested)
├── tests/
│   ├── test_main.py     # 41 comprehensive tests
│   └── conftest.py      # Shared fixtures
├── pyproject.toml       # Dependencies with uv
├── pytest.ini           # Pytest configuration
└── htmlcov/             # Coverage reports (98% overall)
```

**Key Learnings:**
- Context Engineering: Structured AI collaboration for infrastructure design
- Spec-Driven Development: Clear intent over manual configuration
- Testing for AI agents: Schema stability, contract consistency, error format standardization
- FastAPI best practices: Type hints, async/await, automatic validation

#### FastAPI Skill Development
Working on enhancing the FastAPI skill with:
- Agent integration patterns (APIs → Functions → Tools → Agents)
- Comprehensive testing documentation
- Complete CRUD operations examples
- Agent-specific workflows and best practices

**See:** `prompt_to_update_fastapi_skill_agent_integration.md` for enhancement plan

## Repository Structure

```
.
├── .claude/
│   └── skills/        # Claude Code skills development
│       ├── fastapi/   # FastAPI skill (enhanced with agent integration)
│       └── ...        # Other skills (browser-use, context7, docx, pdf, etc.)
├── task-management-api/  # Module 1: FastAPI project with comprehensive testing
│   ├── main.py        # FastAPI application
│   ├── tests/         # Test suite (41 tests, 100% coverage)
│   └── pyproject.toml # Dependencies
├── module-1/          # Foundations: Cloud Native Infrastructure for AI (planned)
├── module-2/          # Docker Fundamentals: Containerizing AI Applications (planned)
├── module-3/          # Kubernetes Basics: Orchestrating Agent Systems (planned)
├── module-4/          # DAPR Core: Cloud-Agnostic Abstractions (planned)
├── module-5/          # Production Operations: Observability, Scaling & CI/CD (planned)
├── projects/          # Course projects and assignments (planned)
├── notes/             # Course notes and documentation (planned)
└── fastapi.skill      # Packaged FastAPI skill file
```

## Resources

- [Course Page](https://panaversity.org/flagship-program/courses/AI-400)
- [Panaversity](https://panaversity.org)

---

**Status Legend:**
- ⏳ Not Started
- 🚧 In Progress
- ✅ Completed
