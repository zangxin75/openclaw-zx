"""
Video to Text - 视频转文字模块

支持从视频文件提取文字内容
"""

import os
import subprocess
import tempfile
from pathlib import Path

def extract_audio(video_path: str, output_audio: str = None) -> str:
    """
    从视频提取音频
    
    Args:
        video_path: 视频文件路径
        output_audio: 输出音频路径 (可选)
        
    Returns:
        音频文件路径
    """
    if output_audio is None:
        output_audio = video_path.rsplit(".", 1)[0] + ".wav"
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio,
        "-y",
        "-hide_banner",
        "-loglevel", "error"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"音频提取失败: {result.stderr}")
    
    return output_audio


def transcribe_audio(audio_path: str, model: str = "base", language: str = "zh") -> str:
    """
    使用 faster-whisper 转录音频
    
    Args:
        audio_path: 音频文件路径
        model: 模型大小 (tiny, base, small, medium, large-v3)
        language: 语言代码 (zh, en, ja, auto)
        
    Returns:
        转录文字
    """
    stt_script = os.path.expanduser("~/.openclaw/workspace/tools/stt.sh")
    
    if not os.path.exists(stt_script):
        raise FileNotFoundError(f"未找到 stt.sh 脚本: {stt_script}")
    
    result = subprocess.run(
        ["bash", stt_script, audio_path, model, language],
        capture_output=True,
        text=True,
        timeout=300
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"转录失败: {result.stderr}")
    
    return result.stdout.strip()


def transcribe_video(video_path: str, model: str = "base", language: str = "zh") -> str:
    """
    视频转文字 - 一键完成
    
    Args:
        video_path: 视频文件路径
        model: 模型大小
        language: 语言代码
        
    Returns:
        转录文字
        
    Example:
        >>> text = transcribe_video("video.mp4")
        >>> print(text)
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 提取音频
        audio_path = os.path.join(tmp_dir, "audio.wav")
        extract_audio(video_path, audio_path)
        
        # 转录音频
        text = transcribe_audio(audio_path, model, language)
        
        return text


__all__ = ["extract_audio", "transcribe_audio", "transcribe_video"]
