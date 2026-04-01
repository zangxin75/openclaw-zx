# OpenClaw + TDD + Oh-my-Claudecode 整合设计方案

## 1. 核心整合思想

### 1.1 设计哲学融合

```
┌─────────────────────────────────────────────────────────────────┐
│                     三大理念融合                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TDD (测试驱动)          Oh-my-Claudecode        OpenClaw        │
│   ─────────────          ────────────────        ────────        │
│   • Red-Green-Refactor   • Teams-first          • 多平台集成      │
│   • 测试先行             • 32专业Agent          • 技能扩展        │
│   • 质量保障             • 自然语言编排         • 记忆持久化      │
│   • 安全重构             • 零学习曲线           • 工具丰富        │
│                                                                 │
│                          整合后                                   │
│                    ┌─────────────────┐                          │
│                    │ TDD-First Team  │                          │
│                    │  多智能体编排   │                          │
│                    │  专业化分工     │                          │
│                    │  资产可复用     │                          │
│                    └─────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 整合后的核心优势

| 维度 | 传统方式 | 整合方案 |
|------|---------|---------|
| **开发流程** | 线性瀑布 | TDD 循环 + 多智能体并行 |
| **任务分配** | 人工指派 | 智能识别 + 自动委派 |
| **知识复用** | 经验依赖 | 32个专业Agent能力资产 |
| **沟通成本** | 会议同步 | 异步协作 + 状态可视化 |
| **质量保证** | 事后测试 | 测试先行 + 持续验证 |
| **学习曲线** | 陡峭 | 自然语言描述即可 |

---

## 2. 整合架构设计

### 2.1 系统架构图

```
┌────────────────────────────────────────────────────────────────────┐
│                        用户交互层                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  自然语言输入 → 需求理解 → 任务拆解 → 智能委派               │  │
│  │  "帮我做一个用户登录系统"                                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────┐
│                     Oh-my-Claudecode 编排层                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │  Intent     │  │  Task       │  │  Agent      │  │ Workflow │ │
│  │  Parser     │  │  Router     │  │  Selector   │  │ Engine   │ │
│  │  (意图解析)  │  │  (任务路由)  │  │  (智能选择)  │  │ (工作流)  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┘ │
└────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────┐
│                    TDD 多智能体执行层                               │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   RED Phase  │  │  GREEN Phase │  │REFACTOR Phase│             │
│  │  (测试驱动)   │  │  (实现驱动)   │  │  (质量驱动)   │             │
│  │              │  │              │  │              │             │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │             │
│  │ │  oc-tdd  │ │  │ │ oc-tdd   │ │  │ │  oc-tdd  │ │             │
│  │ │  -tester │ │  │ │  -coder  │ │  │ │  -coder  │ │             │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Support    │  │   Support    │  │   Support    │             │
│  │    Agents    │  │    Agents    │  │    Agents    │             │
│  │              │  │              │  │              │             │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │             │
│  │ │ oc-arch  │ │  │ │ oc-ops   │ │  │ │ oc-review│ │             │
│  │ │ -itect   │ │  │ │          │ │  │ │ -er      │ │             │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │             │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │             │
│  │ │oc-research│ │  │ │ oc-doc   │ │  │ │ oc-qa    │ │             │
│  │ │          │ │  │ │ -writer  │ │  │ │          │ │             │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────┐
│                      OpenClaw 基础设施层                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  Docker  │  │  Shared  │  │  Message │  │  Skill   │           │
│  │  Runtime │  │ Workspace│  │   Bus    │  │ Registry │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 智能体角色矩阵 (整合 32 个专业能力)

#### 核心 TDD 智能体 (Core TDD Trio)

