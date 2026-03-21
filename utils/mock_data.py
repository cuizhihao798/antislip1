import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)

VEHICLES = [
    {"id": "A01", "status": "作业", "battery": 78, "track": "1股道", "train": "G105", "task": "放鞋·后轮", "fault": None,     "status_color": "green"},
    {"id": "A02", "status": "放鞋", "battery": 55, "track": "2股道", "train": "G182", "task": "放鞋·前轮", "fault": None,     "status_color": "amber"},
    {"id": "A03", "status": "充电", "battery": 32, "track": "充电基地","train": "—",    "task": "自动对位",  "fault": None,     "status_color": "blue"},
    {"id": "A04", "status": "故障", "battery": 61, "track": "4股道", "train": "G307", "task": "旋转电机异常","fault": "E-214", "status_color": "red"},
]

TRACKS = [
    {"num": "1 股道", "train": "G105", "state": "停靠中", "style": "train-blue",  "task_badge": ("已放鞋 ✓", "green"), "vehicle": "A01"},
    {"num": "2 股道", "train": "G182", "state": "作业中", "style": "train-blue",  "task_badge": ("放鞋中...", "amber"), "vehicle": "A02"},
    {"num": "3 股道", "train": "—",    "state": "空闲",   "style": "",            "task_badge": ("待命",      "gray"),  "vehicle": ""},
    {"num": "4 股道", "train": "G307", "state": "待发车", "style": "train-amber", "task_badge": ("待取鞋 !",  "red"),   "vehicle": "A04故障"},
]

ALARMS = [
    {"id": "ALM-001", "level": "严重", "device": "A04", "code": "E-214",
     "title": "A04 · 旋转电机过载",
     "sub": "E-214 · 14:02:11 · 前轮旋转模组 · 电流超限42%",
     "suggest": "停止该机作业 → 检查机械臂卡阻 → 重置电机驱动器",
     "status": "待处理", "color": "red"},
    {"id": "ALM-002", "level": "预警", "device": "A02", "code": "W-103",
     "title": "A02 · 视觉模组遮挡预警",
     "sub": "W-103 · 14:29:55 · 前置传感器置信度下降",
     "suggest": "切换备用传感器 → 作业完成后清洁镜头",
     "status": "处理中", "color": "amber"},
    {"id": "ALM-003", "level": "预警", "device": "A01", "code": "W-401",
     "title": "A01 · 电池低电量预警",
     "sub": "W-401 · 13:45:00 · 电量低于30%阈值",
     "suggest": "已调度返回充电基地",
     "status": "已解决", "color": "green"},
]

DIM_STATUS = [
    ("旋转电机电流",  "A04: 142%", "red"),
    ("视觉传感器信号","A02: 68%",  "amber"),
    ("激光测距高度",  "正常",      "green"),
    ("电池 SoC",      "A03: 32%",  "blue"),
    ("通信链路",      "全部在线",  "green"),
    ("动作行程编码器","正常",      "green"),
    ("压力传感器",    "正常",      "green"),
    ("环境温度",      "28°C",      "green"),
    ("IP防护等级",    "IP65 ✓",    "green"),
    ("GPS/限界传感",  "正常",      "green"),
    ("充电耦合精度",  "±18mm ✓",   "green"),
    ("远程通讯链路",  "在线",      "green"),
]

def gen_records(n=38):
    now = datetime(2026, 3, 21, 14, 32, 8)
    rows = []
    ops = ["放鞋·前轮", "放鞋·后轮", "取鞋·前轮", "取鞋·后轮"]
    trains = ["G105", "G182", "G219", "G307", "G412"]
    tracks = ["1股道", "2股道", "3股道", "4股道"]
    for i in range(n):
        t = now - timedelta(minutes=i * 8 + random.randint(0, 4))
        dev = random.choice(["A01", "A02", "A03"])
        ok = random.random() > 0.05
        rows.append({
            "时间戳": t.strftime("%H:%M:%S"),
            "设备": dev,
            "股道/车次": f"{random.choice(tracks)} / {random.choice(trains)}",
            "操作类型": random.choice(ops),
            "视觉置信度": f"{random.uniform(93,99.5):.1f}%",
            "压力验证": "双验证 ✓" if ok else "—",
            "电量": f"{random.randint(30,95)}%",
            "结果": "成功" if ok else "失败",
        })
    rows[0] = {
        "时间戳": "14:30:12", "设备": "A02", "股道/车次": "2股道 / G182",
        "操作类型": "放鞋·前轮", "视觉置信度": "96.3%",
        "压力验证": "等待中", "电量": "55%", "结果": "执行中",
    }
    return pd.DataFrame(rows)

def gen_week_bar():
    labels = ["周一","周二","周三","周四","周五","周六","今日"]
    vals = [28, 35, 30, 46, 43, 48, 38]
    return labels, vals

def gen_energy_curve():
    hours = [f"{h:02d}:00" for h in range(8, 15)]
    vals  = [12, 28, 45, 68, 88, 95, 87]
    return hours, vals

INTERLOCK = [
    ("列车已完全停稳，收到停车信号", "ok"),
    ("防溜车已抵达指定位置",         "ok"),
    ("视觉定位已完成锁定",           "ok"),
    ("发车前防溜车已撤回安全限界",   "warn"),
    ("设备无故障（A04 电机异常）",   "err"),
]

FLOW_STEPS = ["待机", "移动", "视觉定位", "放铁鞋", "返回", "充电"]
A02_ACTIVE = 3
