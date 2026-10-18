# 从逐句分镜到成片

所有命令在仓库根目录执行，路径含空格时加引号。默认 1920×1080、25 fps；一帧 40ms。`build/` 是可删除的工作目录，原素材应另作备份。先按 README 安装 Python 依赖、ffmpeg 并下载字体。默认字体预设是 `cinematic`（得意黑 + 霞鹜文楷，缺字回退 Noto）；切回旧外观用 `PLAYBOOK_FONT_PRESET=noto`。

## 1. 建一份工作副本

```bash
mkdir -p build
cp -R examples/city-choice build/project
mkdir -p build/vo build/project/vo/timing build/transcribe
```

修改 `build/project/vo/text/*.txt` 原稿、`beats.json` 中的触发词与元素、`footage.json` 和研究来源。段落 ID 保持一致；无旁白章节写 `seconds`。分镜的文本说明见案例 `beats.md`，实际执行的是 `beats.json`。绘图节点可以独立重排，不必修改 Python。

## 2. 配音：每段一个 WAV

任何 TTS 或真人录音都可以。文件命名为 `build/vo/<段落ID>.wav`，不包括无旁白章节。无需在音频里额外补静音，工具会在每段前留 0.25 秒、后留 0.45 秒。音频已经带长静音时先裁掉，避免重复。

```bash
# 如输入格式不是 WAV，逐段转成 48 kHz PCM；把 input 替换为自己的文件。
ffmpeg -i input.m4a -ar 48000 -ac 1 -c:a pcm_s24le build/vo/00a.wav
```

工具不会合成、上传或克隆声音。仓库的时间戳可用于无音频的版式演示；实际新配音必须重做下一步。

## 3. 用 whisper.cpp 取逐字时间戳

