# 合成与剪辑后端

## ffmpeg：默认且不依赖剪辑软件

见 [流水线第 8 步](02-pipeline.md)。输入为实拍 EDL、ID 命名的源片、两层 RGBA PNG 序列和最终 WAV；也可将 `--gfx` / `--subs` 指向带 alpha 的 MOV。输出 H.264 / AAC MP4，含整片末尾 1.2 秒淡黑。软件编码跨平台；`--hw` 需要 macOS 的 VideoToolbox。CLI 会检查 V1 是否连续并覆盖片长。

## 把透明序列封成 MOV

FCPXML 和 Resolve 脚本都使用两条透明 MOV，避免编辑器导入数千张图片。以下为跨平台软件编码方案，可能较慢但不需要专有编码器：

```bash
ffmpeg -y -framerate 25 -start_number 0 -i build/layers/gfx/%05d.png -an -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le build/gfx.mov
ffmpeg -y -framerate 25 -start_number 0 -i build/layers/subs/%05d.png -an -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le build/subs.mov
```

可用 `ffprobe -v error -show_entries stream=codec_name,pix_fmt,nb_frames -of json build/gfx.mov` 检查；需保留 alpha，不能把这两层编码成普通 H.264。支持的 Mac 可尝试 `-c:v prores_videotoolbox -profile:v 4444 -pix_fmt bgra`，具体以本机 ffmpeg 编码器帮助为准。

## FCPXML 1.10

```bash
python tools/export_fcpxml.py --edl build/v1_edl.json --footage build/footage --gfx build/gfx.mov --subs build/subs.mov --mix build/final_mix.wav --srt build/layers/subs.srt --output build/timeline.fcpxml
python tests/check_fcpxml.py build/timeline.fcpxml build/v1_edl.json
```

主 spine 是 V1 实拍，连接 lane 1、2 为图形和字幕，lane −1 为混音。每个源片只有一个 asset 资源，多次使用以多个剪辑引用；另有三个图层资源，时间用精确有理数秒。导出器探测存在的媒体以记录原生尺寸和帧率，缺失文件时按 EDL 留下可重连占位信息。资源 URI 相对 XML 保存，移动时把整个 `build/` 一起移动；不能只发 XML。SRT 复制到 XML 旁，和视频字幕层二选一使用，避免双字幕。

**Final Cut Pro**：先建资源库，再 `File > Import > XML` 选择 `timeline.fcpxml`，缺素材时 Relink Files；确认项目是 1080p / 25 fps。检查图形和字幕合成到 V1 上、混音存在、短镜头没有空帧。该格式需要支持 FCPXML 1.10 的版本；Final Cut 自身导出的 1.10+ 文件可能为 `.fcpxmld` bundle，本工具输出单文件互换 XML。[Apple 的 XML 导入说明](https://support.apple.com/en-am/guide/final-cut-pro/verdbd66ae/mac)。

**DaVinci Resolve 免费版**：无需脚本。在 Edit 页 `File > Import Timeline > Import AAF, EDL, XML`，选择 FCPXML，使用 25 fps、自动导入源片，必要时手动指向素材目录。检查三条视频轨和混音轨；黑底透明异常时检查 Clip Attributes 的 Alpha Mode（先试 Straight）。XML 导入无需 Studio；编解码支持随平台和版本不同，遇到原片解码限制先转码，再重连。菜单以安装版本为准。[Blackmagic 官方手册与下载](https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion)。

**Premiere Pro**：不能直接把此 `.fcpxml` 当作旧版 Final Cut Pro 7 XML 导入。可先用 Resolve 免费版导入，导出 Final Cut Pro 7 XML，再在 Premiere `File > Import`；或用 XtoCC 转换后导入。跨格式转换后核查 alpha、连接图层、音轨、源片入点和缩放；SRT 可以单独导入。Adobe 明确要求 FCPXML 先经过转换：[官方迁移说明](https://helpx.adobe.com/premiere/desktop/organize-media/import-files/migrate-from-final-cut-pro-x.html)。

**共同限制**：图形/字幕已光栅化，不能在编辑器中直接改单字，改稿需重渲；字幕附件 SRT 可作为可编辑字幕重新导入。XML 不携带字体、素材文件、侧链或 loudnorm 插件，混音已经烘焙进 WAV。源片多帧率、alpha 解释和缩放要逐镜检查。本仓库执行 XML 解析和计数校验，没有声称在这些应用中完成实机导入验证。XML/Resolve 方案需在编辑器里手动加整片末尾 1.2 秒淡黑；ffmpeg 会自动执行。

## 剪映等不支持 XML 的软件

导入 `final.mp4` 即可继续剪，或将 `gfx.mov`、`subs.mov` 和 `final_mix.wav` 从时间零点对齐放在原实拍之上。软件必须支持 alpha MOV 才能保留透明；不支持时使用 ffmpeg 成片。不要对两条透明层使用色键去底，否则黑字和投影会被破坏。需要独立编辑实拍切点时按 `v1_edl.json` 的 rec / frames 重建，或用支持 XML 的编辑器转接。

## Resolve Studio：可选脚本

在 Studio 的 Preferences > System > General 中将 External scripting 设为 Local，打开 Resolve。按随应用附带的 `Developer/Scripting/README.md` 配置 `RESOLVE_SCRIPT_API`、`RESOLVE_SCRIPT_LIB`、`PYTHONPATH`，让当前 Python 能 `import DaVinciResolveScript`。macOS 的 API 文档通常在 `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/`。路径和 Python 版本随平台安装而变。

```bash
python tools/resolve_build.py --edl build/v1_edl.json --footage build/footage --gfx build/gfx.mov --subs build/subs.mov --mix build/final_mix.wav --project Explainer --timeline Draft-01
```

脚本通过官方 `scriptapp('Resolve')` 获取连接，读显式参数；创建新时间线，不删除原时间线。V1 仅视频，V2/V3 为透明图层，A1 为混音。源帧率与时间线不同时按源 fps 换算并向上取整；须检查源片末端及时间线总帧数。

在已有 Resolve MCP 的 `run_script_unsafe` 等 Python 入口中，也可显式传入 Resolve 对象：

```python
import sys
from pathlib import Path
repository = Path('path/to/explainer-video-playbook').resolve()  # 改成自己的仓库路径
work = repository / 'build'
sys.path.insert(0, str(repository / 'tools'))
from resolve_build import build
result = build({
    'edl': str(work / 'v1_edl.json'), 'footage': str(work / 'footage'),
    'gfx': str(work / 'gfx.mov'), 'subs': str(work / 'subs.mov'),
    'mix': str(work / 'final_mix.wav'), 'project': 'Explainer', 'timeline': 'Draft-02'
}, resolve=resolve)
```

MCP 若限制每次执行时间，先减少导入批次或在外部终端执行脚本。导出成片仍可交给默认 ffmpeg；Studio 不是本仓库的前置条件。脚本仅做组装，不自动调色或删除旧工程。