```yaml
# oc-tdd-tester (TDD 测试工程师)
name: tdd-tester
role: RED Phase Driver
inherit_from: [ohmy-qa, ohmy-test-designer, ohmy-edge-case-hunter]
tdd_phase: RED
responsibilities:
  - 编写失败的测试 (Red)
  - 分析需求边界条件
  - 设计测试用例矩阵
  - 编写验收标准
ohmy_skills:
  - test-designer: 测试设计专家
  - edge-case-hunter: 边界情况发现者
  - qa-engineer: QA工程师
  - acceptance-criteria-writer: 验收标准编写者
assets:
  - test_templates: 测试模板库
  - mock_generators: Mock数据生成器
  - coverage_analyzers: 覆盖率分析工具

# oc-tdd-coder (TDD 实现工程师)
name: tdd-coder
role: GREEN + REFACTOR Phase Driver
inherit_from: [ohmy-builder, ohmy-implementer, ohmy-refactorer]
tdd_phase: GREEN / REFACTOR
responsibilities:
  - 编写最简实现 (Green)
  - 重构优化代码
  - 确保测试通过
  - 提升代码质量
ohmy_skills:
  - implementer: 实现专家
  - refactorer: 重构专家
  - code-optimizer: 代码优化师
  - pattern-applier: 设计模式应用者
assets:
  - code_templates: 代码模板
  - refactoring_patterns: 重构模式库
  - performance_tips: 性能优化技巧

# oc-tdd-lead (TDD 技术负责人)
name: tdd-lead
role: TDD Process Coordinator
inherit_from: [ohmy-tech-lead, ohmy-coordinator]
responsibilities:
  - 协调 RED/GREEN/REFACTOR 流转
  - 解决技术争议
  - 代码审查
  - 质量保证
ohmy_skills:
  - tech-lead: 技术负责人
  - coordinator: 协调者
  - mentor: 导师
```

#### 支持智能体 (Support Agents - 按需激活)

```yaml
# oc-architect (架构师)
name: architect
role: System Architect
inherit_from: [ohmy-architect, ohmy-steering-architect, ohmy-system-designer]
activated_when:
  - 复杂系统设计需求
  - 技术选型决策
  - 架构重构
responsibilities:
  - 系统架构设计
  - 技术方案评估
  - 架构文档编写
ohmy_skills:
  - steering-architect: 架构掌舵人
  - system-designer: 系统设计师
  - tech-evaluator: 技术评估师

# oc-researcher (研究员)
name: researcher
role: Technology Researcher
inherit_from: [ohmy-researcher, ohmy-investigator, ohmy-analyst]
activated_when:
  - 新技术调研
  - 方案对比分析
  - 问题根因分析
responsibilities:
  - 技术调研
  - 方案对比
  - 可行性分析
ohmy_skills:
  - technology-researcher: 技术研究员
  - solution-analyst: 方案分析师
  - best-practice-finder: 最佳实践发现者

# oc-ops (运维工程师)
name: ops
role: DevOps Engineer
inherit_from: [ohmy-devops, ohmy-ci-cd-expert, ohmy-deployer]
activated_when:
  - CI/CD 配置
  - 环境部署
  - 监控告警
responsibilities:
  - 自动化流水线
  - 部署脚本
  - 监控配置
ohmy_skills:
  - devops-engineer: DevOps工程师
  - ci-cd-expert: CI/CD专家
  - infrastructure-designer: 基础设施设计师

# oc-doc-writer (文档工程师)
name: doc-writer
role: Documentation Specialist
inherit_from: [ohmy-doc-writer, ohmy-technical-writer]
activated_when:
  - API文档编写
  - 使用手册
  - 技术文档
responsibilities:
  - 技术文档编写
  - API文档生成
  - 使用手册
ohmy_skills:
  - technical-writer: 技术写作者
  - doc-generator: 文档生成器

# oc-reviewer (代码审查员)
name: reviewer
role: Code Reviewer
inherit_from: [ohmy-code-reviewer, ohmy-quality-gatekeeper]
activated_when:
  - PR审查
  - 代码质量检查
  - 安全审计
responsibilities:
  - 代码审查
  - 质量门禁
  - 最佳实践检查
ohmy_skills:
  - code-reviewer: 代码审查员
  - quality-gatekeeper: 质量守门人
  - security-auditor: 安全审计员

# oc-security (安全专家)
name: security
role: Security Engineer
inherit_from: [ohmy-security-expert, ohmy-vulnerability-hunter]
activated_when:
  - 安全审计
  - 漏洞扫描
  - 安全加固
responsibilities:
  - 安全评估
  - 漏洞修复
  - 安全最佳实践
ohmy_skills:
  - security-expert: 安全专家
  - vulnerability-researcher: 漏洞研究员

# oc-perf (性能专家)
name: perf
role: Performance Engineer
inherit_from: [ohmy-performance-engineer, ohmy-optimizer]
activated_when:
  - 性能优化
  - 瓶颈分析
  - 压力测试
responsibilities:
  - 性能分析
  - 优化建议
  - 性能测试
ohmy_skills:
  - performance-engineer: 性能工程师
  - bottleneck-analyzer: 瓶颈分析器

# oc-data (数据专家)
name: data
role: Data Engineer
inherit_from: [ohmy-data-scientist, ohmy-data-engineer, ohmy-ml-engineer]
activated_when:
  - 数据处理
  - 数据分析
  - ML模型
responsibilities:
  - 数据处理
  - 数据分析
  - 模型训练
ohmy_skills:
  - data-scientist: 数据科学家
  - data-engineer: 数据工程师
  - ml-engineer: ML工程师
```

