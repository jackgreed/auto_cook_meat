import whisper

def transcribe_audio(file_path, language="ja"):
    model = whisper.load_model("large")  # 使用large模型
    print(f"[识别] 正在识别：{file_path}")
    # 指定语言可以避免多语言混淆
    result = model.transcribe(file_path, language=language)
    return result["segments"]

import srt
from datetime import timedelta

def segments_to_srt(segments):
    subs = []
    for i, seg in enumerate(segments):
        subs.append(srt.Subtitle(
            index=i + 1,
            start=timedelta(seconds=seg["start"]),
            end=timedelta(seconds=seg["end"]),
            content=seg["text"]
        ))
    return srt.compose(subs), subs

def save_srt_file(srt_content, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"[保存] SRT 文件已保存到：{output_path}")