macOS：`brew install whisper-cpp`。其他系统按 [whisper.cpp 官方说明](https://github.com/ggml-org/whisper.cpp) 编译。使用 `whisper-cli` 和 `large-v3-turbo`，不使用 Python 的 openai-whisper 包。

```bash
mkdir -p build/models
curl -fL --retry 3 https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin -o build/models/ggml-large-v3-turbo.bin
# 使用 bash，逐段执行；转录用的 16 kHz 文件不替代混音用的 48 kHz 原音。
bash -c 'for wav in build/vo/*.wav; do
  id=$(basename "$wav" .wav)
  ffmpeg -v error -y -i "$wav" -ar 16000 -ac 1 "build/transcribe/$id.wav"
  whisper-cli -m build/models/ggml-large-v3-turbo.bin -l zh -f "build/transcribe/$id.wav" -ojf -ml 1 -of "build/project/vo/timing/$id"
done'
```

`-ojf -ml 1` 输出含 `transcription[].text` 和毫秒 `offsets.from/to` 的细粒度 JSON。自动识别会出现同音字、末尾幻觉；检查时间覆盖和重复内容。字幕始终取原稿，识别只用于对齐。公开文件时只保留这两个字段，剔除模型路径、系统信息和日志。

## 4. 建段落时间轴，再对齐关键词

```bash
python tools/build_edl.py --spec build/project/beats.json --wav-dir build/vo --output build/edl.json
python tools/align.py --spec build/project/beats.json --edl build/edl.json --output build/timeline.json
```

`edl.json` 用真实 WAV 时长累计段落和旁白落点；无旁白章节默认在规格中设 2.2 秒。对齐器合并相邻阿拉伯数字 token，转换中文整数读法，再以原稿字符对齐；错字或漏字在两侧锚点间插值。`timeline.json` 保存修复清单，逐项听检，插值不能代替人工校对。找不到触发词会直接报错。相同词重复触发时依分镜顺序匹配下一次出现。

## 5. 获取素材和卡片静帧

```bash
bash tools/fetch_footage.sh build/project/footage.json build/footage
python tools/prepare_stills.py --spec build/project/beats.json --footage build/footage --output build/stills
python tools/build_edl.py --timeline build/timeline.json --footage build/footage --output build/v1_edl.json
```

搜索新素材时，在 Pexels 搜索页的浏览器控制台粘贴 `tools/pexels_harvest.js`，从 `__NEXT_DATA__` 导出候选的 ID、时长、页面和 CDN 链接；人工挑选后填上 `beats` 用途再下载。网站数据结构或 CDN 可能变化，失败时重新采集。脚本不使用账号、cookie、API token 或私有接口。

卡片静帧默认从第 2 秒抽取，生成的 JPG 只放本机工作目录。实拍 EDL 从 F 类型切点生成；B 讲解板期间延续前一个实拍作底。素材不够长时从头分片重用，不能凭空生成不存在的帧。源片音轨不进入成片。

## 6. 渲染图形、字幕与 SRT

```bash
# 先抽查几个词的入场；指定 --frames 时只写这些帧。
python tools/render.py --spec build/project/beats.json --timeline build/timeline.json --fonts build/fonts --stills build/stills --output build/sample --frames 0,1,4,18,150
# 正式渲染时不加 --frames。
python tools/render.py --spec build/project/beats.json --timeline build/timeline.json --fonts build/fonts --stills build/stills --output build/layers
```

得到 `gfx/%05d.png`、`subs/%05d.png` 与 `subs.srt`。F 图形层透明，B 图形层不透明。全片两层序列需要数 GB 磁盘；工具把稳定帧硬链接到相同图像以减少实际占用，复制到其他文件系统后可能变大。两层序列保持整片时长，不能只取有字的帧。字幕的数字会按中文整数读法显示，点数、年份逐字读等特殊读法建议直接写中文。

## 7. 混音

自行准备有使用权的背景音乐，存为 `build/music.wav`。工具循环音乐至片长，先降低 15 dB，以旁白做侧链（threshold 0.015、ratio 10、attack 30ms、release 600ms），最后 1.2 秒淡出；按实测第一遍参数做第二遍 loudnorm，目标 −14 LUFS、真峰值 −1 dBTP。

```bash
python tools/mix.py --edl build/edl.json --wav-dir build/vo --music build/music.wav --output build/final_mix.wav
ffmpeg -hide_banner -i build/final_mix.wav -af loudnorm=I=-14:TP=-1:print_format=json -f null -
```

`final_mix.loudnorm.json` 是归一化前的测量值；验收时看最后一条命令的 `input_i/input_tp`。音乐的录制电平会影响实际压低程度，需试听；禁止靠大幅削波换响度。

## 8. 默认 ffmpeg 合成

```bash
python tools/compose_ffmpeg.py --edl build/v1_edl.json --footage build/footage --gfx 'build/layers/gfx/%05d.png' --subs 'build/layers/subs/%05d.png' --mix build/final_mix.wav --duration 20 --output build/preview.mp4
python tools/compose_ffmpeg.py --edl build/v1_edl.json --footage build/footage --gfx 'build/layers/gfx/%05d.png' --subs 'build/layers/subs/%05d.png' --mix build/final_mix.wav --output build/final.mp4
```

默认 `libx264` + AAC，macOS 可加 `--hw` 切换 `h264_videotoolbox`。先逐镜规范化帧率、尺寸和方形像素，再硬切拼接，上叠图形、字幕和混音。音画片尾淡出默认 1.2 秒；视频可用 `--fade-seconds` 调整。`--duration 20` 只截预览，仍使用整片的淡黑位置。素材不足时补最后一帧以保持 EDL 时长。

## 9. 审片与交付

```bash
python tools/review.py --timeline build/timeline.json --edl build/v1_edl.json --footage build/footage --layers build/layers --output build/review
python tools/review.py --timeline build/timeline.json --edl build/v1_edl.json --footage build/footage --layers build/layers --output build/review-boards --boards
ffmpeg -v error -xerror -i build/final.mp4 -f null -
ffprobe -v error -show_entries format=duration -of default=nw=1 build/final.mp4
```

常规拼图取 beat 后 0.7 秒，讲解板版取 1.2 秒；短 beat 另加中点，索引记录抽样是否跨过切点。拼图用原始图层，片尾淡黑以最终 MP4 为准。检查所有字幕、数字来源、入场时机、四城颜色、短镜头与片尾，然后完整看一遍成片。编辑器接手看 [后端说明](03-backends.md)。

## 复现原案例的验收

示例保留 4690 帧的原段落 EDL、31 镜头的 `v1_edl.json` 与净化后的逐字时间戳；不包含原录音。`tests/check_equivalence.py` 读取用户显式传入的原制作目录，重新运行新对齐器和渲染器，比较图形/字幕各十帧，写入不带本机路径的 `tests/equivalence.json`。不要把原工程、日志或媒体复制进公开仓库。