---

## 3. TDD + Oh-my-Claudecode 工作流

### 3.1 智能委派流程

```
用户输入: "帮我做一个用户登录系统，要求支持邮箱密码登录和验证码"

┌─────────────────────────────────────────────────────────────────┐
│ Step 1: 意图解析 (Intent Parser)                                │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 解析结果:                                                        │
│   - 功能: 用户认证系统                                            │
│   - 复杂度: 中等 (需要安全考虑)                                    │
│   - 技术栈: 需要选择 (后端框架、数据库、缓存)                       │
│   - 特殊要求: 验证码功能                                          │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: 任务路由 (Task Router)                                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 任务拆解:                                                        │
│   1. [RESEARCH] 技术选型 → oc-researcher                        │
│   2. [ARCH] 架构设计 → oc-architect                             │
│   3. [TDD-RED] 编写测试 → oc-tdd-tester                         │
│   4. [TDD-GREEN] 实现功能 → oc-tdd-coder                        │
│   5. [TDD-REFACTOR] 代码优化 → oc-tdd-coder                     │
│   6. [REVIEW] 代码审查 → oc-reviewer                            │
│   7. [DOC] 文档编写 → oc-doc-writer                             │
│   8. [OPS] 部署配置 → oc-ops                                    │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Agent Selector (智能选择)                               │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
根据任务特征选择最佳 Agent:
   - 安全敏感 → 激活 oc-security
   - 性能要求高 → 激活 oc-perf
   - 数据量大 → 激活 oc-data
```

### 3.2 TDD 循环增强版

