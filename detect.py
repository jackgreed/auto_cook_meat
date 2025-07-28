import os
import subprocess



def is_video_file(path):
    video_exts = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    return os.path.splitext(path)[-1].lower() in video_exts

def convert_audio_to_video(audio_path, output_path, resolution=(1280, 720), color=(0, 0, 0), background_image=None):
    if background_image and os.path.exists(background_image):
        print(f"[背景] 使用自定义图片: {background_image}")
        
        command_copy = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", background_image,
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "copy",  # 尝试直接复制原音频
            "-vf", f"scale={resolution[0]}:{resolution[1]}:force_original_aspect_ratio=increase,crop={resolution[0]}:{resolution[1]},fps=24",
            "-pix_fmt", "yuv420p",  # 确保像素格式兼容性
            "-profile:v", "baseline",  # 使用基线配置以提高兼容性
            "-level", "3.0",
            "-shortest",
            output_path
        ]
    else:
        print("[背景] 使用纯色背景")
        # 使用纯色背景
        command_copy = [
            "ffmpeg",
            "-y",
            "-i", audio_path,
            "-f", "lavfi",
            "-i", f"color=c=black:size={resolution[0]}x{resolution[1]}:rate=24",
            "-c:v", "libx264",
            "-c:a", "copy",  # 尝试直接复制原音频
            "-shortest",
            output_path
        ]
    
    try:
        subprocess.run(command_copy, check=True, capture_output=True)
        print("[音频] 使用无损复制模式")
    except subprocess.CalledProcessError:
        # 如果无损复制失败，使用高质量重编码
        print("[音频] 无损复制失败，使用高质量重编码模式")
        if background_image and os.path.exists(background_image):
            command_hq = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-i", background_image,
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-b:a", "320k",  # 使用320kbps高质量AAC编码
                "-vf", f"scale={resolution[0]}:{resolution[1]}:force_original_aspect_ratio=increase,crop={resolution[0]}:{resolution[1]},fps=24",
                "-pix_fmt", "yuv420p",  # 确保像素格式兼容性
                "-profile:v", "baseline",  # 使用基线配置以提高兼容性
                "-level", "3.0",
                "-shortest",
                output_path
            ]
        else:
            command_hq = [
                "ffmpeg",
                "-y",
                "-i", audio_path,
                "-f", "lavfi",
                "-i", f"color=c=black:size={resolution[0]}x{resolution[1]}:rate=24",
                "-c:v", "libx264",
                "-c:a", "aac",
                "-b:a", "320k",  # 使用320kbps高质量AAC编码
                "-shortest",
                output_path
            ]
        subprocess.run(command_hq, check=True)

def embed_soft_subtitle(input_video_path, srt_path, output_path):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_video_path,
        "-i", srt_path,
        "-c", "copy",
        "-c:s", "mov_text",  # 使用软字幕
        "-metadata:s:s:0", "language=chi",  
        output_path
    ]
    subprocess.run(command, check=True)

def prepare_video_with_subtitle(input_path, srt_path, output_path, background_image=None):
    temp_video = "temp_video.mp4"

    if is_video_file(input_path):
        print("[信息] 检测到视频文件，直接嵌入字幕")
        embed_soft_subtitle(input_path, srt_path, output_path)
    else:
        print("[信息] 检测到音频文件，正在转为视频...")
        convert_audio_to_video(input_path, temp_video, background_image=background_image)
        print("[信息] 音频转视频完成，正在嵌入字幕...")
        embed_soft_subtitle(temp_video, srt_path, output_path)
        os.remove(temp_video)
        print("[信息] 临时文件已清理")

    print(f"[完成] 最终输出文件: {output_path}")
