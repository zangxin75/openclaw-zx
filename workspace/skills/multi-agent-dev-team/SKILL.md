---
name: multi-agent-dev-team
description: |
  2-agent collaborative software development workflow. PM Agent orchestrates projects and breaks down requirements, Dev Agent implements code and tests functionality. Build complete software projects from simple descriptions.
---

# Multi-Agent Dev Team

Build software with AI agents that collaborate like a real dev team.

## Overview

Provides two collaborative AI agents:
- **PM Agent**: Orchestrates projects, breaks down requirements, coordinates the Dev agent
- **Dev Agent**: Implements code, tests functionality, commits to Git

## Quick Start

### Installation

```bash
npx clawhub install multi-agent-dev-team
```

### Configuration

Add to `~/.openclaw/config.yaml`:

```yaml
agents:
  multi-agent-pm:
    soul: ~/.openclaw/skills/multi-agent-dev-team/agents/pm-agent/SOUL.md
    model: anthropic/claude-sonnet-4-5-20250929
    
  multi-agent-dev:
    soul: ~/.openclaw/skills/multi-agent-dev-team/agents/dev-agent/SOUL.md
    model: google/gemini-2.5-flash
```

### Usage

```bash
openclaw chat --agent multi-agent-pm
```

Then simply describe what you want to build!

## Features

- 🤝 **2 collaborative agents** (PM + Dev)
- 🏗️ **Project orchestration** by PM agent
- 💻 **Code implementation** by Dev agent
- 📝 **Git integration** with clean commits
- 🎯 **Iterative refinement** (up to 3 rounds)

## How It Works

```
You (Director)
    ↓
    ↓ Describe project
    ↓
PM Agent
    ↓ Create task spec
    ↓ Spawn Dev agent
    ↓
Dev Agent
    ↓ Implement code
    ↓ Test & commit
    ↓
PM Agent
    ↓ Review deliverables
    ↓ Report completion
    ↓
You receive working code! ✨
```

## What Can You Build?

### Perfect For:
- ✅ Landing pages and marketing sites
- ✅ React/Next.js applications
- ✅ Component libraries
- ✅ Prototypes and MVPs
- ✅ Developer tools
- ✅ Documentation sites

## Requirements

- OpenClaw 2026.2.0 or later
- At least one LLM provider configured (Anthropic/Google/OpenAI)
- Git installed (for Dev agent)
- Node.js 18+ (for web projects)

## Recommended Models

**PM Agent:**
- `anthropic/claude-sonnet-4-5-20250929` (best reasoning)
- `google/gemini-2.5-flash` (fast & efficient)

**Dev Agent:**
- `google/gemini-2.5-flash` (recommended - fast code generation)
- `anthropic/claude-sonnet-4-5` (higher quality)
