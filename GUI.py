import tkinter as tk
from tkinter import filedialog,messagebox
import detect
import os
import subprocess
import sys
import extract
import translate
import srt
# Initialize global variables to avoid unbound errors
audio_video_path = None
background_path = None
srt_path = None

def init_window():
    root = tk.Tk()
    root.title("ACM 视频处理工具")
    root.geometry("600x400")
    root.resizable(False, False)
    audio_video_btn= tk.Button(root, text="上传音频/视频文件", command=upload_audio_video)
    audio_video_btn.pack(pady=10)
    background_image_btn = tk.Button(root, text="上传背景图片", command=upload_background_image)
    background_image_btn.pack(pady=10)
    srt_btn = tk.Button(root, text="上传字幕文件", command=upload_srt)
    srt_btn.pack(pady=10)
    tk.Label(root, text="请输入语言代码:").pack(pady=10)
    
    global lang
    lang = tk.Entry(root)
    lang.pack(pady=10)
    process_F_btn = tk.Button(root, text="处理 -F", command=process_F)
    process_F_btn.pack(pady=10)
    process_S_btn = tk.Button(root, text="处理 -S", command=process_S)
    process_S_btn.pack(pady=10)
    process_M_btn = tk.Button(root, text="处理 -M", command=process_M)
    process_M_btn.pack(pady=10)
    return root
def upload_audio_video():
    filepath = filedialog.askopenfilename(
        title="选择要上传的文件",
        filetypes=[("媒体文件", "*.mp4 *.mp3 *.wav *.mkv *.avi *.flac"), ("所有文件", "*.*")]
    )
    if filepath:
        global audio_video_path
        audio_video_path = filepath
        messagebox.showinfo("文件上传", f"已上传文件: {os.path.basename(filepath)}")
def upload_background_image():
    filepath = filedialog.askopenfilename(
        title="选择背景图片",
        filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp"), ("所有文件", "*.*")]
    )
    if filepath:
        global background_path
        background_path = filepath
        messagebox.showinfo("图片上传", f"已上传背景图片: {os.path.basename(filepath)}")
def upload_srt():
    filepath = filedialog.askopenfilename(
        title="选择字幕文件",
        filetypes=[("字幕文件", "*.srt"), ("所有文件", "*.*")]
    )
    if filepath:
        global srt_path
        srt_path = filepath
        messagebox.showinfo("字幕上传", f"已上传字幕文件: {os.path.basename(filepath)}")
def process_F():
    global background_path
    if not audio_video_path:
        messagebox.showerror("错误", "请先上传音频/视频文件")
    language_code=lang.get().strip()
    if not language_code:
        language_code = "ja"  # 默认语言为日语
    if not background_path: #ignore
        background_path = None
    messagebox.showinfo("信息", "处理中请稍后...")
    #whisper 读取字幕
    segments = extract.transcribe_audio(audio_video_path, language_code)
    original_srt, subs = extract.segments_to_srt(segments)
    with open("original.srt", "w", encoding="utf-8") as f:
        f.write(original_srt)
    print(f"[完成] 使用语言: {language_code}")
    #加载翻译模型
    translate.load_model()
    print(f"模型加载成功")
    #逐句翻译
    for sub in subs:
        sub.content = translate.translate_text(sub.content, src_lang=language_code, tgt_lang="zh")
    print(f"[翻译] 完成翻译 {len(subs)} 个字幕段")
    #转回 SRT 格式并保存
    translated_srt = srt.compose(subs)
    with open("translated.srt", "w", encoding="utf-8") as f:
        f.write(translated_srt)
    print(f"[翻译] 完成翻译，输出到 translated.srt")
    if background_path:
        print(f"[背景] 将使用自定义背景图片: {background_path}")
    detect.prepare_video_with_subtitle(audio_video_path, "translated.srt", "output.mp4", background_image=background_path)
    print(f"[完成] 最终输出文件: output.mp4")
    messagebox.showinfo("完成", "处理完成，请在程序所在目录下查看")
def process_S():
    if not audio_video_path:
        messagebox.showerror("错误", "请先上传音频/视频文件")
    language_code = lang.get().strip()
    if not language_code:
        language_code = "ja"  # 默认语言为日语
    #whisper 读取字幕
    messagebox.showinfo("信息", "处理中请稍后...")
    segments = extract.transcribe_audio(audio_video_path, language_code)
    original_srt, subs = extract.segments_to_srt(segments)
    with open("original.srt", "w", encoding="utf-8") as f:
        f.write(original_srt)
    print(f"[完成] 使用语言: {language_code}")
    #加载翻译模型
    translate.load_model()
    print(f"模型加载成功")
    #逐句翻译
    for sub in subs:
        sub.content = translate.translate_text(sub.content, src_lang=language_code, tgt_lang="zh")
    print(f"[翻译] 完成翻译 {len(subs)} 个字幕段")
    #转回 SRT 格式并保存
    messagebox.showinfo("完成", "处理完成，请在程序所在目录下查看")
def process_M():
    global background_path
    if not audio_video_path:
        messagebox.showerror("错误", "请先上传音频/视频文件")
    if not srt_path:
        messagebox.showerror("错误", "请先上传字幕文件")
    if not background_path:  # ignore
        background_path = None
    messagebox.showinfo("信息", "处理中请稍后...")
    detect.prepare_video_with_subtitle(audio_video_path, srt_path, "output.mp4", background_image=background_path)
    print(f"[完成] 最终输出文件: output.mp4")
    messagebox.showinfo("完成", "处理完成，请在程序所在目录下查看")
    
root=init_window()
root.mainloop()