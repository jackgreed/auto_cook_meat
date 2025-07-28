### auto-cook-meat
正如名字所述: 自动-烤-肉,此程序的目的即是自动对音视频烤肉(即翻译为中文)
## how it works
使用whisper自动从音视频文件中生成源语言字幕->使用facebook/m2m100_418M对获取的字幕进行翻译->使用ffmpeg将字幕以软字幕形式嵌入视频文件中
## what should I perpare
# 配置python环境
python>3.10
# 下载库
pip install -r requirements.txt
# 下载模型
python download.py
# 跑
python acm.py args
## what are args
python acm.py -F <file_dict> <language_code> [background_image_dict]

一步到位,直接输出output.mp4

python acm.py -S <file_dict> <language_code>

中途停止,生成原字幕+翻译字幕以供人工校对

Python acm.oy -M <file_dict> <srt_dict> [backgroud_image_dict]

用音视频文件与以生成好的翻译字幕文件合成目标视频
