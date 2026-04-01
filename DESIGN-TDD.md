# OpenClaw 多智能体 TDD 开发流程设计

## 1. TDD 核心理念与多智能体映射

### TDD 循环 (Red-Green-Refactor)
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│   RED   │ ──▶ │  GREEN  │ ──▶ │REFACTOR │
│ 写测试   │     │ 写代码   │     │  重构   │
└─────────┘     └─────────┘     └────┬────┘
     ▲───────────────────────────────┘
```

### 多智能体 TDD 分工
```
┌─────────────────────────────────────────────────────────┐
│                    TDD 协作流程                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│  │ oc-qa   │───▶│ oc-dev  │───▶│ oc-qa   │             │
│  │ (RED)   │    │ (GREEN) │    │(Verify) │             │
│  │ 写测试   │    │ 写代码   │    │ 验证通过 │             │
│  └────┬────┘    └────┬────┘    └────┬────┘             │
│       │              │              │                   │
│       └──────────────┼──────────────┘                   │
│                      ▼                                  │
│               ┌─────────────┐                           │
│               │  oc-dev     │                           │
│               │ (REFACTOR)  │                           │
│               │  重构优化   │                           │
│               └─────────────┘                           │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Agent 角色与 TDD 职责

### Agent 1: oc-qa (测试驱动者)
```yaml
role: TDD Driver - Test Writer
tdd_phase: RED
responsibilities:
  - 根据需求编写失败测试 (Red)
  - 定义测试用例和边界条件
  - 编写测试文档和验收标准
  - 运行测试确认其失败 (符合预期)
  - 代码完成后验证测试通过
deliverables:
  - test/feature_name.test.js
  - test/acceptance_criteria.md
  - test/coverage_report.md
workflow:
  1. 接收 PM 分配的功能需求
  2. 分析需求，识别测试场景
  3. 编写单元测试和集成测试
  4. 运行测试，确认失败 (Red 状态)
  5. 将任务移交给 oc-dev
  6. oc-dev 完成后，验证所有测试通过
```

### Agent 2: oc-dev (实现者)
```yaml
role: TDD Implementer - Code Writer
tdd_phase: GREEN + REFACTOR
responsibilities:
  - 编写最简单代码让测试通过 (Green)
  - 重构代码提升质量 (Refactor)
  - 确保不破坏现有测试
  - 提交代码并通知 QA 验证
  - 编写实现文档
deliverables:
  - src/feature_name.js
  - docs/implementation_notes.md
  - 重构后的优化代码
workflow:
  1. 接收 QA 的测试文件
  2. 分析测试要求
  3. 编写最简实现让测试通过 (Green)
  4. 提交初步实现，通知 QA
  5. QA 确认通过后，进行重构
  6. 确保重构后测试仍通过
  7. 标记任务完成
```

### Agent 3: oc-pm (流程协调者)
```yaml
role: TDD Coordinator
tdd_phase: 全流程协调
responsibilities:
  - 拆解用户故事为可测试任务
  - 定义每个功能的验收标准
  - 协调 QA 和 Dev 的任务流转
  - 监控 TDD 循环进度
  - 处理阻塞和冲突
deliverables:
  - tasks/user_story_xxx.md
  - tasks/acceptance_criteria.md
  - 进度报告
workflow:
  1. 接收用户需求
  2. 拆解为小的可测试单元
  3. 创建任务：先 QA 写测试
  4. QA 完成后，分配给 Dev
  5. Dev 完成后，QA 验证
  6. 确认完成，关闭任务
```

### Agent 4: oc-ops (CI/CD 保障者)
```yaml
role: TDD Enabler
tdd_phase: 基础设施支持
responsibilities:
  - 配置自动化测试环境
  - 设置 CI/CD 流水线
  - 监控测试覆盖率
  - 部署测试报告工具
deliverables:
  - ci/github-actions.yml
  - ci/jest.config.js
  - monitoring/coverage_dashboard.yml
```

---

## 3. TDD 工作流详细设计

### 3.1 完整 TDD 循环流程

