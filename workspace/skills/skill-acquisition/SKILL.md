# 技能自动获取协议

## 发现新技能的渠道

1. **ClawHub** - https://clawhub.com
2. **GitHub** - 搜索 openclaw, mcp, agent skills
3. **社区文章** - 如刘飞的龙虾经验分享
4. **用户需求** - 用户提到的功能需求

## 技能评估标准

| 评估项 | 标准 |
|--------|------|
| **必要性** | 是否解决常见问题？ |
| **可行性** | 能否在本地/API 实现？ |
| **维护性** | 是否需要频繁更新？ |
| **安全性** | 是否有风险？ |

## 安装流程

```bash
# 方法1: ClawHub
npx clawhub install <skill-name>

# 方法2: 手动安装
git clone <skill-repo> ~/.openclaw/workspace/skills/<skill-name>

# 方法3: 自己编写
mkdir ~/.openclaw/workspace/skills/<skill-name>
# 创建 SKILL.md 和相关脚本
```

## 当前技能清单（15个）

| 技能 | 状态 | 来源 |
|------|------|------|
| voice-stt | ⚠️ 需API | 预装 |
| voice-transcribe | ⚠️ 需API | 预装 |
| agent-orchestrator | ✅ 可用 | 预装 |
| github | ✅ 可用 | 预装 |
| pdf | ✅ 可用 | 预装 |
| summarizer | ✅ 可用 | 预装 |
| role-based-collaboration | ✅ 新建 | 自研 |

## 待获取技能

- [ ] 本地语音识别（无需API）
- [ ] 文件自动同步
- [ ] 项目模板生成
- [ ] 代码审查助手
