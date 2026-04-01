# Video OCR - 视频画面文字识别

从视频画面中识别文字（字幕、PPT、屏幕文字等）

## 功能特性

- ✅ 提取视频画面中的文字内容
- ✅ 支持字幕条、PPT、屏幕录制
- ✅ 自动去重和时序整理
- ✅ 结合语音转文字，生成完整文档

## 工作流程

```
视频文件 → 提取关键帧 → OCR识别 → 去重整理 → 输出文字
```

## 依赖

- ffmpeg (提取帧)
- PaddleOCR / Tesseract (文字识别)
- OpenCV (图像处理)

## 安装

```bash
# PaddleOCR (推荐，中文效果好)
pip install paddleocr paddlepaddle --break-system-packages

# 或 Tesseract (备选)
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```