```
┌────────────────────────────────────────────────────────────────┐
│  Phase 1: RED (QA 写测试)                                       │
├────────────────────────────────────────────────────────────────┤
│  1. PM 创建任务                                                  │
│     └── /shared/tasks/US-001-user-login.md                      │
│                                                                  │
│  2. QA 接收任务                                                  │
│     └── 分析需求，识别测试场景                                    │
│                                                                  │
│  3. QA 编写测试                                                  │
│     └── /shared/projects/auth/test/user-login.test.js           │
│     └── /shared/projects/auth/test/mocks/user.mock.js           │
│                                                                  │
│  4. QA 运行测试 (Red)                                           │
│     └── npm test user-login.test.js                             │
│     └── 确认测试失败 (符合预期)                                  │
│                                                                  │
│  5. QA 通知 Dev                                                  │
│     └── 写入 /shared/tasks/US-001-status: READY_FOR_DEV         │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  Phase 2: GREEN (Dev 写代码)                                    │
├────────────────────────────────────────────────────────────────┤
│  1. Dev 接收测试文件                                             │
│     └── 读取 /shared/projects/auth/test/user-login.test.js      │
│                                                                  │
│  2. Dev 分析测试要求                                             │
│     └── 理解输入/输出/边界条件                                    │
│                                                                  │
│  3. Dev 编写最简实现                                             │
│     └── /shared/projects/auth/src/user-login.js                 │
│     └── 原则：让测试通过即可，不求完美                            │
│                                                                  │
│  4. Dev 运行测试 (Green)                                        │
│     └── npm test user-login.test.js                             │
│     └── 确认测试通过 ✅                                          │
│                                                                  │
│  5. Dev 通知 QA                                                  │
│     └── 写入 /shared/tasks/US-001-status: READY_FOR_VERIFY      │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  Phase 3: VERIFY (QA 验证)                                      │
├────────────────────────────────────────────────────────────────┤
│  1. QA 运行完整测试套件                                          │
│     └── npm test                                                │
│     └── 确认新功能测试通过                                       │
│     └── 确认没有破坏现有测试                                     │
│                                                                  │
│  2. QA 验证边界条件                                              │
│     └── 检查边界值、异常情况                                      │
│                                                                  │
│  3. QA 更新状态                                                  │
│     └── /shared/tasks/US-001-status: VERIFIED                   │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  Phase 4: REFACTOR (Dev 优化)                                   │
├────────────────────────────────────────────────────────────────┤
│  1. Dev 分析代码质量                                             │
│     └── 可读性、性能、设计模式                                    │
│                                                                  │
│  2. Dev 重构代码                                                 │
│     └── 提取函数、消除重复、优化命名                              │
│     └── /shared/projects/auth/src/user-login.js (优化版)        │
│                                                                  │
│  3. Dev 运行回归测试                                             │
│     └── npm test                                                │
│     └── 确认所有测试仍通过 ✅                                     │
│                                                                  │
│  4. Dev 提交代码                                                 │
│     └── git commit -m "feat: user login with tests"             │
│                                                                  │
│  5. 触发 CI/CD                                                   │
│     └── 自动运行测试、生成报告、部署                              │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  Phase 5: DONE (PM 确认)                                        │
├────────────────────────────────────────────────────────────────┤
│  1. PM 检查完成标准                                              │
│     └── 测试通过 ✅                                              │
│     └── 代码审查通过 ✅                                          │
│     └── 文档完整 ✅                                              │
│                                                                  │
│  2. PM 关闭任务                                                  │
│     └── /shared/tasks/US-001-status: DONE                       │
│                                                                  │
│  3. PM 更新进度                                                  │
│     └── 通知用户功能已完成                                        │
└────────────────────────────────────────────────────────────────┘
```

### 3.2 状态流转图

```
[TASK_CREATED] 
      │
      ▼ (PM 分配给 QA)
[RED: QA_WRITING_TEST]
      │
      ▼ (QA 完成测试)
[RED: TEST_READY]
      │
      ▼ (PM 分配给 Dev)
[GREEN: DEV_IMPLEMENTING]
      │
      ▼ (Dev 代码通过测试)
[GREEN: CODE_READY]
      │
      ▼ (QA 验证)
[VERIFIED]
      │
      ▼ (Dev 重构)
[REFACTORED]
      │
      ▼ (CI 通过)
[INTEGRATED]
      │
      ▼ (PM 确认)
[DONE]
```

---

## 4. 目录结构 (TDD 版本)

