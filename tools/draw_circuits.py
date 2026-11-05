# 电路原理图 SVG 生成器
# 用法: python tools/draw_circuits.py
# 输出: analog/images/*.svg
# 约定: 1px = 1 单位; 无背景(透明); 线条 currentColor, 标注 var(--muted), 信号 var(--accent)
import os

WIRE = "currentColor"
TXT = "var(--fg)"
MUTED = "var(--muted)"
ACC = "var(--accent)"
FONT = "Menlo, Consolas, 'Courier New', monospace"


class Svg:
    def __init__(self, w, h, label):
        self.a = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">',
            '<rect width="100%" height="100%" fill="none"/>',
        ]

    def line(self, x1, y1, x2, y2, color=WIRE, sw=2):
        self.a.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{sw}" fill="none"/>')

    def poly(self, pts, color=WIRE, sw=2, fill="none"):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.a.append(f'<polygon points="{p}" stroke="{color}" '
                      f'stroke-width="{sw}" fill="{fill}"/>')

    def circle(self, cx, cy, r, color=WIRE, sw=2):
        self.a.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" '
                      f'stroke="{color}" stroke-width="{sw}" fill="none"/>')
    def rect(self, x, y, w, h, color=WIRE, sw=2):
        self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                      f'stroke="{color}" stroke-width="{sw}" fill="none"/>')

    def text(self, x, y, t, size=15, color=TXT, anchor="middle", italic=False):
        ai = ' font-style="italic"' if italic else ""
        anc = {"start": "start", "end": "end"}.get(anchor, "middle")
        self.a.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{color}" text-anchor="{anc}"{ai}>{t}</text>')

    def node(self, x, y, color=WIRE):
        self.a.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{color}"/>')

    def arrow_head(self, x, y, dx, dy, color=WIRE, sw=2, size=7):
        # 在 (x,y) 处沿方向 (dx,dy) 画箭头两翼
        import math
        a = math.atan2(dy, dx)
        for da in (math.radians(150), math.radians(-150)):
            self.line(x, y, x + size*math.cos(a+da), y + size*math.sin(a+da), color, sw)

    # ---------- 元件 ----------
    def resistor_v(self, x, y0, y1, label=None, lx=1):
        self.line(x, y0, x, y0+10)
        self.rect(x-11, y0+10, 22, y1-y0-20)
        self.line(x, y1-10, x, y1)
        if label:
            self.text(x + 16*lx, (y0+y1)/2+5,
                      anchor="start" if lx > 0 else "end", t=label)

    def resistor_h(self, x0, x1, y, label=None, ly=-1):
        self.line(x0, y, x0+10, y)
        self.rect(x0+10, y-11, x1-x0-20, 22)
        self.line(x1-10, y, x1, y)
        if label:
            self.text((x0+x1)/2, y - 16 if ly < 0 else y + 27, label)

    def capacitor_v(self, x, y0, y1, label=None):
        mid = (y0+y1)/2
        self.line(x, y0, x, mid-9)
        self.line(x-15, mid-9, x+15, mid-9, sw=2.6)
        self.line(x-15, mid+9, x+15, mid+9, sw=2.6)
        self.line(x, mid+9, x, y1)
        if label:
            self.text(x+16, mid+5, label, anchor="start")

    def diode_h(self, x0, x1, y, label=None):
        """阳极在左, 阴极在右, 正向电流方向 →"""
        self.line(x0, y, x0+6, y)
        self.poly([(x0+6, y-12), (x0+6, y+12), (x1-8, y)])
        self.line(x1-8, y-13, x1-8, y+13, sw=2.6)
        self.line(x1-8, y, x1, y)
        if label:
            self.text((x0+x1)/2, y-16, label, color=MUTED)

    def zener_v(self, x, y0, y1, label=None):
        """阴极在上"""
        mid = (y0+y1)/2
        self.line(x, y0, x, mid-12)
        self.line(x-12, mid-12, x+12, mid-12, sw=2.6)            # 阴极横杠
        self.line(x-12, mid-12, x-17, mid-4)                    # 两端向外下折(齐纳标记)
        self.line(x+12, mid-12, x+17, mid-4)
        self.poly([(x-10, mid+12), (x+10, mid+12), (x, mid-2)], fill=WIRE)  # 实心阳极三角
        self.line(x, mid+12, x, y1)
        if label:
            self.text(x+16, mid+5, label, anchor="start")

    def ground(self, x, y):
        self.line(x, y, x, y+7)
        self.line(x-15, y+7, x+15, y+7, sw=2.6)
        self.line(x-9, y+13, x+9, y+13, sw=2.6)
        self.line(x-3.5, y+19, x+3.5, y+19, sw=2.6)

    def terminal(self, x, y, t, dy=-10):
        self.node(x, y)
        self.text(x, y+dy, t, size=14, color=MUTED)

    def save(self, path):
        self.a.append('</svg>')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.a))


# ---------------- 图 1: 分压 ----------------
def fig_voltage_divider(out):
    s = Svg(250, 260, "分压电路")
    s.terminal(120, 30, "Vin")
    s.line(120, 30, 120, 55)
    s.resistor_v(120, 55, 120, "R1")
    s.node(120, 120)
    s.text(145, 116, "Vout", color=ACC, anchor="start", italic=True)
    s.resistor_v(120, 120, 185, "R2")
    s.ground(120, 190)
    s.save(out)


