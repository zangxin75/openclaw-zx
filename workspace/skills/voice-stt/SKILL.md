---
name: voice-stt
description: 语音消息自动转文字（本地 faster-whisper，完全免费）
---

# voice-stt

自动转录语音消息为文字。**完全本地运行，无需 API Key，永久免费。**

## 方案对比

| 方案 | 成本 | 网络要求 | 中文效果 | 推荐度 |
|------|------|----------|----------|--------|
| **faster-whisper (本地)** | 免费 | 无需联网 | ⭐⭐⭐⭐ | ✅ 推荐 |
| AssemblyAI | 免费额度$50 | 需联网 | ⭐⭐⭐⭐⭐ | 备选 |

## 使用方法

### 1. 本地 faster-whisper（推荐）

```bash
# 转录语音文件
~/.openclaw/workspace/tools/stt.sh <音频文件> [模型大小] [语言]

# 示例
~/.openclaw/workspace/tools/stt.sh voice.opus           # 默认 base 模型，中文
~/.openclaw/workspace/tools/stt.sh voice.opus base zh   # 同上，显式指定
~/.openclaw/workspace/tools/stt.sh voice.mp3 small auto # small模型，自动语言检测
```

**模型大小对比：**
- `tiny`: 最快，准确度一般 (~39MB)
- `base`: 平衡方案，推荐 (~74MB) ✅
- `small`: 更好准确度，稍慢 (~244MB)
- `medium`: 高准确度 (~769MB)
- `large-v3`: 最高准确度，最慢 (~1.5GB)

### 2. AssemblyAI（需 API Key）

如需云端更高准确度：
```bash
echo "AAI_API_KEY=你的key" > ~/.openclaw/workspace/tools/assemblyai/.env
node ~/.openclaw/workspace/tools/stt_assemblyai.js <音频文件>
```

## 支持格式

ogg, opus, mp3, m4a, wav, webm, mp4

## 自动处理

在 Feishu/微信等收到语音消息时，OpenClaw 会自动调用此 skill 进行转录。

## 技术栈

- **STT**: faster-whisper (OpenAI Whisper 的 CTranslate2 加速版)
- **运行环境**: 本地 CPU/GPU，无需联网
- **首次使用**: 会自动下载模型文件 (~74MB for base)
