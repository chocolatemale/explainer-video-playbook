# beats 规格 v1

选择 JSON，UTF-8，无需 YAML 库。`examples/city-choice/beats.json` 是完整示例，文本版分镜见相邻 `beats.md`。工具只解释下面的通用图形和控制节点，没有针对段落名、城市名或案例数据的分支。

## 根对象

| 字段 | 类型 / 含义 |
|---|---|
| `version` | `1` |
| `width`, `height`, `fps` | 此风格预设固定 `1920`, `1080`, `25`；合成后可缩放 |
| `lead_seconds`, `tail_seconds` | 每段旁白前后留白，示例为 `0.25`, `0.45` |
| `fade_seconds` | 片尾设计时长，示例 `1.2`；调用 build/compose 时保持相同参数 |
| `variables` | 任意 JSON 主题变量，表达式中按名字引用，如列名和固定配色 |
| `stills` | 卡片库素材 ID 的字符串数组；`prepare_stills.py` 抽取对应 JPG |
| `layouts` | 可复用节点列表字典；`include` 按名称调用 |
| `settle_frames` | 可选稳定帧缓存界限。示例所有动效在 30 帧内结束；有持续动画时删除此项 |
| `segments` | 按时间顺序的段落对象数组 |

## 段落和 beat

每段有唯一 `id`、`beats` 数组和 `elements` 绘图数组。有旁白的段落额外写 `text`、`timing`、`wav`（相对于规格文件的路径）；无旁白段落写 `seconds`。`build_edl.py --wav-dir` 可以覆盖 WAV 所在目录，按 `<id>.wav` 查找，不改变规格原文。

```json
{
  "id": "intro",
  "text": "vo/text/intro.txt",
  "timing": "vo/timing/intro.json",
  "wav": "vo/wav/intro.wav",
  "beats": [
    {"key": "open", "word": "开头", "type": "F", "mode": "F", "clip": "123456"},
    {"key": "cost", "word": "生活成本", "type": "F", "text": "生活成本"},
    {"key": "compare", "word": "扣掉之后", "type": "B", "mode": "B"}
  ],
  "elements": [
    {"type": "chip-y", "when": "on('cost') and not on('compare')",
     "args": ["生活成本", 960, 400, 100], "kwargs": {"age": {"expr": "age('cost')"}}},
    {"type": "text", "when": "on('compare')", "args": ["扣掉之后", 960, 400, 100]}
  ]
}
```

- `key`：段内唯一标识；`word`：在原稿里找的触发词，默认 `开头`，不是识别结果中的文字。相同触发词再次出现时，找下一个匹配。
- `type`：这个 beat 当时的画面类型 F / B，便于读规格；`mode`：真正切换画面的指令，仅在切换时填写。两者请保持一致，`type` 不独自触发切镜。
- `clip`：F 模式切换需要的素材 ID。B 模式不切换底层实拍，直接盖不透明纸张。
- `offset`：触发位置后移的帧数，可负；最终位置必须仍在段内。
- `after`：另一条已定义 beat 的 key，替代 `word`，用于短尾蒙太奇等固定帧间隔；`offset` 相对其位置。
- `text`：分镜备注/预期上屏内容，实际绘制取 `elements` 的参数，改稿时两处一起改。

每个画面变化都应有独立 key。工具生成 `timeline.json` 的 `events`（含绝对 `start`）、`triggers[段落][key]`、`modes` 和字幕。时间线第一条须在第 0 帧设 F，供实拍 V1 连续铺底；独立纯 B 项目可自行准备底片后再组装。

## 逐字时间戳与字幕

输入兼容 whisper.cpp JSON，最小格式如下，offset 单位为毫秒、相对该段 WAV 开头：

```json
{"transcription":[{"text":"生活","offsets":{"from":0,"to":320}},{"text":"成本","offsets":{"from":320,"to":640}}]}
```

一项有多个字时均匀分配到各字；相邻数字 token 先拼接，再转中文整数读法。`157` 与 `15`+`7` 都对齐到「一百五十七」。小数、百分号、逐位读年份等有歧义时，原稿直接写准确读法。对齐时取字母、汉字与数字（去掉标点），输出字幕使用原稿经同样规范化的文本，按标点切分、每屏不超过 16 字，尾部最多延长 4 帧并受下一条/段落末尾限制。

`alignment[段落].repairs` 记录识别与原稿差异，`chars` 为每字全片帧范围。时间戳单调但错误音频仍可能导致不准确，要逐词审听。

## 绘图节点

`elements` 按数组顺序从后景画到前景。所有坐标为 1080p 像素，文字默认锚点居中 `mm`。普通 JSON 值原样传入；只有 `{"expr":"表达式"}` 会求值。每个绘图节点可加 `when` 条件，默认为真；`target` 默认为主图层 `im`。

通用结构：`{"type":"元素名","args":[位置参数...],"kwargs":{"可选参数":值}}`。