```
┌─────────────────────────────────────────────────────────────────┐
│                    RED Phase (测试先行)                          │
│                    激活: oc-tdd-tester                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 接收: 架构文档 + 需求规格                                     │
│                                                                 │
│  2. 分析: (使用 ohmy-test-designer 技能)                         │
│     - 识别测试场景                                                │
│     - 设计边界条件                                                │
│     - 规划测试金字塔 (单元/集成/E2E)                              │
│                                                                 │
│  3. 编写: (使用 ohmy-edge-case-hunter 技能)                      │
│     - 正向测试用例                                                │
│     - 异常测试用例                                                │
│     - 边界条件测试                                                │
│     - 安全测试用例 (激活 oc-security 协助)                        │
│                                                                 │
│  4. 验证:                                                        │
│     - 运行测试，确认全部失败 (Red ✅)                              │
│     - 生成测试报告                                                │
│     - 覆盖率基线: 0% (预期)                                       │
│                                                                 │
│  5. 移交: 标记任务状态为 READY_FOR_GREEN                         │
│     - 通知 oc-tdd-coder                                          │
│     - 提供: 测试文件 + 验收标准                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GREEN Phase (实现驱动)                         │
│                   激活: oc-tdd-coder                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 分析: (使用 ohmy-implementer 技能)                           │
│     - 理解测试要求                                                │
│     - 设计最小实现方案                                            │
│                                                                 │
│  2. 实现:                                                        │
│     - 编写最简代码 (KISS 原则)                                    │
│     - 不求完美，先让测试通过                                       │
│     - (如有疑问，咨询 oc-architect)                               │
│                                                                 │
│  3. 验证:                                                        │
│     - 运行测试，确认全部通过 (Green ✅)                            │
│     - 检查覆盖率提升                                              │
│                                                                 │
│  4. 移交: 标记任务状态为 READY_FOR_VERIFY                        │
│     - 通知 oc-tdd-tester                                         │
│     - 提供: 源代码 + 实现说明                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   VERIFY Phase (验证确认)                        │
│                   激活: oc-tdd-tester + oc-reviewer             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 回归测试:                                                    │
│     - 运行完整测试套件                                            │
│     - 确认新功能测试通过                                          │
│     - 确认无回归 (原有测试仍通过)                                  │
│                                                                 │
│  2. 代码审查: (oc-reviewer 使用 ohmy-code-reviewer 技能)         │
│     - 代码质量检查                                                │
│     - 最佳实践符合度                                              │
│     - 安全漏洞扫描 (oc-security 协助)                             │
│                                                                 │
│  3. 移交: 标记任务状态为 READY_FOR_REFACTOR                      │
│     - 通知 oc-tdd-coder                                          │
│     - 审查报告存档                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  REFACTOR Phase (质量优化)                       │
│                  激活: oc-tdd-coder + oc-perf (可选)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 分析: (使用 ohmy-refactorer 技能)                            │
│     - 代码坏味道识别                                              │
│     - 设计模式应用机会                                            │
│     - 性能优化点 (oc-perf 协助)                                   │
│                                                                 │
│  2. 重构:                                                        │
│     - 小步重构，每次修改后运行测试                                  │
│     - 应用设计模式                                                │
│     - 优化命名和结构                                              │
│                                                                 │
│  3. 验证:                                                        │
│     - 测试套件仍通过 ✅                                           │
│     - 代码质量指标提升                                            │
│     - 覆盖率保持或提升                                            │
│                                                                 │
│  4. 完成: 标记任务状态为 IMPLEMENTATION_DONE                     │
│     - 通知 oc-ops (部署)                                          │
│     - 通知 oc-doc-writer (文档)                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 能力资产复用机制

```yaml
# 能力资产库 (Asset Library)
assets:
  # 测试资产 (来自 ohmy-test-designer)
  test_patterns:
    - name: "API Endpoint Test"
      template: |
        describe('{{endpoint}}', () => {
          it('should return 200 for valid input', () => {});
          it('should return 400 for invalid input', () => {});
          it('should return 401 for unauthorized', () => {});
        });
      
    - name: "Database Model Test"
      template: |
        describe('{{model}} Model', () => {
          it('should validate required fields', () => {});
          it('should enforce unique constraints', () => {});
          it('should handle soft delete', () => {});
        });

  # 代码资产 (来自 ohmy-implementer)
  code_patterns:
    - name: "Express Controller"
      template: |
        exports.{{name}} = async (req, res, next) => {
          try {
            // Implementation
          } catch (error) {
            next(error);
          }
        };
      
    - name: "Repository Pattern"
      template: |
        class {{name}}Repository {
          async findById(id) {}
          async create(data) {}
          async update(id, data) {}
          async delete(id) {}
        }

  # 重构资产 (来自 ohmy-refactorer)
  refactoring_patterns:
    - name: "Extract Method"
      steps:
        - "识别重复代码块"
        - "创建新方法"
        - "替换重复代码为方法调用"
        - "运行测试确认"
    
    - name: "Replace Conditional with Polymorphism"
      steps:
        - "识别复杂条件逻辑"
        - "创建策略接口"
        - "实现具体策略类"
        - "替换条件判断"

  # 架构资产 (来自 ohmy-architect)
  architecture_patterns:
    - name: "Microservices"
      considerations:
        - "服务边界划分"
        - "通信协议选择"
        - "数据一致性策略"
    
    - name: "Clean Architecture"
      layers:
        - "Entities"
        - "Use Cases"
        - "Interface Adapters"
        - "Frameworks & Drivers"
