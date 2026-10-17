#!/usr/bin/env python3
"""Recompute the four fixed city scenarios; print the table in takehome.md.

Python standard library only. Inputs: adjacent city_data.json (read only).
Money is rounded to CNY cents with ROUND_HALF_UP after local tax calculation.
This preserves the frozen JSON CNY input values and exact accounting identities.
"""
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
import json
from pathlib import Path


D = lambda value: Decimal(str(value))
ROOT = Path(__file__).resolve().parent
FX = {"上海": D(1), "深圳": D(1), "东京": D("0.042439"),
      "硅谷（南湾）": D("6.7220")}
FIELDS = ("total_comp_cny", "tax_social_total_cny", "take_home_cny",
          "take_home_percent", "annual_rent_cny", "remaining_cny",
          "rent_to_take_home_percent")


def rounded(value, places="0.01"):
    return value.quantize(D(places), rounding=ROUND_HALF_UP)


def floor1000(value):
    return (value / 1000).to_integral_value(rounding=ROUND_FLOOR) * 1000


def progressive(value, bands):
    tax, lower = D(0), D(0)
    for upper, rate in bands:
        upper = D(upper)
        tax += max(D(0), min(value, upper) - lower) * D(rate)
        lower = upper
    return tax


def calculate():
    source = json.loads((ROOT / "city_data.json").read_text(encoding="utf-8"))
    rows = {}
    for city, fx in FX.items():
        comp = source[city]["software_engineer_median_total_comp_aux"]
        rent = source[city]["city_center_1br_rent_aux"]
        g, monthly = D(comp["value"]), D(rent["cny"])
        gross = D(comp["cny"])
        formulas = {}
        if city == "上海":
            base = min(g / 12, D(37302)) * 12
            b = {"pension": base * D(".08"), "health": base * D(".02"),
                 "unemployment": base * D(".005")}
            social = sum(b.values())
            b["income_tax"] = (g - 60000 - social) * D(".30") - 52920
            formulas = {
                "pension": "min(666112/12,37302)×12×8%",
                "health": "min(666112/12,37302)×12×2%",
                "unemployment": "min(666112/12,37302)×12×0.5%",
                "income_tax": "(666112−60000−47000.52)×30%−52920",
            }
        elif city == "深圳":
            b = {"pension": min(g / 12, D(27549)) * 12 * D(".08"),
                 "health": min(g / 12, D(33666)) * 12 * D(".02"),
                 "unemployment": min(g / 12, D(44265)) * 12 * D(".002")}
            social = sum(b.values())
            b["income_tax"] = (g - 60000 - social) * D(".25") - 31920
            formulas = {
                "pension": "min(505231/12,27549)×12×8%",
                "health": "min(505231/12,33666)×12×2%",
                "unemployment": "min(505231/12,44265)×12×0.2%",
                "income_tax": "(505231−60000−35537.342)×25%−31920",
            }
        elif city == "东京":
            # Same continuous approximation to standard remuneration as city_data.
            b = {"health": min(g / 12, D(1390000)) * 12 * D(".04955"),
                 "pension": min(g / 12, D(650000)) * 12 * D(".0915"),
                 "unemployment": g * D(".0055")}
            social = sum(b.values())
            taxable = floor1000(g - 1950000 - social - 580000)
            b["income_tax"] = (taxable * D(".20") - 427500) * D("1.021")
            b["resident_tax"] = floor1000(g - 1950000 - social - 430000) * D(".1") + 5000 - 2500
            formulas = {
                "health": "min(8539096/12,1390000)×12×4.955%（连续近似）",
                "pension": "min(8539096/12,650000)×12×9.15%",
                "unemployment": "8539096×0.55%",
                "income_tax": "(floor1000(8539096−1950000−1183777.2348−580000)×20%−427500)×1.021 = (4825000×20%−427500)×1.021",
                "resident_tax": "floor1000(8539096−1950000−1183777.2348−430000)×10%+5000−2500 = 4975000×10%+2500",
            }
        else:
            b = {"social_security": min(g, D(176100)) * D(".062"),
                 "medicare": g * D(".0145"),
                 "additional_medicare": max(D(0), g - 200000) * D(".009"),
                 "sdi": g * D(".012")}
            b["federal_tax"] = progressive(g - 15750, [
                (11925, ".10"), (48475, ".12"), (103350, ".22"),
                (197300, ".24"), (250525, ".32"), (626350, ".35"),
                ("Infinity", ".37")])
            b["state_tax"] = max(D(0), progressive(g - 5706, [
                (11079, ".01"), (26264, ".02"), (41452, ".04"),
                (57542, ".06"), (72724, ".08"), (371479, ".093"),
                (445771, ".103"), (742953, ".113"), ("Infinity", ".123")]) - 153)
            formulas = {
                "social_security": "min(233750,176100)×6.2%",
                "medicare": "233750×1.45%（不封顶）",
                "additional_medicare": "max(233750−200000,0)×0.9%",
                "sdi": "233750×1.2%（2025不封顶）",
                "federal_tax": "应税额=233750−15750=218000；11925×10%+36550×12%+54875×22%+93950×24%+20700×32%",
                "state_tax": "应税额=233750−5706=228044；3201.97+(228044−72724)×9.3%−153",
            }
        tax = rounded(sum(b.values()) * fx)
        net = rounded(gross - tax)
        annual_rent = rounded(monthly * 12)
        remaining = net - annual_rent
        values = [gross, tax, net, rounded(net / gross * 100, ".000001"),
                  annual_rent, remaining,
                  rounded(annual_rent / net * 100, ".000001")]
        row = {key: float(value) for key, value in zip(FIELDS, values)}
        row["formulas"] = {
            "total_comp_cny": f"city_data.json 自报总包原值 {g}×{fx}；采用已存人民币值 {gross}",
            "tax_social_total_cny": f"round2(({' + '.join(str(v) for v in b.values())})×{fx}) = {tax}",
            "take_home_cny": f"{gross}−{tax} = {net}",
            "take_home_percent": f"{net}÷{gross}×100%",
            "annual_rent_cny": f"{monthly}×12 = {annual_rent}",
            "remaining_cny": f"{net}−{annual_rent} = {remaining}",
            "rent_to_take_home_percent": f"{annual_rent}÷{net}×100%",
        }
        row["currency"] = comp["unit"].split("/")[0]
        row["total_comp_local"] = float(g)
        row["monthly_rent_cny"] = float(monthly)
        row["fx_cny_per_local"] = float(fx)
        row["breakdown_local"] = {k: float(v) for k, v in b.items()}
        row["breakdown_formulas"] = formulas
        row["input_sources"] = {"total_comp": comp["source_url"], "rent": rent["source_url"],
                                "previous_tax_model": f"city_data.json / {city} / modeled_take_home_annual"}
        rows[city] = row
    return {
        "metadata": {
            "tax_year": 2025, "input_snapshot_year": 2026, "fx_date": "2026-10-16",
            "money_unit": "CNY/year", "percent_unit": "percent (0–100)",
            "assumptions": "30岁单身无抚养、全年当地税务居民、前一年同薪；总包（含股票）全部按工资并均分12个月；不使用奖金/股权优惠；中国不扣公积金及其税前扣除；美国标准扣除，不扣商业医保/401(k)；日本计次年住民税稳态；沿用2025下半年标准年化和日本标准报酬连续近似。",
            "rounding": "本币分项不先取整（日本应税额按千日元向下取整）；税社保本币合计乘汇率后四舍五入至人民币分；到手用city_data已存人民币总包减该合计；年租用已存人民币月租×12；比例以人民币分计算并保留6位小数。",
            "meaning_of_remaining": "仅减税社保和房租，未减餐饮交通等其他开支，不是全年储蓄。自报薪酬和众包租金均仅辅助；东京薪酬覆盖Greater Tokyo Area，南湾代理为San Jose。",
            "source_model": "city_data.md；city_data.json（均只读）",
        },
        "cities": rows,
    }


def render_table(result):
    lines = ["| 城市 | 总包 | 税社保合计 | 到手 | 到手比例 | 年租金 | 剩余 | 房租/到手 |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for city, row in result["cities"].items():
        cells = [f"{D(row[key]) / 10000:.1f}" if "percent" not in key
                 else f"{D(row[key]):.1f}%" for key in FIELDS]
        lines.append("| " + " | ".join([city] + cells) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(render_table(calculate()))