| type | args（按顺序） | 常用 kwargs |
|---|---|---|
| `text` | 文字, x, y, size=60, fill=墨色 | `anchor`, `stroke`, `weight`（Bold / Medium；静态展示字体忽略字重轴） |
| `chip-y`, `chip-k`, `chip-g`, `sticker-r` | 文字, cx, cy, size=60 | `age`, `angle`；红贴纸通常 `angle:8` |
| `chip` | 文字, cx, cy, size=60, kind=y, age=null, angle=0 | kind 可 y/k/g/r/tag |
| `tag` | 文字, age=null | 固定左上角的白标签 |
| `kinetic` | 文字, cy=480, size=120, highlight="", age=null, color=白 | 黑描边大字，highlight 用黄底 |
| `card` | 素材ID, 标签文字, x, y, w, h, age=null | 卡片左上位置、尺寸 |
| `count` | 目标数值, x, y, age, size=90, color=墨色, unit="" | ease 计数，不带弹出缩放 |
| `bar` / `rounded` | [x0,y0,x1,y1], fill, r=10, outline=null, width=1 | 条形图给终点坐标表达式，bar 为语义别名 |
| `line` | [x0,y0,x1,y1] | Pillow `fill`, `width` |
| `ellipse` | [x0,y0,x1,y1] | Pillow `fill`, `outline`, `width` |
| `formula`, `dots`, `table`, `group` | 无 args，使用 `elements` 子数组 | 容器，按原顺序执行，不自动推测排版 |
| `layer` | 无 args | `name`, `size:[w,h]`, `color` 创建局部 RGBA 画布 |
| `place` | 局部画布, cx, cy, age=null, kind=pop | kind 为 pop/card/flip；居中放置 |
| `alpha_paste` | 局部画布, x, y | 左上角贴图 |

函数的可选参数既可放 `args` 对应位置，也可用 `kwargs`；别重复赋同一参数。`card` 从 `--stills/<ID>.jpg` 取图；无卡片的段落不需要静帧。原风格的公式行由 chip/text 组成；表格由 repeat + rounded/text 组成；点阵由 repeat + ellipse 组成；它们的标题、位置、颜色、格数、数据全部在 JSON 中。

```json
{"type":"bar","when":"on('compare')",
 "args":[[300,450,{"expr":"300+900*ease(age('compare')/12.5)"},510],"#FFE03A",8]}
```

贴纸 `age` 从 0 开始：约 4.5 帧回弹；卡片 7.5 帧上浮淡入；条形图常用 `ease(age/12.5)` 在 0.5 秒长满。没有 `age` 时直接画最终状态，负 age 时隐藏。

## 条件、循环和布局复用

- `set`：`{"type":"set","name":"x","value":{"expr":"960-300"}}`；name 也可 `"x,y"` 解包。
- `if`：`{"type":"if","condition":"on('compare')","then":[...],"else":[...]}`。
- `repeat`：`{"type":"repeat","names":"i,label","items":{"expr":"enumerate(labels)"},"elements":[...]}`。
- `continue`：跳过当前循环剩余节点。
- `include`：`{"type":"include","layout":"布局名"}`，以当前环境副本执行 `layouts` 中的节点，不泄漏局部赋值。
- `layer` 配合 `target` 和 `place`，可组成翻面卡、数字牌或其他复合元素。

表达式环境：`sid`、绝对帧 `f`、当前 `mode` 字典、完整时间线 `T`、根 `variables`、配色常量 `PAPER/INK/YELLOW/RED/BLUE/GREEN/GRAY`，以及 `set`/循环变量。

函数：`on(key)` 判断触发；`age(key)` 返回触发后的帧数；`stage(sid,f,keys)` 返回最后一个已触发 key；`event_age(sid,key,f)`；`ease`、`measure`、`photo`、`shadow`；`str/round/len/enumerate/zip/range/min/max/int/float/abs`。支持算术、比较、布尔、三元表达式、列表/元组/字典、列表推导、索引、切片、字典 `.get` 与列表 `.index`。

解释器检查 AST，不允许 import、私有名称或任意属性/调用。规格仍须来自可信来源：没有执行时间/内存配额，极大循环或图像仍会消耗资源。不要把密钥、账号或本机绝对路径放到变量中。

## EDL 输出

段落 EDL：`fps,total_frames,segments:[{seg,start,frames}],vo:[{id,path,rec}]`。旧例保留的 shots/overlays 字段不参与新工具的段落构建。

实拍 EDL：`shots:[{seg,clip,rec,frames,src_in_sec}]`；`rec` 与 `frames` 是全片帧号和帧数，`src_in_sec` 是源片秒数。必须从 0 连续覆盖至 `total_frames`。`ending` 保存淡黑描述，默认合成使用片长和 `--fade-seconds`；示例旧 EDL 的 15 帧收黑注释保留用于对照，当前 v3 合成统一采用 30 帧。编辑器方案需手工加同样淡黑。