```
/mnt/d/openclaw-home/
├── agents/
│   ├── oc-pm/                   # 项目管理
│   ├── oc-qa/                   # 测试驱动
│   ├── oc-dev/                  # 实现开发
│   └── oc-ops/                  # CI/CD
│
├── shared/                      # 共享工作空间
│   ├── projects/               # 项目代码
│   │   └── {project-name}/
│   │       ├── src/            # 源代码 (Dev 写)
│   │       ├── test/           # 测试代码 (QA 写)
│   │       │   ├── unit/       # 单元测试
│   │       │   ├── integration/# 集成测试
│   │       │   └── e2e/        # 端到端测试
│   │       ├── docs/           # 文档
│   │       └── ci/             # CI 配置
│   │
│   ├── tasks/                  # 任务管理
│   │   ├── TODO/               # 待处理
│   │   ├── RED/                # 测试中
│   │   ├── GREEN/              # 开发中
│   │   ├── VERIFY/             # 验证中
│   │   └── DONE/               # 已完成
│   │
│   ├── tdd-reports/            # TDD 报告
│   │   ├── coverage/           # 覆盖率报告
│   │   ├── test-results/       # 测试结果
│   │   └── metrics/            # TDD 指标
│   │
│   └── knowledge/              # 知识库
│       ├── tdd-patterns/       # TDD 模式
│       ├── testing-best-practices/
│       └── refactoring-techniques/
│
└── infrastructure/
    ├── ci-server/              # CI 服务 (Jenkins/GitHub Actions)
    ├── test-runners/           # 测试执行环境
    └── coverage-tools/         # 覆盖率工具
```

---

## 5. 通信协议 (TDD 专用)

### 5.1 消息类型

```json
// 1. 测试就绪通知 (QA -> Dev)
{
  "message_type": "test_ready",
  "from": "oc-qa",
  "to": "oc-dev",
  "task_id": "US-001",
  "payload": {
    "test_files": [
      "/shared/projects/auth/test/user-login.test.js"
    ],
    "test_count": 5,
    "coverage_target": "80%",
    "run_command": "npm test user-login.test.js",
    "expected_behavior": "所有测试应失败 (Red 状态)"
  }
}

// 2. 实现完成通知 (Dev -> QA)
{
  "message_type": "implementation_ready",
  "from": "oc-dev",
  "to": "oc-qa",
  "task_id": "US-001",
  "payload": {
    "source_files": [
      "/shared/projects/auth/src/user-login.js"
    ],
    "test_result": "PASSED (5/5)",
    "coverage": "82%",
    "notes": "最简实现，待重构"
  }
}

// 3. 验证通过通知 (QA -> Dev)
{
  "message_type": "verification_passed",
  "from": "oc-qa",
  "to": "oc-dev",
  "task_id": "US-001",
  "payload": {
    "all_tests_passed": true,
    "no_regression": true,
    "coverage_achieved": "85%",
    "ready_for_refactor": true
  }
}

// 4. 重构完成通知 (Dev -> PM)
{
  "message_type": "refactor_complete",
  "from": "oc-dev",
  "to": "oc-pm",
  "task_id": "US-001",
  "payload": {
    "changes": ["提取验证函数", "优化错误处理"],
    "test_result": "PASSED (5/5) - 无回归",
    "code_quality_score": "A"
  }
}
```

### 5.2 任务状态文件

```markdown
# /shared/tasks/RED/US-001-user-login.md

## 任务信息
- ID: US-001
- 标题: 用户登录功能
- 状态: RED (测试中)
- 负责人: oc-qa
- 创建时间: 2026-03-20T10:00:00Z

## 需求描述
用户可以通过邮箱和密码登录系统

## 验收标准
- [ ] 正确的邮箱密码可以登录
- [ ] 错误的密码返回错误
- [ ] 不存在的邮箱返回错误
- [ ] 密码加密存储
- [ ] 登录成功返回 Token

## TDD 状态
- Phase: RED
- Test Files: /shared/projects/auth/test/user-login.test.js
- Test Count: 5
- Current Status: 测试编写完成，等待实现

## 下一步
等待 oc-dev 接收并实现
```

---

## 6. CI/CD 集成 (TDD 流程)

### 6.1 GitHub Actions 配置
```yaml
# .github/workflows/tdd-pipeline.yml
name: TDD Pipeline

on:
  push:
    paths:
      - 'src/**'
      - 'test/**'
  pull_request:

jobs:
  red-phase:
    name: RED - Run Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Upload test results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results.json

  green-phase:
    name: GREEN - Verify Implementation
    needs: red-phase
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests with coverage
        run: npm run test:coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  refactor-phase:
    name: REFACTOR - Quality Check
    needs: green-phase
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint
        run: npm run lint
      - name: Complexity check
        run: npm run complexity
      - name: Security scan
        run: npm audit
```

### 6.2 测试覆盖率阈值
```json
// jest.config.js
{
  "coverageThreshold": {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  },
  "coverageReporters": ["text", "html", "json"]
}
```

---

## 7. TDD 质量门禁