# ---------------- 图 2: RC 充放电 ----------------
def fig_rc_charge(out):
    s = Svg(250, 260, "RC 充放电电路")
    s.terminal(120, 30, "Vin")
    s.line(120, 30, 120, 55)
    s.resistor_v(120, 55, 120, "R")
    s.node(120, 120)
    s.text(145, 116, "Vc(t)", color=ACC, anchor="start")
    s.capacitor_v(120, 120, 190, "C")
    s.ground(120, 195)
    s.save(out)


# ---------------- 图 3: 半波整流 ----------------
def fig_half_wave(out):
    s = Svg(320, 190, "半波整流电路")
    # 左侧交流源(竖在左边框上)
    s.line(60, 40, 60, 62)
    s.circle(60, 85, 22)
    s.text(60, 92, "~", size=20)
    s.line(60, 107, 60, 140)
    # 上边框
    s.line(60, 40, 100, 40)
    s.diode_h(100, 140, 40, "D")
    s.node(140, 40)
    s.line(140, 40, 190, 40)
    s.resistor_h(190, 260, 40, "RL（负载）")
    # 右边框 + 下边框
    s.line(260, 40, 260, 140)
    s.line(60, 140, 260, 140)
    s.text(225, 72, "Vout", color=ACC)
    s.save(out)


# ---------------- 图 4: 稳压管稳压 ----------------
def fig_zener(out):
    s = Svg(300, 270, "稳压管并联稳压电路")
    s.terminal(100, 28, "Vin")
    s.line(100, 28, 100, 50)
    s.resistor_v(100, 50, 115, "Rs 限流")
    s.node(100, 115)
    s.line(100, 115, 200, 115)
    s.terminal(200, 115, "Vout", dy=-12)
    s.zener_v(100, 115, 190, "Dz")
    s.line(200, 115, 200, 130)
    s.resistor_v(200, 130, 190, "RL")
    s.line(100, 190, 200, 190)
    s.ground(100, 190)
    s.ground(200, 190)
    s.save(out)


# ---------------- 图 5: BJT 低侧开关 ----------------
def fig_bjt_switch(out):
    s = Svg(310, 290, "NPN 三极管低侧开关")
    s.terminal(130, 26, "Vcc")
    s.line(130, 26, 130, 48)
    s.resistor_v(130, 48, 110, "Rc（负载）")
    # 三极管
    s.circle(130, 165, 28)
    s.line(130, 110, 130, 137)                                   # 集电极引线
    s.line(112, 146, 112, 184, sw=2.6)                           # 基极竖杠
    s.line(130, 137, 114, 152)                                   # 集电极斜臂
    s.line(114, 178, 130, 193)                                   # 发射极斜臂
    s.arrow_head(130, 193, 10, 9)                                # 发射极箭头(朝外)
    # 基极回路
    s.line(112, 165, 96, 165)
    s.resistor_h(30, 96, 165, "Rb")
    s.terminal(30, 165, "GPIO", dy=-12)
    # 发射极接地
    s.line(130, 193, 130, 215)
    s.ground(130, 215)
    s.text(168, 160, "Q1", anchor="start", color=MUTED)
    s.save(out)


# ---------------- 图 6: MOSFET 低侧开关 ----------------
def fig_mos_switch(out):
    s = Svg(310, 300, "N 沟道 MOSFET 低侧开关")
    s.terminal(140, 26, "Vcc")
    s.line(140, 26, 140, 48)
    s.resistor_v(140, 48, 110, "负载")
    # MOS: 漏极-沟道(增强型断沟 + 三条短划线)
    s.line(140, 110, 140, 142)                                  # 漏极引线
    for yy in (156, 172, 188):                                   # 沟道短划
        s.line(133, yy, 147, yy, sw=2)
    s.line(140, 202, 140, 222)                                  # 源极引线
    s.arrow_head(132, 196, -8, 0)                               # 衬底箭头(指向栅极)
    s.line(140, 196, 133, 196)
    # 栅极(与沟道断开的竖板)
    s.line(108, 148, 108, 196, sw=2.8)
    s.line(108, 172, 92, 172)
    s.resistor_h(38, 92, 172, "Rg")
    s.terminal(38, 172, "GPIO", dy=-12)
    # 栅极下拉
    s.node(108, 172)
    s.line(108, 172, 108, 200)
    s.resistor_v(108, 200, 244, "Rgs 100k", lx=-1)
    # 源极接地
    s.ground(140, 222)
    s.ground(108, 244)
    s.text(165, 158, "Q1 N-MOS", anchor="start", color=MUTED)
    s.save(out)


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "analog", "images")
    figs = {
        "voltage-divider.svg": fig_voltage_divider,
        "rc-charge.svg": fig_rc_charge,
        "half-wave-rectifier.svg": fig_half_wave,
        "zener-regulator.svg": fig_zener,
        "bjt-switch.svg": fig_bjt_switch,
        "mosfet-switch.svg": fig_mos_switch,
    }
    for name, fn in figs.items():
        fn(os.path.join(base, name))
        print("generated", name)