```

---

## 4. 目录结构设计 (整合版)

```
/mnt/d/openclaw-home/
├── DESIGN-TDD-OMC.md           # 本设计文档
├── docker-compose.yml          # 基础设施编排
│
├── .omc/                       # Oh-my-Claudecode 配置
│   ├── config.yml              # OMC 主配置
│   ├── agents.yml              # Agent 定义
│   ├── workflows/              # 工作流定义
│   │   ├── tdd-basic.yml       # 基础 TDD 流程
│   │   ├── tdd-advanced.yml    # 高级 TDD 流程 (含架构)
│   │   └── feature-complete.yml # 完整功能开发
│   └── skills/                 # 技能映射
│       ├── ohmy-to-openclaw/   # Ohmy 技能转 OpenClaw
│       └── tdd-extensions/     # TDD 扩展技能
│
├── agents/                     # TDD + OMC 智能体
│   ├── oc-tdd-tester/          # TDD 测试工程师
│   │   ├── docker-compose.yml
│   │   ├── config/
│   │   │   ├── SOUL.md         # TDD 哲学 + Ohmy QA 精神
│   │   │   ├── IDENTITY.md
│   │   │   └── skills/
│   │   │       ├── tdd-core.yml
│   │   │       ├── ohmy-test-designer.yml
│   │   │       └── ohmy-edge-case-hunter.yml
│   │   └── workspace/
│   │       └── test-assets/    # 测试资产库
│   │
│   ├── oc-tdd-coder/           # TDD 实现工程师
│   │   ├── docker-compose.yml
│   │   ├── config/
│   │   │   └── skills/
│   │   │       ├── tdd-core.yml
│   │   │       ├── ohmy-implementer.yml
│   │   │       └── ohmy-refactorer.yml
│   │   └── workspace/
│   │       └── code-patterns/  # 代码模式库
│   │
│   ├── oc-tdd-lead/            # TDD 技术负责人
│   │   └── config/
│   │       └── skills/
│   │           ├── ohmy-tech-lead.yml
│   │           └── coordination.yml
│   │
│   ├── oc-architect/           # 架构师 (按需)
│   ├── oc-researcher/          # 研究员 (按需)
│   ├── oc-reviewer/            # 审查员 (按需)
│   ├── oc-ops/                 # 运维 (按需)
│   ├── oc-doc-writer/          # 文档 (按需)
│   ├── oc-security/            # 安全 (按需)
│   └── oc-perf/                # 性能 (按需)
│
├── shared/                     # 共享工作空间
│   ├── projects/               # 项目代码
│   │   └── {project}/
│   │       ├── src/            # 源代码 (Green 产物)
│   │       ├── test/           # 测试代码 (Red 产物)
│   │       ├── docs/           # 文档
│   │       └── .tdd/           # TDD 状态追踪
│   │           ├── current-phase  # 当前阶段: RED/GREEN/REFACTOR
│   │           ├── test-results/  # 测试结果历史
│   │           └── coverage/      # 覆盖率报告
│   │
│   ├── tasks/                  # 任务队列 (TDD 状态)
│   │   ├── BACKLOG/            # 待办
│   │   ├── RED/                # 测试中
│   │   ├── GREEN/              # 实现中
│   │   ├── VERIFY/             # 验证中
│   │   ├── REFACTOR/           # 重构中
│   │   └── DONE/               # 已完成
│   │
│   ├── omc-assets/             # Oh-my-Claudecode 资产
│   │   ├── patterns/           # 设计模式
│   │   ├── templates/          # 代码模板
│   │   ├── checklists/         # 检查清单
│   │   └── lessons/            # 经验教训
│   │
│   ├── tdd-reports/            # TDD 报告
│   │   ├── coverage/           # 覆盖率趋势
│   │   ├── metrics/            # TDD 指标
│   │   └── history/            # 历史记录
│   │
│   └── knowledge/              # 知识库
│       └── omc-integration/    # OMC 集成知识
│
├── infrastructure/             # 基础设施
│   ├── redis/                  # 消息总线
│   ├── ci-server/              # CI 服务
│   └── monitoring/             # 监控
│
└── scripts/                    # 管理脚本
    ├── init-omc.sh             # 初始化 OMC
    ├── agent-tdd.sh            # TDD Agent 管理
    ├── workflow.sh             # 工作流执行
    └── omc-cli.sh              # OMC 命令行工具
