import streamlit as st
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.theme import load_css, badge, metric_accent
from utils.mock_data import gen_records, gen_week_bar, gen_energy_curve
import plotly.graph_objects as go
import io

st.set_page_config(page_title="报表中心 · 防溜车系统", page_icon="📊", layout="wide")
load_css()

st.markdown("""
<div style="padding:4px 0 12px">
  <div style="font-size:18px;font-weight:500;color:#e2e8f0">自动报表与产量分析中心</div>
  <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;margin-top:2px">
    数字化作业记录 · 全流程溯源 · 一车一记录
  </div>
</div>""", unsafe_allow_html=True)
st.divider()

# ── 指标 ──────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_accent("TODAY TASKS", "38", "放鞋 19 · 取鞋 19", "blue"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_accent("SUCCESS RATE", "97.4%", "1次失败 · A04故障", "green"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_accent("WEEK TOTAL", "214", "较上周 +12%", "amber"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_accent("REPORTS GEN.", "38", "含8项关键参数", "purple"), unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── 溯源记录表 ────────────────────────────────────────────
col_table, col_chart = st.columns([1.6, 1])

with col_table:
    st.markdown('<div class="rail-card"><div class="rail-card-title">防溜作业记录 · 溯源报表</div>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([2, 1, 1])
    with fc1:
        search = st.text_input("搜索", placeholder="时间 / 设备 / 车次...", label_visibility="collapsed")
    with fc2:
        result_filter = st.selectbox("结果", ["全部", "成功", "失败", "执行中"], label_visibility="collapsed")
    with fc3:
        dev_filter = st.selectbox("设备", ["全部", "A01", "A02", "A03", "A04"], label_visibility="collapsed")

    df = gen_records(38)
    if search:
        mask = df.apply(lambda r: search in " ".join(r.astype(str)), axis=1)
        df = df[mask]
    if result_filter != "全部":
        df = df[df["结果"].str.contains(result_filter)]
    if dev_filter != "全部":
        df = df[df["设备"] == dev_filter]

    def style_result(val):
        if "成功" in val:  return "color:#10b981;font-weight:500"
        if "失败" in val:  return "color:#ef4444;font-weight:500"
        if "执行中" in val:return "color:#3b82f6;font-weight:500"
        return "color:#94a3b8"

    styled = df.style.applymap(style_result, subset=["结果"])
    st.dataframe(styled, use_container_width=True, hide_index=True, height=340)

    # 导出按钮
    buf = io.BytesIO()
    df.to_excel(buf, index=False, engine="openpyxl")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.download_button("⬇ 导出 Excel", data=buf.getvalue(),
                           file_name="防溜作业记录.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    with col_e2:
        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇ 导出 CSV", data=csv_data,
                           file_name="防溜作业记录.csv",
                           mime="text/csv", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    # 周趋势柱图
    labels, vals = gen_week_bar()
    colors = ["#2a4480"] * 6 + ["#f59e0b"]
    fig_week = go.Figure(go.Bar(x=labels, y=vals, marker_color=colors, marker_line_width=0))
    fig_week.update_layout(
        margin=dict(l=0, r=0, t=4, b=0), height=160,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="#475569", size=11, family="JetBrains Mono")),
        yaxis=dict(showgrid=False, visible=False),
        bargap=0.2,
    )
    st.markdown('<div class="rail-card"><div class="rail-card-title">本周作业量趋势</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_week, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # 能源曲线
    hours, energy = gen_energy_curve()
    fig_e = go.Figure(go.Scatter(
        x=hours, y=energy,
        mode="lines+markers",
        line=dict(color="#06b6d4", width=2),
        marker=dict(color="#06b6d4", size=5),
        fill="tozeroy",
        fillcolor="rgba(6,182,212,0.08)",
    ))
    fig_e.update_layout(
        margin=dict(l=0, r=0, t=4, b=0), height=140,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="#475569", size=10, family="JetBrains Mono")),
        yaxis=dict(showgrid=False, visible=False),
    )
    st.markdown('<div class="rail-card"><div class="rail-card-title">太阳能补能功率曲线</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_e, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # API 接口状态
    api_html = '<div class="rail-card"><div class="rail-card-title">数据上传接口状态</div>'
    apis = [
        ("MQTT 上行链路", "在线", "green"),
        ("Restful API 接口", "在线", "green"),
        ("上层管理系统同步", "实时", "green"),
    ]
    for name, val, color in apis:
        api_html += f"""
        <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
                    border-bottom:1px solid #1e3260;font-size:11px">
          <span style="width:6px;height:6px;border-radius:50%;background:#10b981;
                       box-shadow:0 0 6px #10b981;display:inline-block;flex-shrink:0"></span>
          <span style="flex:1;color:#94a3b8">{name}</span>
          {badge(val, color)}
        </div>"""
    api_html += '<div style="font-size:10px;color:#475569;font-family:\'JetBrains Mono\',monospace;margin-top:8px">最后上传 14:32:01 · 本日 38 条</div></div>'
    st.markdown(api_html, unsafe_allow_html=True)
