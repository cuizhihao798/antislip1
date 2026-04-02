import streamlit as st
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.theme import load_css, badge, metric_accent
from utils.state import init_state
from utils.mock_data import gen_week_bar, gen_energy_curve
import plotly.graph_objects as go
import pandas as pd
import io

st.set_page_config(page_title="报表中心 · 防溜车系统", page_icon="📊", layout="wide")
load_css()
init_state()

st.markdown("""
<div style="padding:4px 0 12px">
  <div style="font-size:18px;font-weight:500;color:#e2e8f0">自动报表与产量分析中心</div>
  <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;margin-top:2px">
    数据实时同步 · 调度指令/故障处理均自动写入
  </div>
</div>""", unsafe_allow_html=True)
st.divider()

task_records   = st.session_state.task_records
charge_records = st.session_state.charge_records

total   = len(task_records)
success = sum(1 for r in task_records if r.get("结果") == "成功")
rate    = f"{success/total*100:.1f}%" if total > 0 else "—"

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_accent("TODAY TASKS", str(total), "含调度新增记录", "blue"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_accent("SUCCESS RATE", rate, f"成功 {success} / 总计 {total}", "green"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_accent("CHARGE RECORDS", str(len(charge_records)), "含返回充电记录", "amber"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_accent("REPORTS GEN.", str(total), "含8项关键参数", "purple"), unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📋 作业溯源记录", "🔋 充电基地记录"])

with tab1:
    col_table, col_chart = st.columns([1.6, 1])
    with col_table:
        st.markdown('<div class="rail-card"><div class="rail-card-title">防溜作业记录（实时写入）</div>', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns([2, 1, 1])
        with fc1:
            search = st.text_input("搜索", placeholder="时间/设备/车次...", label_visibility="collapsed")
        with fc2:
            result_f = st.selectbox("结果", ["全部","成功","失败","执行中"], label_visibility="collapsed")
        with fc3:
            dev_f = st.selectbox("设备", ["全部","A01","A02","A03","A04"], label_visibility="collapsed")

        df = pd.DataFrame(task_records)
        if not df.empty:
            if search:
                mask = df.apply(lambda r: search in " ".join(r.astype(str)), axis=1)
                df = df[mask]
            if result_f != "全部":
                df = df[df["结果"].str.contains(result_f, na=False)]
            if dev_f != "全部":
                df = df[df["设备"] == dev_f]

            def style_result(val):
                if "成功" in str(val):   return "color:#10b981;font-weight:500"
                if "失败" in str(val):   return "color:#ef4444;font-weight:500"
                if "执行中" in str(val): return "color:#3b82f6;font-weight:500"
                return "color:#94a3b8"

            st.dataframe(df.style.applymap(style_result, subset=["结果"]),
                         use_container_width=True, hide_index=True, height=340)

            buf = io.BytesIO()
            df.to_excel(buf, index=False, engine="openpyxl")
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.download_button("⬇ 导出 Excel", data=buf.getvalue(),
                                   file_name="防溜作业记录.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            with col_e2:
                csv = df.to_csv(index=False).encode("utf-8-sig")
                st.download_button("⬇ 导出 CSV", data=csv,
                                   file_name="防溜作业记录.csv",
                                   mime="text/csv", use_container_width=True)
        else:
            st.info("暂无作业记录")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart:
        labels, vals = gen_week_bar()
        colors = ["#2a4480"] * 6 + ["#f59e0b"]
        fig_week = go.Figure(go.Bar(x=labels, y=vals, marker_color=colors, marker_line_width=0))
        fig_week.update_layout(margin=dict(l=0,r=0,t=4,b=0), height=160,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickfont=dict(color="#475569",size=11,family="JetBrains Mono")),
            yaxis=dict(showgrid=False, visible=False), bargap=0.2)
        st.markdown('<div class="rail-card"><div class="rail-card-title">本周作业量趋势</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_week, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        hours, energy = gen_energy_curve()
        fig_e = go.Figure(go.Scatter(x=hours, y=energy, mode="lines+markers",
            line=dict(color="#06b6d4", width=2), marker=dict(color="#06b6d4", size=5),
            fill="tozeroy", fillcolor="rgba(6,182,212,0.08)"))
        fig_e.update_layout(margin=dict(l=0,r=0,t=4,b=0), height=140,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickfont=dict(color="#475569",size=10,family="JetBrains Mono")),
            yaxis=dict(showgrid=False, visible=False))
        st.markdown('<div class="rail-card"><div class="rail-card-title">太阳能补能功率曲线</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_e, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        api_html = '<div class="rail-card"><div class="rail-card-title">数据上传接口</div>'
        for name, val, color in [("MQTT 上行链路","在线","green"),("Restful API","在线","green"),("上层系统同步","实时","green")]:
            api_html += f'<div style="display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid #1e3260;font-size:11px"><span style="width:6px;height:6px;border-radius:50%;background:#10b981;display:inline-block;flex-shrink:0"></span><span style="flex:1;color:#94a3b8">{name}</span>{badge(val, color)}</div>'
        api_html += f'<div style="font-size:10px;color:#475569;margin-top:8px">共 {total} 条记录已同步</div></div>'
        st.markdown(api_html, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="rail-card"><div class="rail-card-title">充电基地作业记录（实时写入）</div>', unsafe_allow_html=True)
    df_c = pd.DataFrame(charge_records)
    if not df_c.empty:
        def style_charge(val):
            if "完成" in str(val):   return "color:#10b981;font-weight:500"
            if "充电中" in str(val): return "color:#3b82f6;font-weight:500"
            return "color:#94a3b8"
        st.dataframe(df_c.style.applymap(style_charge, subset=["状态"]),
                     use_container_width=True, hide_index=True, height=300)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            buf_c = io.BytesIO()
            df_c.to_excel(buf_c, index=False, engine="openpyxl")
            st.download_button("⬇ 导出充电记录 Excel", data=buf_c.getvalue(),
                               file_name="充电基地记录.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        with col_c2:
            csv_c = df_c.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇ 导出充电记录 CSV", data=csv_c,
                               file_name="充电基地记录.csv",
                               mime="text/csv", use_container_width=True)
        charging_now = [r for r in charge_records if r.get("状态") == "充电中"]
        completed    = [r for r in charge_records if r.get("状态") == "完成"]
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown(metric_accent("正在充电", str(len(charging_now)), "台设备补能中", "blue"), unsafe_allow_html=True)
        with col_s2:
            st.markdown(metric_accent("今日完成", str(len(completed)), "次完整充电", "green"), unsafe_allow_html=True)
        with col_s3:
            st.markdown(metric_accent("对接精度", "±18mm", "均在容差范围内", "cyan"), unsafe_allow_html=True)
    else:
        st.info("暂无充电记录，防溜车执行返回充电指令后自动写入")
    st.markdown("</div>", unsafe_allow_html=True)