```

---

## 5. 关键集成点

### 5.1 自然语言到 TDD 的转换

```yaml
# 用户输入: "做一个用户登录功能"

intent_parsing:
  raw_input: "做一个用户登录功能"
  
  omc_nlp_analysis:
    intent: "feature_development"
    domain: "authentication"
    complexity: "medium"
    implicit_requirements:
      - "用户认证"
      - "安全性"
      - "会话管理"
    
  tdd_task_generation:
    epic: "User Authentication System"
    stories:
      - id: "US-001"
        title: "用户邮箱密码登录"
        tdd_cycle:
          - phase: RED
            assignee: oc-tdd-tester
            output: test/user-login.test.js
          - phase: GREEN
            assignee: oc-tdd-coder
            output: src/user-login.js
          - phase: REFACTOR
            assignee: oc-tdd-coder
            criteria: "代码质量 A 级"
            
      - id: "US-002"
        title: "登录状态保持"
        tdd_cycle: [...]
        
      - id: "US-003"
        title: "登录安全保护"
        tdd_cycle: [...]
        support_agents:
          - oc-security  # 安全专家参与
```

### 5.2 技能继承与扩展

```yaml
# oc-tdd-tester 技能定义示例
agent: oc-tdd-tester
skills:
  # 基础 TDD 技能
  - name: tdd-core
    source: built-in
    capabilities:
      - red-phase-execution
      - test-design
      - coverage-analysis
      
  # 继承 Oh-my-Claudecode 技能
  - name: ohmy-test-designer
    source: oh-my-claudecode
    mapping:
      ohmy_capability: "design_comprehensive_tests"
      openclaw_tool: "write_test_file"
    adaptation:
      - 增加 TDD Red 阶段验证
      - 增加失败测试确认步骤
      
  - name: ohmy-edge-case-hunter
    source: oh-my-claudecode
    mapping:
      ohmy_capability: "identify_boundary_conditions"
      openclaw_tool: "generate_boundary_tests"
    adaptation:
      - 优先生成失败测试用例
      - 标记高风险边界条件
      
  # TDD 特定扩展
  - name: tdd-red-validator
    source: custom
    capability: "ensure_tests_fail_properly"
    description: "验证测试在实现前确实失败，符合 TDD 原则"
