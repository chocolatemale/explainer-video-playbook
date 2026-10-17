# 《怎么选一座城市工作和生活》四城数据底稿

核对截止：2026-10-17。只做数据整理。货币均为名义金额，不是购买力平价；人民币符号统一为“¥”，日元以“日元”明示。

汇率统一为 **2026-10-16中间价：1 USD = 6.7220 CNY；100 JPY = 4.2439 CNY，即1 JPY = 0.042439 CNY**。来源：[国家外汇管理局](https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do?COLLCC=546877760)。不要将原表“每100日元”错作每1日元。

地域：上海、深圳为行政市；东京人口/一般工资为东京都，程序员辅助样本为Greater Tokyo Area；南湾人口/通勤为Santa Clara县、工资为San Jose-Sunnyvale-Santa Clara MSA（另含San Benito县）、房租为San Jose市。未把旧金山市或全湾区代替南湾。

主值优先官方。**辅**为非官方自报/众包，仅辅助；官方定义缺失仍用null，辅助值单列。四城的一般工资不具备完全相同抽样总体，不能据此给“普通打工人收入”作精确排名。

| 指标（本币＋人民币） | 上海 | 深圳 | 东京 | 硅谷：南湾 |
|---|---|---|---|---|
| 一般雇员税前年均工资 | 239,557.00 人民币 ≈ ¥239,557.00（2024） [SHW](#source-shw) | 191,367.00 人民币 ≈ ¥191,367.00（2025） [SZW](#source-szw) | 6,788,676.00 日元 ≈ ¥288,104.62（2025） [TKW](#source-tkw) | 119,225.60 美元 ≈ ¥801,434.48（2025） [USW](#source-usw) |
| 私营单位税前年均工资（补充） | 113,914.00 人民币 ≈ ¥113,914.00（2024） [SHW](#source-shw) | 99,220.00 人民币 ≈ ¥99,220.00（2025） [SZW](#source-szw) | 不适用 | 不适用 |
| 软件工程师官方职业工资中位数/年 | null [SHW](#source-shw) | null [SZW](#source-szw) | null [TKW](#source-tkw) | 213,110.00 美元 ≈ ¥1,432,525.42（2025） [USMED](#source-usmed) [USW](#source-usw) |
| **辅**：软件工程师自报总包中位数/年 | 666,112.00 人民币 ≈ ¥666,112.00（2026） [SHL](#source-shl) | 505,231.00 人民币 ≈ ¥505,231.00（2026） [SZL](#source-szl) | 8,539,096.00 日元 ≈ ¥362,390.70（2026） [TKL](#source-tkl) | 233,750.00 美元 ≈ ¥1,571,267.50（2026） [USL](#source-usl) |
| 市中心一居室官方同口径月租 | null [SHR](#source-shr) | null [SZR](#source-szr) | null [TKR](#source-tkr) | null [USR](#source-usr) |
| **辅**：市中心一居室月租 | 6,952.38 人民币 ≈ ¥6,952.38（2026） [SHR](#source-shr) | 5,095.38 人民币 ≈ ¥5,095.38（2026） [SZR](#source-szr) | 202,375.00 日元 ≈ ¥8,588.59（2026） [TKR](#source-tkr) | 3,085.56 美元 ≈ ¥20,741.13（2026） [USR](#source-usr) |
| 官方同口径房价收入比 | null [PIR](#source-pir) [PIRM](#source-pirm) | null [PIR](#source-pir) [PIRM](#source-pirm) | null [PIR](#source-pir) [PIRM](#source-pirm) | null [PIR](#source-pir) [PIRM](#source-pirm) |
| **辅**：房价收入比（年，固定2026榜） | 34.2（2026） [PIR](#source-pir) [PIRM](#source-pirm) | 28.5（2026） [PIR](#source-pir) [PIRM](#source-pirm) | 15.2（2026） [PIR](#source-pir) [PIRM](#source-pirm) | 8.4（2026） [PIR](#source-pir) [PIRM](#source-pirm) |
| 50万元人民币等值税前年薪 | 500,000.00 人民币 ≈ ¥500,000.00（2025） [FX](#source-fx) | 500,000.00 人民币 ≈ ¥500,000.00（2025） [FX](#source-fx) | 11,781,615.97 日元 ≈ ¥500,000.00（2025） [FX](#source-fx) | 74,382.62 美元 ≈ ¥499,999.97（2025） [FX](#source-fx) |
| 个税＋个人社保后到手/年（估算） | 386,669.61 人民币 ≈ ¥386,669.61（2025） [CNTAX](#source-cntax) [SHCAP](#source-shcap) [SHSOC](#source-shsoc) [SHUI25](#source-shui25) | 395,274.84 人民币 ≈ ¥395,274.84（2025） [CNTAX](#source-cntax) [SZCAP](#source-szcap) [SZMCAP](#source-szmcap) [SZMRATE](#source-szmrate) [SZPENSION](#source-szpension) [SZUI](#source-szui) [SZUIBASE](#source-szuibase) | 8,409,720.14 日元 ≈ ¥356,900.11（2025） [TKTAX](#source-tktax) [TKEXP](#source-tkexp) [TKBASE](#source-tkbase) [TKLOCAL](#source-tklocal) [TKHEALTH](#source-tkhealth) [TKPENSION](#source-tkpension) [TKPCAP](#source-tkpcap) [TKUI](#source-tkui) | 57,261.40 美元 ≈ ¥384,911.13（2025） [USTAX](#source-ustax) [USBASE](#source-usbase) [CATAX](#source-catax) [CABASE](#source-cabase) [CAFORM](#source-caform) [FICA](#source-fica) [SSCAP](#source-sscap) [CASDI](#source-casdi) |
| 到手比例（%，估算） | 77.3339（2025） [CNTAX](#source-cntax) [SHCAP](#source-shcap) [SHSOC](#source-shsoc) [SHUI25](#source-shui25) | 79.055（2025） [CNTAX](#source-cntax) [SZCAP](#source-szcap) [SZMCAP](#source-szmcap) [SZMRATE](#source-szmrate) [SZPENSION](#source-szpension) [SZUI](#source-szui) [SZUIBASE](#source-szuibase) | 71.38（2025） [TKTAX](#source-tktax) [TKEXP](#source-tkexp) [TKBASE](#source-tkbase) [TKLOCAL](#source-tklocal) [TKHEALTH](#source-tkhealth) [TKPENSION](#source-tkpension) [TKPCAP](#source-tkpcap) [TKUI](#source-tkui) | 76.9822（2025） [USTAX](#source-ustax) [USBASE](#source-usbase) [CATAX](#source-catax) [CABASE](#source-cabase) [CAFORM](#source-caform) [FICA](#source-fica) [SSCAP](#source-sscap) [CASDI](#source-casdi) |
| 平均单程通勤（分钟） | 39（2024） [CNCOMM](#source-cncomm) [CNCOMM_IMG](#source-cncomm_img) | 33（2024） [CNCOMM](#source-cncomm) [CNCOMM_IMG](#source-cncomm_img) | null [TKCOMM](#source-tkcomm) | 26.2（2020–2024） [USPOP](#source-uspop) |
| 法定通常工时/加班门槛（小时/周） | 40（2026核对） [CNH](#source-cnh) | 40（2026核对） [CNH](#source-cnh) | 40（2026核对） [TKH](#source-tkh) | 40（2026核对） [USH](#source-ush) [USEX](#source-usex) |
| 主要/重点产业（定性） | 集成电路、生物医药、人工智能、汽车制造、金融服务 [SHP](#source-shp) [SHI](#source-shi) | 电子信息硬件、软件与互联网、新能源汽车、金融服务、现代物流 [SZP](#source-szp) [SZI](#source-szi) | IT与通信、金融与金融科技、医疗生命科学、文娱与电子 [TKI](#source-tki) [RAKUTEN](#source-rakuten) [SONY](#source-sony) | 半导体与硬件、软件及AI、先进制造、医疗健康 [USI](#source-usi) [USW](#source-usw) |
| 代表企业 | 上汽通用、中芯国际（上海）、联影医疗 [SHCO](#source-shco) | 华为、腾讯、比亚迪 [SZCO](#source-szco) [SZI](#source-szi) | Sony Group、SoftBank Group、Rakuten Group [SONY](#source-sony) [SOFTBANK](#source-softbank) [RAKUTEN](#source-rakuten) | NVIDIA（Santa Clara）、Apple（Cupertino）、Adobe（San Jose） [NVIDIA](#source-nvidia) [APPLE](#source-apple) [ADOBE](#source-adobe) |
| 独角兽（家，胡润2026） | 74（2026） [HURUN](#source-hurun) | 44（2026） [HURUN](#source-hurun) | null [HURUN](#source-hurun) | null [HURUN](#source-hurun) |
| 上市科技公司统一口径数量 | null | null | null | null |
| 外地户籍/外国人长期居留 | 内地外地户籍：居住证积分120分是公共服务门槛；常规居转户为持证及社保累计7年，另须纳税、职称/职业资格及社保基数等；也有人才引进、留学回国通道。 [SHRES](#source-shres) [SHHUKOU](#source-shhukou) | 内地外地户籍：普通高等教育本科以上且45周岁以下，或专科以上且35周岁以下，可按人才引进条件核准；在职办理核验就业社保等；另有积分/政策迁户。 [SZHUKOU](#source-szhukou) [SZGUIDE](#source-szguide) | 外国人：匹配雇主及专业资格的工作居留/高度人才；高度人才70分维持3年、80分维持1年可按特例申请永住。经营管理新申请须资本金等3000万日元及至少1名符合条件常勤员工，另有能力/经历/事业计划要求。 [TKHSP](#source-tkhsp) [TKPR](#source-tkpr) [TKBIZ](#source-tkbiz) | 外国人：雇主申请H-1B，名额受限部分需遴选；FY2027采用加权规则。长期定居另走职业移民等路径，受资格与出生地排期影响。2025公告曾要求部分新境外H-1B请愿付款10万美元；2026虽宣布延期，实施政策被法院阻止，当前不能写成必缴。 [H1BLOT](#source-h1blot) [H1B25](#source-h1b25) [H1B26](#source-h1b26) [H1BCOURT](#source-h1bcourt) [H1BCHECK](#source-h1bcheck) [EB2](#source-eb2) |
| 人口（人） | 24,854,100（2025） [SHP](#source-shp) | 18,248,500（2025） [SZP](#source-szp) | 14,296,683（2026） [TKP](#source-tkp) | 1,914,391（2025） [USPOP](#source-uspop) |
| 年均温（℃；单年与气候期不能混比） | 18.8（2024） [SHCLIM](#source-shclim) | 23.5（2025） [SZCLIM](#source-szclim) [SZCLIMN](#source-szclimn) | 15.8（1991–2020） [TKCLIM](#source-tkclim) | null [USCLIM](#source-usclim) |
| 气候一句话 | 亚热带季风；夏热湿、冬凉、四季分明。 [SHCLIM](#source-shclim) | 南亚热带季风；长夏短冬、夏半年多雨并受台风影响。 [SZCLIM](#source-szclim) [SZCLIMN](#source-szclimn) | 夏季暖湿、冬季较凉，季节差异明显。 [TKCLIM](#source-tkclim) | 保留气候描述：San Jose地中海型，夏暖干燥、冬凉多雨。 [USCLIM](#source-usclim) |

税后比例显示到小数4位仅用于复算，视频建议取小数1位；这是冻结2025标准的情景估算，不能标为2026实时薪资工具。公积金和商业医保等排除项会使“实际到账工资”低于表内净额。

**H-1B核实结论**：2025-09-19公告第1节确有10万美元要求（折人民币672200元），不是谣传，但不是所有人每年必交。2026-09-18延长公告也确实存在；2026-09-30法院裁定第34页禁止实施原公告及延期的机构政策，10-01大学执行说明交叉确认仍暂停。因此截至本次调研不能上屏成“赴美申请必交67.22万元”。参见 [公告原文](https://www.whitehouse.gov/presidential-actions/2025/09/restriction-on-entry-of-certain-nonimmigrant-workers/)、[延期原文](https://www.whitehouse.gov/presidential-actions/2026/09/restriction-on-entry-of-certain-nonimmigrant-workers-faad/)、[法院原文](https://www.govinfo.gov/content/pkg/USCOURTS-cand-4_25-cv-08454/pdf/USCOURTS-cand-4_25-cv-08454-17.pdf)。

日本经营管理门槛：3000万日元≈人民币1273170元（2025-10-16新标准）；这是经营资本等要求，不能与美国申请费当作同类成本比较。

逐条来源（URL、发布机构、数据年份；抓取日均为2026-10-17）：

<a id="source-fx"></a>
- **FX** [人民币汇率中间价表](https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do?COLLCC=546877760)｜国家外汇管理局（中国外汇交易中心中间价）｜数据/规则年份：2026-10-16。原表每100美元672.20元、每100日元4.2439元；本文全部货币统一按此日折算。
<a id="source-shw"></a>
- **SHW** [上海统计年鉴2025，表2.23 城镇单位就业人员平均工资](https://tjj.sh.gov.cn/tjnj/2025tjnj/C0223.htm)｜上海市统计局｜数据/规则年份：2024。非私营239557元，私营113914元。未核实到同定义2025年上海原表，保留2024年。
<a id="source-szw"></a>
- **SZW** [2025年深圳市城镇单位就业人员年平均工资情况](https://www.sz.gov.cn/cn/xxgk/zfxxgj/tjsj/tjgb/content/mpost_12907800.html)｜深圳市统计局｜数据/规则年份：2025。2026-07-24发布；非私营191367元，私营99220元。
<a id="source-szw24"></a>
- **SZW24** [2024年深圳市城镇单位就业人员年平均工资情况](https://www.sz.gov.cn/cn/xxgk/zfxxgj/tjsj/tjgb/content/post_12561969.html)｜深圳市统计局｜数据/规则年份：2024。2025-06-30发布；用于与上海同年比较：非私营174478元，私营95217元。
<a id="source-tkw"></a>
- **TKW** [毎月勤労統計調査2025年年报，概要表2](https://www.toukei.metro.tokyo.lg.jp/maikin/2025/mk25qf0001.pdf)｜东京都总务局统计部｜数据/规则年份：2025。2026-06-30发布；一般劳动者月均现金工资565723日元，含奖金，乘12得年化工资。5人以上事业所。
<a id="source-usw"></a>
- **USW** [Occupational Employment and Wages in San Jose—May 2025](https://www.bls.gov/regions/west/news-release/occupationalemploymentandwages_sanjose.htm)｜美国BLS｜数据/规则年份：2025。2026-07-09发布；全职业平均时薪57.32美元，按2080小时年化；软件开发者平均年工资221710美元。MSA包括Santa Clara及San Benito两县。
<a id="source-usmed"></a>
- **USMED** [Local Wages 15-1252.00，Full Details表中的San Jose行](https://www.onetonline.org/link/localwages/15-1252.00?zip=94025)｜美国劳工部O*NET（转载BLS OEWS）｜数据/规则年份：2025。务必读表中San Jose-Sunnyvale-Santa Clara行，中位数213110美元；页首94025对应旧金山地区，不能抄页首数字。
<a id="source-shl"></a>
- **SHL** [Software Engineer Median Total Compensation](https://www.levels.fyi/t/software-engineer/locations/shanghai-chn)｜Levels.fyi，自报样本（辅助）｜数据/规则年份：2026-10-16。抓取2026-10-17；是页面当前样本总包中位数，并非2026单年总体抽样调查；含底薪、股票、奖金，样本有明显行业和公司选择偏差。
<a id="source-szl"></a>
- **SZL** [Software Engineer Median Total Compensation](https://www.levels.fyi/t/software-engineer/locations/shenzhen-chn)｜Levels.fyi，自报样本（辅助）｜数据/规则年份：2026-10-17。抓取2026-10-17；是页面当前样本总包中位数，并非2026单年总体抽样调查；含底薪、股票、奖金，样本有明显行业和公司选择偏差。
<a id="source-tkl"></a>
- **TKL** [Software Engineer Median Total Compensation](https://www.levels.fyi/t/software-engineer/locations/greater-tokyo-area)｜Levels.fyi，自报样本（辅助）｜数据/规则年份：2026-10-16。抓取2026-10-17；是页面当前样本总包中位数，并非2026单年总体抽样调查；含底薪、股票、奖金，样本有明显行业和公司选择偏差。
<a id="source-usl"></a>
- **USL** [Software Engineer Median Total Compensation](https://www.levels.fyi/t/software-engineer/locations/san-jose-usa)｜Levels.fyi，自报样本（辅助）｜数据/规则年份：2026-10-16。抓取2026-10-17；是页面当前样本总包中位数，并非2026单年总体抽样调查；含底薪、股票、奖金，样本有明显行业和公司选择偏差。
<a id="source-shr"></a>
- **SHR** [1 Bedroom Apartment in City Centre，Rent Per Month](https://www.numbeo.com/cost-of-living/in/Shanghai)｜Numbeo，众包（辅助）｜数据/规则年份：2026-10-15。抓取2026-10-17；页面滚动报价，非官方租赁成交均值；市中心、房型、面积和租约条件未统一，不能当作官方房租排名。
<a id="source-szr"></a>
- **SZR** [1 Bedroom Apartment in City Centre，Rent Per Month](https://www.numbeo.com/cost-of-living/in/Shenzhen/)｜Numbeo，众包（辅助）｜数据/规则年份：2026-10-15。抓取2026-10-17；页面滚动报价，非官方租赁成交均值；市中心、房型、面积和租约条件未统一，不能当作官方房租排名。
<a id="source-tkr"></a>
- **TKR** [1 Bedroom Apartment in City Centre，Rent Per Month](https://www.numbeo.com/cost-of-living/in/Tokyo)｜Numbeo，众包（辅助）｜数据/规则年份：2026-10-16。抓取2026-10-17；页面滚动报价，非官方租赁成交均值；市中心、房型、面积和租约条件未统一，不能当作官方房租排名。
<a id="source-usr"></a>
- **USR** [1 Bedroom Apartment in City Centre，Rent Per Month](https://www.numbeo.com/cost-of-living/in/San-Jose)｜Numbeo，众包（辅助）｜数据/规则年份：2026-10-15。抓取2026-10-17；页面滚动报价，非官方租赁成交均值；市中心、房型、面积和租约条件未统一，不能当作官方房租排名。
<a id="source-pir"></a>
- **PIR** [Property Prices Index by City 2026](https://www.numbeo.com/property-investment/rankings.jsp?title=2026)｜Numbeo，众包（辅助）｜数据/规则年份：2026。固定2026榜单：上海34.2、深圳28.5、东京15.2、San Jose CA 8.4；不使用滚动榜混搭。
<a id="source-pirm"></a>
- **PIRM** [About Property Value and Investment Indexes](https://www.numbeo.com/property-investment/indicators_explained.jsp)｜Numbeo，方法说明｜数据/规则年份：2026核对。房价收入比=90平方米×中心/非中心平均平方米价格÷(平均税后月薪×1.5×12)。不是实际家庭中位收入，也不是独栋住宅价格收入比。
<a id="source-cncomm"></a>
- **CNCOMM** [2025年中国主要城市通勤监测报告，印刷第19、20页](https://huiyan.baidu.com/boswebsite/cms/report/2025tongqin/)｜中国城市规划设计研究院、百度地图｜数据/规则年份：2024。报告为2025版，底层数据截至2024年底。已查看原图P29及P30：上海39分钟、深圳33分钟。大数据模型估计，非住户问卷。
<a id="source-cncomm_img"></a>
- **CNCOMM_IMG** [通勤报告原图P29（印刷第19页）](https://huiyan.baidu.com/cms/report/2025tongqin/P29.png)｜中国城市规划设计研究院、百度地图｜数据/规则年份：2024。原始图表，与下一页年度变化表P30交叉核对。
<a id="source-tkcomm"></a>
- **TKCOMM** [社会生活基本調査2021，结果概要表6-1](https://www.stat.go.jp/data/shakai/2021/pdf/gaiyoua.pdf)｜日本总务省统计局｜数据/规则年份：2021。东京都平日通勤通学行動者平均为每日95分钟；包含通学及全天往返，不可直接填作单程上班时间。
<a id="source-uspop"></a>
- **USPOP** [QuickFacts: Santa Clara County, California](https://www.census.gov/quickfacts/fact/table/santaclaracountycalifornia/PST045225)｜美国Census Bureau｜数据/规则年份：2025人口；2020–2024 ACS通勤。2025-07-01人口1914391；2020–2024年16岁以上上班者平均单程26.2分钟，排除在家工作者。县界与工资MSA并非完全一致。
<a id="source-cnh"></a>
- **CNH** [允许合法加班和夜班：援引国务院工作时间规定第三条](https://fgw.sh.gov.cn/ys-laogong-1.5.2.1-h5/20240125/f173e5aa3b29400aa425188a3519b228.html)｜上海市发展改革委（国务院规定）｜数据/规则年份：1995修订；2026核对。标准工时每日8小时、每周40小时；不得把法定标准当作实际每周工作时长。
<a id="source-tkh"></a>
- **TKH** [労働時間・休日](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/roudouzikan/index.html)｜日本厚生劳动省｜数据/规则年份：2026核对。原则每日8小时、每周40小时；存在变形工时、加班等规定。
<a id="source-ush"></a>
- **USH** [Overtime](https://www.dir.ca.gov/dlse/faq_overtime.htm)｜加州工业关系部DIR｜数据/规则年份：2026核对。一般非豁免雇员每日8小时、每周40小时为加班门槛，不能解释为法律禁止超过40小时。
<a id="source-usex"></a>
- **USEX** [Overtime Exemption for Computer Software Employees](https://www.dir.ca.gov/OPRL/ComputerSoftware.htm)｜加州工业关系部DIR｜数据/规则年份：2026。符合职责及薪酬等条件的软件从业者可能豁免加班规则；不能断言科技业人人朝九晚五。
<a id="source-shp"></a>
- **SHP** [2025年上海市国民经济和社会发展统计公报](https://tjj.sh.gov.cn/tjgb/20260330/e0772941e8e041eaaad2df850b44ef98.html)｜上海市统计局｜数据/规则年份：2025。2026-03-30发布，年末常住人口24854100。产业为依据公报选择的主要板块，不是统一就业人数排序。
<a id="source-szp"></a>
- **SZP** [深圳市2025年国民经济和社会发展统计公报，政府公报第17期](https://www.sz.gov.cn/attachment/1/1723/1723320/12848626.pdf)｜深圳市统计局、国家统计局深圳调查队｜数据/规则年份：2025。2026-05-25发布，年末常住人口18248500。
<a id="source-tkp"></a>
- **TKP** [東京都の人口（推計），2026年9月1日](https://www.toukei.metro.tokyo.lg.jp/jsuikei/2026/js269f0100.pdf)｜东京都总务局统计部｜数据/规则年份：2026-09-01。东京都全域14296683人，包括多摩及岛屿；基于2025国势调查速報值，有待后续修订。不是大东京都市圈人口。
<a id="source-hurun"></a>
- **HURUN** [2026全球独角兽榜](https://hurun.cn/zh-CN/Info/Detail?num=E9GMNPY37G4Q)｜胡润研究院｜数据/规则年份：2026。2026-06-25发布，估值截止2026-01-01，重大变化更新至发布前。成立于2000年后、估值10亿美元以上且未上市。上海74家、深圳44家；没有用旧金山市数量代替南湾。
<a id="source-shi"></a>
- **SHI** [战略性新兴产业和先导产业发展十四五规划](https://www.shanghai.gov.cn/gwk/search/content/d684ff525ead40d8a2dfa51e541a14e4)｜上海市政府｜数据/规则年份：2021–2025规划。支持集成电路、生物医药、人工智能、新能源汽车等产业分类；规划目标不充当已实现统计值。
<a id="source-shco"></a>
- **SHCO** [上海市纳入2025年度碳排放配额管理单位名单](https://www.shanghai.gov.cn/gwk/search/content/73cb4a6134c74a29b776be60172b4c64)｜上海市生态环境局｜数据/规则年份：2025。名单确认上汽通用、中芯国际（上海）、上海联影医疗位于上海。代表企业不作为企业数量统计。
<a id="source-szi"></a>
- **SZI** [深圳战略性新兴产业风头正盛](https://www.sz.gov.cn/cn/zjsz/fwts_1_3/tzdt_1/content/post_12650791.html)｜深圳政府在线（深圳特区报）｜数据/规则年份：2026。行业背景及比亚迪、华为等企业实例；定性辅助，未引用其中营销式业绩数字。
<a id="source-szco"></a>
- **SZCO** [深圳2025年知识产权数据报告](https://amr.sz.gov.cn/attachment/1/1722/1722088/12838942.pdf)｜深圳市市场监督管理局｜数据/规则年份：2025。企业榜表包含华为、腾讯、比亚迪，本文仅用于代表企业定位，不引用专利排名数量。
<a id="source-tki"></a>
- **TKI** [東京の産業](https://www.investtokyo.metro.tokyo.lg.jp/jp/industries/index.html)｜东京都产业劳动局Invest Tokyo｜数据/规则年份：2026页面核对。列医疗、IT、环境领域；金融和文娱电子依据下列官方平台/企业业务补充，定性选取。
<a id="source-sony"></a>
- **SONY** [Corporate Data](https://www.sony.com/en/SonyInfo/CorporateInfo/data/)｜Sony Group｜数据/规则年份：2026。总部东京都港区；业务覆盖游戏、音乐、影视、电子、影像传感器。
<a id="source-softbank"></a>
- **SOFTBANK** [Corporate Data](https://group.softbank/en/about/profile)｜SoftBank Group｜数据/规则年份：2026页面核对。总部东京都港区；代表科技投资及通信生态。
<a id="source-rakuten"></a>
- **RAKUTEN** [About Us / Company Information](https://global.rakuten.com/corp/about/)｜Rakuten Group｜数据/规则年份：2025。总部东京都世田谷区；电商、金融科技、通信等。
<a id="source-usi"></a>
- **USI** [City of San Jose economic development report](https://www.sanjoseca.gov/home/showpublisheddocument/120890/638812607480530000)｜圣何塞市政府｜数据/规则年份：2025。半导体、软件、先进制造、医疗等主要板块；不声称按同一统计标准排名。
<a id="source-apple"></a>
- **APPLE** [Corporate Address](https://www.apple.com/contact/)｜Apple｜数据/规则年份：2026页面核对。Cupertino，Santa Clara县。
<a id="source-nvidia"></a>
- **NVIDIA** [Contact Us: Americas Locations](https://www.nvidia.com/en-us/contact/)｜NVIDIA｜数据/规则年份：2026页面核对。Santa Clara。
<a id="source-adobe"></a>
- **ADOBE** [Corporate headquarters](https://www.adobe.com/about-adobe/contact.html)｜Adobe｜数据/规则年份：2026页面核对。San Jose。
<a id="source-shres"></a>
- **SHRES** [居住证积分管理办法：总积分标准分值](https://jzzjf.rsj.sh.gov.cn/jzzjf/pingfen/zc2.jsp)｜上海市人社局｜数据/规则年份：现行页面，2026核对。120积分属于居住证公共服务体系，不是落户批准分数。
<a id="source-shhukou"></a>
- **SHHUKOU** [居住证转办常住户口办事指南](https://zwdt.sh.gov.cn/govPortals/bsfw/item/e2f8557b-547a-45de-ba38-8beac177d17e)｜上海一网通办｜数据/规则年份：现行页面，2026核对。常规居转户：持证累计7年、持证期间社保累计7年、依法纳税、职称/职业资格及社保市场化评价等条件；另有人才引进、留学回国等通道。
<a id="source-szhukou"></a>
- **SZHUKOU** [深圳市户籍迁入若干规定](https://ga.sz.gov.cn/ZDYW/ZDYWRK/HZFLFG/content/post_10946469.html)｜深圳市政府（公安局转载）｜数据/规则年份：2016规则，2026核对。普通高等教育本科以上且45周岁以下，或专科以上且35周岁以下，可依条件核准人才引进；在职申请还须符合就业社保等办事条件，不是仅有学历就自动获批。
<a id="source-szguide"></a>
- **SZGUIDE** [人才引进办事指南](https://wsbs.sz.gov.cn/shenzhen/project/phoneGuide?code=4403090000006718601670001000423001)｜深圳市政务服务｜数据/规则年份：2026核对。用于交叉检查学历、年龄及申请条件。
<a id="source-tkhsp"></a>
- **TKHSP** [高度人材ポイント制とは](https://www.moj.go.jp/isa/applications/resources/newimmiact_3_system_index.html?hl=ja&lang=ja)｜日本出入国在留管理厅｜数据/规则年份：2026核对。70分为高度人才优遇认定线；按学历、职历、年收等计分，不是缴钱购买居留。
<a id="source-tkpr"></a>
- **TKPR** [永住許可に関するガイドライン，2026-10-01改定](https://www.moj.go.jp/isa/10_00279.html?lang=ne)｜日本出入国在留管理厅｜数据/规则年份：2026。原文保留70分维持3年、80分维持1年的高度人才居住年限特例；仍须满足善良品行、独立生计、公共义务等审查要求；年限不是审批耗时承诺。
<a id="source-tkbiz"></a>
- **TKBIZ** [经营管理许可基准改正，2025-10-16施行](https://www.moj.go.jp/isa/content/001448070.pdf)｜日本出入国在留管理厅｜数据/规则年份：2025。资本金等至少3000万日元，且雇佣至少1名符合身份限制的常勤职员；另有日语能力、经营经验/学位、事业计划专业确认等条件，既有持有人有过渡安排。
<a id="source-h1b25"></a>
- **H1B25** [Restriction on Entry of Certain Nonimmigrant Workers，Proclamation 10973](https://www.whitehouse.gov/presidential-actions/2025/09/restriction-on-entry-of-certain-nonimmigrant-workers/)｜美国白宫｜数据/规则年份：2025-09-19。第1节规定部分H-1B请愿附带100000美元付款；自2025-09-21生效，原定12个月；原文主要涉及美国境外人员及例外，不是所有申请人每年都交。
<a id="source-h1b26"></a>
- **H1B26** [Restriction on Entry，2026延长公告](https://www.whitehouse.gov/presidential-actions/2026/09/restriction-on-entry-of-certain-nonimmigrant-workers-faad/)｜美国白宫｜数据/规则年份：2026-09-18。宣布延长至2027-09-21；公告文字存在不等于现可执行收费。
<a id="source-h1bcourt"></a>
- **H1BCOURT** [Global Nurse Force v. Trump，Dkt.130，结论第34页](https://www.govinfo.gov/content/pkg/USCOURTS-cand-4_25-cv-08454/pdf/USCOURTS-cand-4_25-cv-08454-17.pdf)｜美国加州北区联邦地区法院（GovInfo原文）｜数据/规则年份：2026-09-30。撤销并发回机构实施政策，禁止执行10973及其11069延期的实施政策，直至完成指定规则制定与分析；法院拒绝暂缓裁定。
<a id="source-h1bcheck"></a>
- **H1BCHECK** [100000 H-1B Executive Order Extended; Fee Remains Blocked](https://internationalcenter.umich.edu/about/news/100000-h-1b-executive-order-extended-fee-remains-blocked)｜密歇根大学International Center｜数据/规则年份：2026-10-01。与法院原文交叉验证暂停执行；截至调研日未查到此后恢复执行的可靠原文。
<a id="source-h1blot"></a>
- **H1BLOT** [FY2027 H-1B Cap Initial Registration Period](https://content.govdelivery.com/accounts/USDHSCIS/bulletins/406da02)｜美国USCIS官方GovDelivery｜数据/规则年份：2026-01-30。FY2027超额登记时采用加权遴选；不能把以前纯随机抽签概率写成2026固定中签率。
<a id="source-eb2"></a>
- **EB2** [Employment-Based Immigration: Second Preference EB-2](https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-second-preference-eb-2)｜美国USCIS｜数据/规则年份：2026核对。H-1B是临时工作身份；长期定居通常另走职业移民等通道，资格、雇主流程和出生地排期影响难度。正文403，未引述具体排期数字。
<a id="source-shclim"></a>
- **SHCLIM** [Shanghai weather: four seasons](https://english.shanghai.gov.cn/en-Overview/20241225/ce046a2a1e754fde8c02804d6d66db18.html)｜上海市政府英文门户｜数据/规则年份：2024。2025-04-18发布，2024年年均温18.8℃；是单年观测，不是长期气候正常值。
<a id="source-szclim"></a>
- **SZCLIM** [深圳2025年气候公报发布](https://weather.sz.gov.cn/mobile/xinxigongkai/gongzuodongtai/content/post_12635681.html)｜深圳市气象局｜数据/规则年份：2025。年均温23.5℃；2026年发布。
<a id="source-szclimn"></a>
- **SZCLIMN** [深圳市气候概况及四季特征](https://weather.sz.gov.cn/qixiangfuwu/qihoufuwu/qihouguanceyupinggu/qihougaikuang/)｜深圳市气象局｜数据/规则年份：1991–2020气候期；2026页面更新。南亚热带季风气候，长夏短冬，夏半年多雨、台风影响。
<a id="source-tkclim"></a>
- **TKCLIM** [Tables of Climatological Normals](https://www.data.jma.go.jp/stats/en/normal/normal.html)｜日本气象厅JMA｜数据/规则年份：1991–2020。Tokyo站年均温15.8℃；长期正常值，不与2024/2025单年数据作温差结论。
<a id="source-usclim"></a>
- **USCLIM** [Climate of San Jose](https://www.weather.gov/media/wrh/online_publications/TMs/TM-259.pdf)｜美国NOAA/NWS｜数据/规则年份：2012说明文档，非2025观测。地中海型气候，夏季温暖干燥，冬季较凉且降雨集中；没有以旧金山市气候替代。
<a id="source-cntax"></a>
- **CNTAX** [中华人民共和国个人所得税法](https://www.chinatax.gov.cn/n810219/n810744/n3752930/n3752974/c3970366/content.html)｜国家税务总局｜数据/规则年份：2018修订；2025模型适用。居民综合所得年减除费用60000元，社保个人缴费可扣；模型适用25%档、速算扣除31920元。
<a id="source-shui25"></a>
- **SHUI25** [2025年阶段性降低社会保险费率政策问答](https://rsj.sh.gov.cn/tzcjd_17352_17352/20250103/t0035_1429760.html)｜上海市人社局｜数据/规则年份：2025。核验2025失业保险单位和个人各0.5%。
<a id="source-caform"></a>
- **CAFORM** [2025 Form540，第1页个人豁免及第2页标准扣除](https://www.ftb.ca.gov/forms/2025/2025-540.pdf)｜加州FTB｜数据/规则年份：2025。表内个人豁免153美元；单身标准扣除5706美元。
<a id="source-shcap"></a>
- **SHCAP** [本市调整2025年度社保缴费基数上下限](https://rsj.sh.gov.cn/tgsgg_17341/20250918/t0035_1435637.html)｜上海市人社局｜数据/规则年份：2025。2025-07-01起上限37302元/月，模型将此下半年标准年化。
<a id="source-shsoc"></a>
- **SHSOC** [新就业形态劳动者专属服务指南：职工个人费率](https://www.shanghai.gov.cn/nw17239/20260913/37398bbb63ad4fffa64e0b9deb0f6afc.html)｜上海市政府（社保费率说明）｜数据/规则年份：2026核对2025延续费率。职工个人养老8%、医保2%、失业0.5%；个人不缴工伤和生育。
<a id="source-szcap"></a>
- **SZCAP** [2025下半年残疾人在岗就业社保补贴通知：所附基数提醒](https://www.szft.gov.cn/bmxx_qt/qcjrlhh/tzgg/content/post_12584252.html)｜深圳市福田区政府｜数据/规则年份：2025。引用全省规定：2025-07-01起养老缴费上限27549元/月；本文仅引用职工基数规定，不使用补贴金额。
<a id="source-szmcap"></a>
- **SZMCAP** [温馨提示：2025职工医保缴费基数](https://hsa.sz.gov.cn/fzlm/znts/cnyc/content/post_11929040.html)｜深圳市医保局｜数据/规则年份：2025。全年医保上限33666元/月。
<a id="source-szmrate"></a>
- **SZMRATE** [医保办法第八条答复](https://www.sz.gov.cn/hdjlpt/detail?pid=2979621&via=pc)｜深圳市医保局｜数据/规则年份：2024规则；2025适用。一档医保个人2%；模型选一档。
<a id="source-szpension"></a>
- **SZPENSION** [单位职工与灵活就业养老保险区别](https://hrss.sz.gov.cn/szsi/gzfw/ywzsk/sbgx/jbgn/content/post_12703216.html)｜深圳市社保局｜数据/规则年份：2026核对法定8%费率。单位职工个人养老缴费8%。
<a id="source-szui"></a>
- **SZUI** [2025深圳社保民生答卷](https://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/content/post_12622847.html)｜深圳政府在线（社保年度执行情况）｜数据/规则年份：2025。确认2025失业保险个人费率0.2%。
<a id="source-szuibase"></a>
- **SZUIBASE** [职工失业保险基数官方答复](https://www.sz.gov.cn/hdjlpt/detail?pid=3209367&vi=)｜深圳市人社局｜数据/规则年份：2025。2025-07-17答复本人工资为基数；该模型月薪41666.67元。
<a id="source-tkexp"></a>
- **TKEXP** [Deduction for employment income](https://www.nta.go.jp/english/taxes/individual/12012.htm)｜日本国税厅NTA｜数据/规则年份：2025。模型收入超过850万日元，工资所得扣除195万日元。
<a id="source-tkbase"></a>
- **TKBASE** [2025 year-end adjustment: deductions](https://www.nta.go.jp/publication/pamph/gensen/nencho2025/pdf/302_en.pdf)｜日本国税厅NTA｜数据/规则年份：2025。模型总所得655万至2350万日元，基本扣除58万日元。
<a id="source-tktax"></a>
- **TKTAX** [No.2260 所得税の税率](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm)｜日本国税厅NTA｜数据/规则年份：2025税制（2026页面核对）。适用23%档减636000日元，再加2.1%复兴特别所得税；国税应税所得按千日元向下取整。
<a id="source-tklocal"></a>
- **TKLOCAL** [个人住民税：税率、基本扣除及调整扣除](https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju)｜东京都主税局｜数据/规则年份：2025所得对应次年稳态税负。所得割合计10%；基本扣除43万日元；含均等割及森林环境税合计5000日元，减最低调整控除2500日元。
<a id="source-tkhealth"></a>
- **TKHEALTH** [2025东京职工健康保险费率表](https://www.kyoukaikenpo.or.jp/assets/13tokyo_7.pdf)｜全国健康保险协会｜数据/规则年份：2025。2025年3月起健康保险总费率9.91%，雇员承担一半。模型用实际工资连续近似标准报酬档次；30岁无需介护险。
<a id="source-tkpension"></a>
- **TKPENSION** [厚生年金保险料](https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20150515-01.html)｜日本年金机构｜数据/规则年份：2017起费率；2025适用。总费率18.3%，劳资各半。
<a id="source-tkpcap"></a>
- **TKPCAP** [厚生年金保険料額表](https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/20200825.html)｜日本年金机构｜数据/规则年份：2020起上限；2025适用。标准报酬月额上限650000日元；无奖金模型。
<a id="source-tkui"></a>
- **TKUI** [2025年度雇用保险费率](https://www.mhlw.go.jp/content/001401966.pdf)｜日本厚生劳动省｜数据/规则年份：2025。一般行业个人失业等保险费率5.5/1000，自2025-04起；模型固定此标准年化。
<a id="source-ustax"></a>
- **USTAX** [Federal income tax rates and brackets](https://www.irs.gov/filing/federal-income-tax-rates-and-brackets)｜美国IRS｜数据/规则年份：2025。Single；11925、48475美元分档，模型最高边际22%。
<a id="source-usbase"></a>
- **USBASE** [2025 Instructions for Form1040](https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf)｜美国IRS｜数据/规则年份：2025。单身标准扣除15750美元，采用2025最终法规，未使用旧版15000美元数字。
<a id="source-catax"></a>
- **CATAX** [2025 California Tax Rate Schedules](https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf)｜加州FTB｜数据/规则年份：2025。模型州应税所得落在57542至72724美元档，税率8%；用公式作估算，未逐档查50美元分组税表。
<a id="source-cabase"></a>
- **CABASE** [2025 Form540 booklet](https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html)｜加州FTB｜数据/规则年份：2025。单身标准扣除5706美元，模型含个人豁免抵免153美元，无其他抵免。
<a id="source-fica"></a>
- **FICA** [Social Security and Medicare withholding rates](https://www.irs.gov/taxtopics/tc751)｜美国IRS｜数据/规则年份：2025模型适用。雇员社安6.2%、Medicare1.45%；本例未达附加Medicare税门槛。
<a id="source-sscap"></a>
- **SSCAP** [Contribution and Benefit Base](https://www.ssa.gov/oact/cola/cbb.html)｜美国SSA｜数据/规则年份：2025。2025社安工资上限176100美元，本例未达到。
<a id="source-casdi"></a>
- **CASDI** [Contribution Rates and Withholding](https://edd.ca.gov/en/payroll_taxes/rates_and_withholding/)｜加州EDD｜数据/规则年份：2025。2025州残障险雇员1.2%；非2026的1.3%。

税后估算的复算假设与过程：

- 共同假设：30岁单身、无抚养、全年当地税务居民；全年固定工资按12个月发，前一年同薪。税前年收入人民币500000元，外币按统一汇率反推。无奖金、股权、其他收入、租房/子女专项抵扣。上海/深圳按2025下半年社保基数标准年化，日本按2025年3/4月后的费率年化，美国按2025最终税制。
- 只计雇员个税和强制社保；中国公积金及其税前扣除均未计，美国商业医保、401(k)未计。日本包含次年住民税的稳态负担，不能把刚入境首年少缴住民税当永久优势。医保档次、奖金结构和报税取整会产生小额差异。
- **上海**：本币年薪500,000.00，个人社保47,000.52，个税66,329.87；净额386,669.61，到手77.33%。详细公式和全部税源URL保留于JSON的note。
- **深圳**：本币年薪500,000.00，个人社保35,526.88，个税69,198.28；净额395,274.84，到手79.05%。详细公式和全部税源URL保留于JSON的note。
- **东京**：本币年薪11,781,615.97，个人社保1,362,277.96，个税1,203,217.87，住民税806,400.00；净额8,409,720.14，到手71.38%。详细公式和全部税源URL保留于JSON的note。
- **硅谷（南湾）**：本币年薪74,382.62，个人社保6,582.86，个税7,813.18，加州税2,725.18；净额57,261.40，到手76.98%。详细公式和全部税源URL保留于JSON的note。

5条最适合做成画面的对比（是数据结论，不是剧本）：

1. **“同样50万元税前年薪，南湾和上海的到手比例在本模型里很接近。”** 上海386669.61÷500000=77.33%；南湾384911.13÷500000=76.98%，仅差0.35个百分点，人民币年净额差1758.48元；深圳79.05%、东京71.38%。这是特定年龄、婚姻和2025冻结规则情景，未计公积金与美国商业医保，不是国民税负排名。来源：上列CNTAX至CASDI及FX；公式逐项保留于JSON。
2. **“上海相对深圳的工资优势，换一个就业口径就明显缩水。”** 用同一2024年官方工资：非私营239557÷174478−1=37.30%；私营113914÷95217−1=19.64%；差17.66个百分点。不能把其中一个部门均值称作全市工资。来源：[上海年鉴表2.23](https://tjj.sh.gov.cn/tjnj/2025tjnj/C0223.htm)、[深圳2024工资公报](https://www.sz.gov.cn/cn/xxgk/zfxxgj/tjsj/tjgb/content/post_12561969.html)。
3. **“上海、深圳都是超大城市，平均通勤仍可差出一年50小时。”** 同源2024单程上海39、深圳33分钟，深圳短(39−33)÷39=15.38%；若每年250个往返工作日，(39−33)×2×250÷60=50小时，相当于6.25个8小时工作日。250天是演示假设，不是法定工作日统计。来源：[报告原图第19页](https://huiyan.baidu.com/cms/report/2025tongqin/P29.png)，另用P30年度表核对；不与东京全天通勤通学时间混比。
4. **“上海独角兽总量比深圳多68%，按人口摊薄后只多约23%。”** 胡润2026上海74、深圳44家，74÷44−1=68.18%；用2025年末常住人口，上海74÷24.8541=2.977家/百万人，深圳44÷18.2485=2.411家/百万人，2.977÷2.411−1=23.48%。这是城市产业密度描述，不是个人找到好工作的概率；榜单和人口时点近似对齐。来源：[胡润原榜](https://hurun.cn/zh-CN/Info/Detail?num=E9GMNPY37G4Q)、[上海人口](https://tjj.sh.gov.cn/tjgb/20260330/e0772941e8e041eaaad2df850b44ef98.html)、[深圳人口](https://www.sz.gov.cn/attachment/1/1723/1723320/12848626.pdf)。
5. **“辅助样本里，南湾租金最高，但房价收入比最低。”** 2026年10月Numbeo San Jose一居月租3085.56×6.7220=人民币20741.13元，是上海6952.38元的2.98倍；但固定2026榜房价收入比San Jose为8.4，上海34.2，34.2÷8.4=4.07。两指标的分母及住宅模型不同；绝不能说“南湾买房比上海便宜4倍”。仅作为众包辅助画面，不作官方定论。来源：[San Jose租金](https://www.numbeo.com/cost-of-living/in/San-Jose)、[上海租金](https://www.numbeo.com/cost-of-living/in/Shanghai)、[固定2026房价收入比榜](https://www.numbeo.com/property-investment/rankings.jsp?title=2026)、[公式](https://www.numbeo.com/property-investment/indicators_explained.jsp)。

不确定或缺失清单：

- 上海2025年同定义非私营/私营工资：未核实到原表，主表保留2024；深圳2025最新值不能与上海2024直接解释成纯地域差异，已另外保留深圳2024用于同年比较。
- 官方软件工程师年薪中位数：上海、深圳、东京均null；自报总包另列，东京辅助地域较宽；南湾BLS工资不等于股票总包。
- 四城官方统一“市中心一居室”月租与统一房价收入比均null；众包辅助列有值，但房屋面积、质量、租约及中心区界限不能完全对齐。
- 东京平均单程上班通勤null；官方2021的95分钟包含通学和全天往返。上海/深圳大数据模型与美国ACS问卷也不是同一种调查。
- 独角兽：东京、南湾null；不能将未上榜或未取得完整清单解释为0，不能把旧金山222家当作南湾。四城统一上市科技公司数量均null。
- 近期统一年均温：南湾null（气候定性有来源）；上海暂用2024单年、深圳2025单年、东京1991–2020正常值，不能据此计算城市气候温差排名。
- 实际每周工时、统一中签概率、永住/落户成功率未作数字结论；表中40小时是法定通常工时/加班门槛。政策难度是条件描述，没有编造量化评分。
- H-1B费用诉讼执行状态可能变化；本次已核实2025公告、2026延期与2026-09-30法院原文，最后执行交叉说明为2026-10-01。发布前应再次查看是否有新的暂缓/上诉裁定。

机器文件约定：顶层仅四个城市，每个指标有value/unit/cny/year/source_url/note；未知值用JSON null。cny只承载货币转换，比例、人口、时间、政策文字的cny均为null，不表示其原始value缺失。辅助指标后缀_aux，不能静默回填官方缺失值。

验收自检（2026-10-17实际执行）：`python3 -c "import json;json.load(open('city_data.json'))"` 退出码0。结构检查通过：4城、89个指标、70项非空值均有来源和年份、19个明确null；30项货币换算通过；21行指标总表及85条来源锚点全部匹配。另用逐档累进法独立复算四城税后模型，5条结论的算术均通过。目录仅有city_data.md和city_data.json两个交付文件。此自检确认结构、溯源标注与计算，不代表不同调查口径已完全统一；未统一处与缺值已逐项说明。
