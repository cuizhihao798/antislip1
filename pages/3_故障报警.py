import streamlit as st
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.theme import load_css, badge, alarm_strip, metric_accent
from utils.mock_data import ALARMS, DIM_STATUS
import pandas as pd

st.set_page_config(page_title="故障报警 · 防溜车系统", page_icon="🔔", layout="wide")
load_css()

st.markdown("""
<div style="padding:4px 0 12px">
  <div style="font-size:18px;font-weight:500;color:#e2e8f0">故障自诊断与报警中心</div>
  <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;margin-top:2px">
    12维度实时监控 · 自动定位故障元件 · 处理跟踪
  </div>
</div>""", unsafe_allow_html=True)
st.divider()

# ── 顶部指标 ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_accent("ACTIVE ALARMS", "2", "严重 1 · 预警 1", "red"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_accent("TODAY FAULTS", "3", "已处理 2 · 待处 1", "amber"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_accent("AUTO DETECT RATE", "100%", "12 维度全覆盖", "green"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_accent("RESPONSE TIME", "≤200ms", "紧急停机响应", "cyan"), unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

col_alarm, col_dim = st.columns([1, 1])

# ── 报警列表 ──────────────────────────────────────────────
with col_alarm:
    st.markdown('<div class="rail-card"><div class="rail-card-title">当前报警列表</div>', unsafe_allow_html=True)

    level_filter = st.multiselect(
        "筛选级别", ["严重", "预警", "已解决"],
        default=["严重", "预警", "已解决"], label_visibility="collapsed"
    )

    for a in ALARMS:
        if a["level"] not in level_filter and a["status"] not in ["已解决"] :
            continue
        if a["status"] == "已解决" and "已解决" not in level_filter:
            continue

        st.markdown(alarm_strip(a["title"], a["sub"], a["color"]), unsafe_allow_html=True)

        with st.expander(f"▸ {a['id']} · 处理向导", expanded=False):
            st.markdown(f"""
            <div style="font-size:11px;color:#94a3b8;font-family:'JetBrains Mono',monospace;line-height:1.8">
              <div><span style="color:#475569">故障码：</span><span style="color:#e2e8f0">{a['code']}</span></div>
              <div><span style="color:#475569">建议处理：</span>{a['suggest']}</div>
            </div>""", unsafe_allow_html=True)

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                status_opt = st.selectbox("处理状态", ["待处理","处理中","已解决"],
                                          index=["待处理","处理中","已解决"].index(a["status"]),
                                          key=f"status_{a['id']}")
            with col_s2:
                handler = st.text_input("处理人", value="张工", key=f"handler_{a['id']}")
            if st.button("提交处理记录", key=f"btn_{a['id']}"):
                st.success(f"✓ {a['id']} 处理记录已保存 · 状态：{status_opt}")

    st.markdown("</div>", unsafe_allow_html=True)

# ── 12维度看板 ────────────────────────────────────────────
with col_dim:
    dim_html = '<div class="rail-card"><div class="rail-card-title">12维度监控看板</div>'
    color_map = {"green": "green", "amber": "amber", "red": "red", "blue": "blue"}
    for name, val, color in DIM_STATUS:
        dim_html += f"""
        <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
                    border-bottom:1px solid #1e3260;font-size:11px">
          <span style="flex:1;color:#94a3b8">{name}</span>
          <span style="font-family:'JetBrains Mono',monospace;color:#e2e8f0">{val}</span>
          {badge("正常" if color == "green" else val if color in ["amber","red"] else val, color)}
        </div>"""
    dim_html += "</div>"
    st.markdown(dim_html, unsafe_allow_html=True)

    # 历史报警记录
    st.markdown('<div class="rail-card" style="margin-top:0"><div class="rail-card-title">历史故障记录</div>', unsafe_allow_html=True)
    hist = pd.DataFrame({
        "时间": ["14:02","13:45","09:30","昨 16:22","昨 08:10"],
        "设备": ["A04","A01","A02","A03","A01"],
        "故障码": ["E-214","W-401","W-103","W-202","E-108"],
        "类型": ["旋转电机过载","电量预警","视觉遮挡","充电对位偏差","行程编码异常"],
        "处理结果": ["待处理","已解决","处理中","已解决","已解决"],
    })
    st.dataframe(hist, use_container_width=True, hide_index=True, height=220)
    st.markdown("</div>", unsafe_allow_html=True)
