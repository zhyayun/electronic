# 硬件学习笔记

个人硬件知识学习与实践项目，涵盖模拟电子、数字电子、电子控制与电源设计。

## 📚 学习方向

| 方向 | 核心内容 |
|------|----------|
| 模拟电子（模电） | 二极管 / 三极管 / MOSFET、放大电路、运放、滤波、反馈 |
| 数字电子（数电） | 逻辑门、组合/时序逻辑、触发器、ADC/DAC、常用数字接口 |
| 电子控制（电控） | MCU 基础、PWM、电机驱动、PID 控制、传感器与闭环 |
| 电源 | LDO / DCDC（Buck/Boost）、线性与开关电源、电池充电、电源完整性 |

## 📁 目录结构

```
electronic/
├── analog/        # 模电：笔记、仿真、电路分析
├── digital/       # 数电：逻辑设计、时序分析
├── control/       # 电控：MCU 工程、控制算法、驱动
├── power/         # 电源：拓扑、设计计算、实测
├── tools/         # 工具链与仿真环境说明
└── docs/          # 参考资料、学习记录
```

## 🛠️ 工具

- 仿真：LTspice / Multisim / TINA-TI
- 电路设计：KiCad / Altium Designer
- MCU 开发：STM32CubeIDE / Keil / PlatformIO
- 仪器：示波器、万用表、电子负载、可调电源

## 📖 学习方法

1. **理论**：搞懂公式与物理含义，记推导过程
2. **仿真**：LTspice 验证电路，观察波形
3. **动手**：洞洞板/PCB 实物验证，用仪器测量
4. **复盘**：对比理论、仿真与实测差异并记录

## 📌 进度记录

- [ ] 模电：半导体器件基础
- [ ] 数电：逻辑代数与门电路
- [ ] 电控：GPIO / PWM / 定时器
- [ ] 电源：LDO 与 Buck 基础

## 🔗 参考资料

- 教材：童诗白《模拟电子技术基础》、阎石《数字电子技术基础》
- [电源网](https://www.dianyuan.com/)：电源工程师社区，偏工程实战
  - [送给新手的电路设计指南](https://www.dianyuan.com/eestar/article-topcis/16.html)：基础/进阶/高级三档，入门先看基础篇
  - [开关电源宝典：3 分钟搞懂 Buck 降压原理](https://www.dianyuan.com/eestar/article-12182.html)
  - [开关电源负反馈设计连载（1~5）](https://www.dianyuan.com/eestar/article-453.html)
  - [论坛](https://www.dianyuan.com/bbs/)：搜索具体问题、调试经验

## 📝 说明

本仓库仅用于个人学习记录，内容如有错误欢迎随时指正。
