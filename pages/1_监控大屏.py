import streamlit as st
import pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.theme import load_css, badge, alarm_strip, lock_row, flow_steps, metric_accent
from utils.mock_data import VEHICLES, TRACKS, ALARMS, INTERLOCK, FLOW_STEPS, A02_ACTIVE, gen_energy_curve
import plotly.graph_objects as go

st.set_page_config(page_title="监控大屏 · 防溜车系统", page_icon="📡", layout="wide")
load_css()

# ── 顶栏 ──────────────────────────────────────────────────
col_t, col_r = st.columns([3, 1])
with col_t:
    st.markdown("""
    <div style="padding:4px 0 12px">
      <div style="font-size:18px;font-weight:500;color:#e2e8f0">全景智能监控大屏</div>
      <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;margin-top:2px">
        实时更新 · 最后刷新 14:32:08
      </div>
    </div>""", unsafe_allow_html=True)
with col_r:
    st.markdown("<div style='padding-top:8px'></div>", unsafe_allow_html=True)
    if st.button("🔴 紧急停机", type="primary"):
        st.error("⚠️ 紧急停机指令已下发！请确认现场安全。")

st.divider()

# ── 指标卡 ────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(metric_accent("ONLINE VEHICLES", "3 / 4", "1台充电中 · A03", "blue"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_accent("SYSTEM UPTIME", "99.97%", "目标 ≥99.9% ✓", "green"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_accent("TODAY TASKS", "38", "放 19 · 取 19", "cyan"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_accent("BASE STORAGE", "87%", "冗余 >30% ✓", "amber"), unsafe_allow_html=True)
with c5:
    st.markdown(metric_accent("ACTIVE ALARMS", "2", "严重 1 · 预警 1", "red"), unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── 股道拓扑 + 防溜车状态 ─────────────────────────────────
col_map, col_veh = st.columns([1.3, 1])

with col_map:
    # 股道拓扑
    track_html = '<div class="rail-card"><div class="rail-card-title">场站股道拓扑</div><div class="track-wrap">'
    for t in TRACKS:
        dot_color = {"train-blue": "#3b82f6", "train-amber": "#f59e0b", "": "#475569"}.get(t["style"], "#475569")
        train_div = ""
        if t["train"] != "—":
            train_div = f'<div class="track-train {t["style"]}" style="width:85%"><span style="width:6px;height:6px;border-radius:50%;background:{dot_color};display:inline-block;flex-shrink:0"></span>{t["train"]} · {t["state"]}</div>'
        else:
            train_div = '<span style="font-size:10px;color:#475569">空闲</span>'
        task_text, task_color = t["task_badge"]
        track_html += f"""
        <div class="track-row-item">
          <span class="track-num">{t["num"]}</span>
          <div class="track-rail">{train_div}</div>
          <div class="track-status">
            {badge(task_text, task_color)}
            <span style="font-size:10px;color:#475569;font-family:'JetBrains Mono',monospace">{t["vehicle"]}</span>
          </div>
        </div>"""
    track_html += """</div>
    <div style="margin-top:12px;padding-top:10px;border-top:1px solid #1e3260;
                display:flex;gap:16px;font-size:10px;color:#475569;font-family:'JetBrains Mono',monospace">
      <span><span style="color:#10b981">●</span> 正常/已放</span>
      <span><span style="color:#f59e0b">●</span> 作业中</span>
      <span><span style="color:#ef4444">●</span> 故障/待处</span>
      <span><span style="color:#3b82f6">●</span> 充电</span>
    </div></div>"""
    st.markdown(track_html, unsafe_allow_html=True)

    # A02 作业流程
    flow_html = f"""
    <div class="rail-card">
      <div class="rail-card-title">A02 · 作业流程追踪</div>
      {flow_steps(FLOW_STEPS, A02_ACTIVE)}
      <div style="margin-top:10px;font-size:10px;color:#475569;font-family:'JetBrains Mono',monospace;line-height:1.8">
        定位阶段：粗定位 ✓ → 精定位 ✓ → <span style="color:#06b6d4">亚像素锁定 ✓</span>
        &nbsp;|&nbsp; 压力检测：<span style="color:#f59e0b">等待接触...</span>
      </div>
    </div>"""
    st.markdown(flow_html, unsafe_allow_html=True)

with col_veh:
    # 防溜车卡
    veh_html = '<div class="rail-card"><div class="rail-card-title">防溜车实时状态</div>'
    color_map = {"green": "#10b981", "amber": "#f59e0b", "blue": "#3b82f6", "red": "#ef4444"}
    card_class = {"green": "vcard", "amber": "vcard", "blue": "vcard vcard-charging", "red": "vcard vcard-fault"}
    for v in VEHICLES:
        batt_color = color_map[v["status_color"]]
        st.markdown(f"""
        <div class="{card_class[v['status_color']]}" style="margin-bottom:8px">
          <div class="vcard-id">{v['id']} {badge(v['status'], v['status_color'])}</div>
          <div class="batt-outer"><div class="batt-inner" style="width:{v['battery']}%;background:{batt_color}"></div></div>
          <div class="vcard-sub">{v['battery']}% · {v['task']}<br>{v['track']} · {v['train']}</div>
        </div>""", unsafe_allow_html=True)
    veh_html += "</div>"

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── 补能 + 报警 + 互锁 ────────────────────────────────────
col_e, col_a, col_l = st.columns([1, 1, 1])

with col_e:
    hours, vals = gen_energy_curve()
    fig = go.Figure(go.Bar(
        x=hours, y=vals,
        marker_color=["#2a4480","#2a4480","#2a4480","#3b82f6","#3b82f6","#3b82f6","#3b82f6"],
        marker_line_width=0,
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=120,
        xaxis=dict(showgrid=False, tickfont=dict(color="#475569", size=10, family="JetBrains Mono"), tickangle=0),
        yaxis=dict(showgrid=False, visible=False),
        bargap=0.15,
    )
    st.markdown('<div class="rail-card"><div class="rail-card-title">双源太阳能补能 · 今日功率</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div style="font-size:10px;color:#475569;font-family:'JetBrains Mono',monospace;line-height:1.8;margin-top:-8px">
      基地剩余：<span style="color:#10b981">充裕（冗余 &gt;30%）</span><br>
      A03 对接精度：<span style="color:#06b6d4">±18mm ✓</span>
    </div></div>""", unsafe_allow_html=True)

with col_a:
    alarm_html = '<div class="rail-card"><div class="rail-card-title">活跃报警</div>'
    for a in ALARMS:
        alarm_html += alarm_strip(a["title"], a["sub"], a["color"])
    alarm_html += "</div>"
    st.markdown(alarm_html, unsafe_allow_html=True)

with col_l:
    lock_html = '<div class="rail-card"><div class="rail-card-title">全过程逻辑互锁</div>'
    for text, status in INTERLOCK:
        lock_html += lock_row(text, status)
    lock_html += """
    <div style="margin-top:10px;padding:8px 12px;background:rgba(239,68,68,.06);
                border:1px solid rgba(239,68,68,.2);border-radius:5px;
                font-size:10px;color:#ef4444;font-family:'JetBrains Mono',monospace;line-height:1.6">
      ⚠ A04 指令已锁定<br>故障码 E-214 排除前禁止该车作业
    </div></div>"""
    st.markdown(lock_html, unsafe_allow_html=True)

# ── 自动刷新 ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    auto = st.toggle("自动刷新", value=True)
    interval = st.select_slider("刷新间隔", options=[5, 10, 30, 60], value=10)
    st.markdown(f"<div style='font-size:10px;color:#475569;font-family:var(--mono)'>每 {interval} 秒刷新</div>",
                unsafe_allow_html=True)
    if auto:
        time.sleep(interval)
        st.rerun()
