# Video-to-Text - 视频转文字

从视频文件中提取音频并转录为文字。支持抖音、YouTube、本地视频等。

## 功能特性

- ✅ 支持多种视频格式 (mp4, webm, mov, avi 等)
- ✅ 本地运行，无需 API Key，完全免费
- ✅ 使用 faster-whisper，中文效果优秀
- ✅ 支持抖音视频下载并转录
- ✅ 支持本地视频文件

## 安装依赖

```bash
# 1. ffmpeg (必需)
sudo apt-get install ffmpeg  # Ubuntu/Debian
brew install ffmpeg          # macOS

# 2. yt-dlp (下载在线视频用)
pip install yt-dlp --break-system-packages

# 3. faster-whisper (应该已经安装)
# 如果未安装，参考 voice-stt skill
```

## 默认下载目录

视频文件和转录结果默认保存到：`/mnt/d/openclaw-download/`

### 修改下载目录

**方式 1: 环境变量**
```bash
export OPENCLAW_DOWNLOAD_DIR="/your/custom/path"
python3 ~/.openclaw/workspace/tools/douyin_to_text.py 'https://...'
```

**方式 2: 修改脚本** (永久生效)
编辑 `~/.openclaw/workspace/tools/douyin_to_text.py`:
```python
DEFAULT_DOWNLOAD_DIR = "/your/custom/path"
```

## 使用方法

### 方式 1: 本地视频转文字

```bash
# 基本用法
~/.openclaw/workspace/tools/video_to_text.sh <视频文件>

# 指定模型和语言
~/.openclaw/workspace/tools/video_to_text.sh video.mp4 small zh

# 示例
~/.openclaw/workspace/tools/video_to_text.sh ~/Downloads/video.mp4
```

### 方式 2: 抖音视频转文字

```bash
# 基本用法 (仅转录，不保存视频)
python3 ~/.openclaw/workspace/tools/douyin_to_text.py <抖音链接>

# 转录并保存视频
python3 ~/.openclaw/workspace/tools/douyin_to_text.py \
    'https://v.douyin.com/xxxxx' --save-video

# 指定模型和语言
python3 ~/.openclaw/workspace/tools/douyin_to_text.py \
    'https://v.douyin.com/xxxxx' --model small --lang zh
```

### 方式 3: Python API

```python
import sys
sys.path.insert(0, '~/.openclaw/workspace/skills/video-to-text')

from video_to_text import transcribe_video

# 转录本地视频
text = transcribe_video("/path/to/video.mp4")
print(text)

# 指定模型和语言
text = transcribe_video("video.mp4", model="small", language="zh")
```

## 工作流程

```
视频文件/链接 → 下载(如需要) → 提取音频 → 语音转文字 → 输出文本
```

## 模型选择

| 模型 | 准确度 | 速度 | 大小 | 推荐场景 |
|------|--------|------|------|----------|
| tiny | ⭐⭐ | 最快 | ~39MB | 快速预览 |
| base | ⭐⭐⭐ | 快 | ~74MB | **日常使用** ✅ |
| small | ⭐⭐⭐⭐ | 中等 | ~244MB | 高质量需求 |
| medium | ⭐⭐⭐⭐⭐ | 慢 | ~769MB | 专业场景 |
| large-v3 | ⭐⭐⭐⭐⭐ | 最慢 | ~1.5GB | 最高质量 |

## 语言代码

- `zh` - 中文 (默认)
- `en` - 英文
- `ja` - 日语
- `ko` - 韩语
- `auto` - 自动检测

## 使用示例

### 示例 1: 本地视频

```bash
cd ~/.openclaw/workspace/skills/video-to-text

~/.openclaw/workspace/tools/video_to_text.sh \
    ~/Videos/my_video.mp4 base zh
```

输出：
```
🎬 视频转文字
视频文件: /home/user/Videos/my_video.mp4
模型: base
语言: zh

📤 步骤 1/3: 提取音频...
✅ 音频提取完成

🎯 步骤 2/3: 转录音频...
✅ 转录完成

📝 转录结果:
========================================
大家好，今天我们来讨论...
========================================
```

### 示例 2: 抖音视频

```bash
python3 ~/.openclaw/workspace/tools/douyin_to_text.py \
    'https://v.douyin.com/ABcdEfG' small zh
```

输出：
```
🎬 抖音视频转文字
==================================================

📁 工作目录: /tmp/xyz123

==================================================
步骤 1/4: 下载视频
==================================================
📥 正在下载视频...
   URL: https://v.douyin.com/ABcdEfG
✅ 下载完成: /tmp/xyz123/video.mp4

==================================================
步骤 2/4: 提取音频
==================================================
🎵 正在提取音频...
✅ 音频提取完成

==================================================
步骤 3/4: 语音转文字
==================================================
🎯 正在转录音频...
   模型: small, 语言: zh
✅ 转录完成

📝 转录结果:
--------------------------------------------------
今天给大家分享一个非常实用的技巧...
--------------------------------------------------
💾 结果已保存到: transcription.txt
```

## 故障排除

### 问题: ffmpeg 未找到

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# 验证
ffmpeg -version
```

### 问题: yt-dlp 未找到

```bash
pip install yt-dlp --break-system-packages

# 验证
yt-dlp --version
```

### 问题: 抖音视频下载失败

1. 检查链接是否有效
2. 尝试使用浏览器的"复制链接"功能获取完整链接
3. 某些视频可能需要登录才能下载

### 问题: 转录结果为空

1. 检查视频是否有音频轨道
2. 尝试使用更大的模型 (small/medium)
3. 检查语言设置是否正确

## 文件位置

```
~/.openclaw/workspace/
├── skills/video-to-text/
│   ├── SKILL.md          # 本文档
│   └── __init__.py       # Python API
│
└── tools/
    ├── video_to_text.sh  # 本地视频转文字脚本
    └── douyin_to_text.py # 抖音视频转文字脚本
```

## 依赖的技能

- `voice-stt` - 提供 faster-whisper 语音转文字功能

## 参考

- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- yt-dlp: https://github.com/yt-dlp/yt-dlp