```

### 5.3 状态同步机制

```
┌────────────────────────────────────────────────────────────┐
│                   状态同步架构                               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   Agent (Docker)          Shared FS         OMC Controller │
│   ─────────────           ─────────         ────────────── │
│        │                       │                  │        │
│        │ 1. 更新状态           │                  │        │
│        │─────────────────────▶│                  │        │
│        │   /shared/tasks/RED/ │                  │        │
│        │   US-001.status      │                  │        │
│        │                      │                  │        │
│        │                      │ 2. 状态变更事件   │        │
│        │                      │─────────────────▶│        │
│        │                      │                  │        │
│        │                      │ 3. 路由决策       │        │
│        │                      │◀─────────────────│        │
│        │                      │   next: oc-tdd   │        │
│        │                      │        -coder    │        │
│        │                      │                  │        │
│        │ 4. 通知目标 Agent    │                  │        │
│        │◀─────────────────────│                  │        │
│        │   message: TEST_READY│                  │        │
│        │                      │                  │        │
└────────────────────────────────────────────────────────────┘
```

---

## 6. 实施路线图

### Phase 1: 核心 TDD  trio (Week 1-2)
- [ ] 部署 oc-tdd-tester (RED)
- [ ] 部署 oc-tdd-coder (GREEN + REFACTOR)
- [ ] 部署 oc-tdd-lead (协调)
- [ ] 配置共享工作空间
- [ ] 跑通第一个 TDD 循环

### Phase 2: OMC 技能集成 (Week 3-4)
- [ ] 导入 Ohmy 测试设计技能
- [ ] 导入 Ohmy 实现技能
- [ ] 导入 Ohmy 重构技能
- [ ] 建立技能映射层
- [ ] 验证技能复用

### Phase 3: 按需 Agent (Week 5-6)
- [ ] 部署 oc-architect
- [ ] 部署 oc-reviewer
- [ ] 部署 oc-ops
- [ ] 配置智能激活规则

### Phase 4: 高级功能 (Week 7-8)
- [ ] 自然语言意图解析
- [ ] 智能任务路由
- [ ] 能力资产库建设
- [ ] 全流程自动化

---

## 7. 使用示例

### 示例 1: 完整功能开发

```bash
# 用户通过 OMC 接口提交需求
$ omc-cli create-feature "用户登录系统，支持邮箱密码和验证码"

# OMC 自动执行:
# 1. 意图解析 → 识别需要 3 个用户故事
# 2. 创建任务:
#    - US-001: 基础登录 (TDD)
#    - US-002: 验证码 (TDD + oc-security)
#    - US-003: 会话管理 (TDD)
# 3. 启动 TDD 循环

# 查看任务状态
$ omc-cli status
US-001: [RED] oc-tdd-tester writing tests...
US-002: [BACKLOG] waiting for US-001
US-003: [BACKLOG] waiting for US-001

# 查看详细进度
$ omc-cli logs US-001
[10:00] oc-tdd-tester: Analyzing requirements...
[10:05] oc-tdd-tester: Generated 5 test cases
[10:10] oc-tdd-tester: Running tests (expecting all to fail)...
[10:11] oc-tdd-tester: ✅ All 5 tests failed as expected
[10:12] oc-tdd-tester: Handing over to oc-tdd-coder
[10:13] oc-tdd-coder: Received test specifications
[10:15] oc-tdd-coder: Implementing login function...
```

### 示例 2: 指定使用特定技能

```bash
# 要求使用特定 Ohmy 技能
$ omc-cli create-feature "支付功能" --with-skills "ohmy-security-expert,ohmy-compliance-auditor"

# oc-security 和合规专家自动加入 TDD 流程
```

### 示例 3: 复用已有资产

```bash
# 查看可用资产
$ omc-cli list-assets
Patterns:
  - auth-jwt-pattern (from ohmy-architect)
  - test-api-pattern (from ohmy-test-designer)
  
# 使用资产开发
$ omc-cli create-feature "JWT认证" --use-asset auth-jwt-pattern
```

---

## 8. 总结

### 整合后的核心能力

1. **自然语言驱动**: 像 Oh-my-Claudecode 一样，用自然语言描述需求
2. **TDD 质量保障**: 每个功能都经过 Red-Green-Refactor 循环
3. **专业化分工**: 32+ 个专业能力按需激活
4. **资产复用**: 积累的模式、模板、经验可复用
5. **零学习曲线**: 不需要记忆复杂命令，系统自动编排

### 价值主张

> "Don't learn TDD. Don't learn OpenClaw. Just describe what you want. 
> The TDD-OMC team handles everything: testing, coding, refactoring, 
> with 32 specialized experts working together."

---

**文档版本**: v1.0-TDD-OMC  
**整合来源**: TDD + Oh-my-Claudecode + OpenClaw  
**创建时间**: 2026-03-20  
**状态**: 设计方案待实施