### 7.1 代码合并检查清单

```markdown
## PR Checklist (TDD)

### 测试 (QA 负责)
- [ ] 所有新功能都有对应的单元测试
- [ ] 边界条件和异常情况已覆盖
- [ ] 测试覆盖率 >= 80%
- [ ] 没有破坏现有测试 (回归测试通过)

### 实现 (Dev 负责)
- [ ] 代码让测试通过 (Green)
- [ ] 代码经过重构，质量达标
- [ ] 没有代码异味 (Code Smell)
- [ ] 代码审查通过

### 文档 (Dev + QA)
- [ ] 代码注释完整
- [ ] 测试文档已更新
- [ ] API 文档已更新 (如有)

### CI/CD (Ops 负责)
- [ ] CI 流水线通过
- [ ] 代码覆盖率报告已生成
- [ ] 性能测试通过 (如有)
```

### 7.2 TDD 指标监控

```yaml
# TDD Metrics Dashboard
metrics:
  test_coverage:
    target: >= 80%
    current: 85%
    status: GREEN

  test_count:
    unit_tests: 150
    integration_tests: 45
    e2e_tests: 12

  tdd_cycle_time:
    avg_red_phase: 2h
    avg_green_phase: 4h
    avg_refactor_phase: 1h
    total_avg: 7h

  defect_rate:
    production_bugs: 2
    bug_per_feature: 0.1
    status: GREEN
```

---

## 8. 典型工作场景

### 场景 1: 新功能开发
```
用户: 我需要用户注册功能

PM:
  └── 创建任务: US-002-user-registration
  └── 分配给 QA

QA (RED Phase):
  └── 编写测试: test/user-registration.test.js
  └── 运行测试: 5 tests failed ✅ (Red confirmed)
  └── 通知 Dev: "测试已就绪"

Dev (GREEN Phase):
  └── 查看测试要求
  └── 编写实现: src/user-registration.js
  └── 运行测试: 5 tests passed ✅ (Green achieved)
  └── 通知 QA: "实现完成，请验证"

QA (VERIFY Phase):
  └── 运行完整测试套件
  └── 确认通过，无回归
  └── 通知 Dev: "验证通过，可以重构"

Dev (REFACTOR Phase):
  └── 优化代码结构
  └── 运行测试: 5 tests passed ✅
  └── 提交 PR

PM:
  └── 检查完成标准
  └── 合并代码
  └── 通知用户: "功能已完成"
```

### 场景 2: Bug 修复 (TDD 模式)
```
用户: 登录功能有 Bug

PM:
  └── 创建 Bug 任务: BUG-001-login-fails
  └── 分配给 QA

QA:
  └── 编写回归测试复现 Bug
  └── 运行测试: 1 test failed ✅ (Bug confirmed)
  └── 分配给 Dev

Dev:
  └── 修复 Bug
  └── 运行测试: 1 test passed ✅
  └── 验证没有破坏其他功能
  └── 提交修复
```

### 场景 3: 重构 (安全重构)
```
Dev: 发现代码需要重构

Dev:
  └── 确保有完整的测试覆盖
  └── 进行小步重构
  └── 每次重构后运行测试
  └── 提交重构代码

QA:
  └── 验证所有测试仍通过
  └── 确认功能无变化
```

---

## 9. 实施建议

### Phase 1: 基础 TDD (Week 1-2)
- [ ] 配置测试环境 (Jest/Vitest)
- [ ] 建立 RED/GREEN/REFACTOR 流程
- [ ] 定义任务状态流转
- [ ] 跑通第一个 TDD 循环

### Phase 2: 自动化 (Week 3-4)
- [ ] CI/CD 集成
- [ ] 自动覆盖率报告
- [ ] 质量门禁配置

### Phase 3: 优化 (Week 5+)
- [ ] TDD 指标监控
- [ ] 流程优化
- [ ] 知识库积累

---

## 10. 优势总结

| 传统开发 | TDD 多智能体 |
|---------|------------|
| 先写代码后补测试 | 先写测试再写代码 |
| QA 和 Dev 工作割裂 | QA 和 Dev 紧密协作 |
| 容易遗漏测试场景 | 测试驱动，覆盖全面 |
| Bug 发现晚，修复成本高 | Bug 早期发现，快速修复 |
| 重构风险大 | 测试保护，安全重构 |
| 单人负责整个功能 | 专业化分工，效率高 |

---

**文档版本**: v1.0-TDD  
**创建时间**: 2026-03-20  
**状态**: 设计方案待评审
