import detect
import os
import subprocess
import download
import sys
import extract
import translate

# -S 只输出原字幕+翻译字幕
# -F 输出最终视频文件
# -M 用用户提供的视频文件与翻译字幕嵌合
if len(sys.argv)< 3:
    print("e.g: python acm.py -F <音频文件路径> <语言代码> [背景图片路径]")
    print("e.g: python acm.py -S <音频文件路径> <语言代码> ")
    print("e.g: python acm.py -M <视频文件路径> <翻译字幕文件路径> [背景图片路径]")
    sys.exit(1)
if sys.argv[1] == "-F":
    file_name= sys.argv[2]
    lang="ja" if len(sys.argv) < 4 else sys.argv[3]
    background_image = sys.argv[4] if len(sys.argv) > 4 else None
    #whisper 读取字幕
    segments = extract.transcribe_audio(file_name, lang)
    original_srt, subs = extract.segments_to_srt(segments)
    with open("original.srt", "w", encoding="utf-8") as f:
        f.write(original_srt)
    print(f"[完成] 使用语言: {lang}")
    #加载翻译模型
    translate.load_model()
    print(f"模型加载成功")
    #逐句翻译
    for sub in subs:
        sub.content = translate.translate_text(sub.content, src_lang=lang, tgt_lang="zh")
    print(f"[翻译] 完成翻译 {len(subs)} 个字幕段")
    #转回 SRT 格式并保存
    import srt
    translated_srt = srt.compose(subs)
    with open("translated.srt", "w", encoding="utf-8") as f:
        f.write(translated_srt)
    print(f"[翻译] 完成翻译，输出到 translated.srt")
    if background_image:
        print(f"[背景] 将使用自定义背景图片: {background_image}")
    detect.prepare_video_with_subtitle(file_name, "translated.srt", "output.mp4", background_image)
    print(f"[完成] 最终输出文件: output.mp4")
    sys.exit(0)
elif sys.argv[1]=="-S":
    file_name= sys.argv[2]
    lang="ja" if len(sys.argv) < 4 else sys.argv[3]
    #whisper 读取字幕
    segments = extract.transcribe_audio(file_name, lang)
    original_srt, subs = extract.segments_to_srt(segments)
    with open("original.srt", "w", encoding="utf-8") as f:
        f.write(original_srt)
    print(f"[完成] 使用语言: {lang}")
    #加载翻译模型
    translate.load_model()
    print(f"模型加载成功")
    #逐句翻译
    for sub in subs:
        sub.content = translate.translate_text(sub.content, src_lang=lang, tgt_lang="zh")
    print(f"[翻译] 完成翻译 {len(subs)} 个字幕段")
    #转回 SRT 格式并保存
    import srt
    translated_srt = srt.compose(subs)
    with open("translated.srt", "w", encoding="utf-8") as f:
        f.write(translated_srt)
    print(f"[翻译] 完成翻译，输出到 translated.srt")
    sys.exit(0)
elif sys.argv[1]=="-M":
    file_name= sys.argv[2]
    srt_file = sys.argv[3]
    background_image = sys.argv[4] if len(sys.argv) > 4 else None
    detect.prepare_video_with_subtitle(file_name, srt_file, "output.mp4", background_image)
else:
    print("未知参数，请使用 -S, -F 或 -M")
    sys.exit(1)