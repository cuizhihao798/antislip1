import streamlit as st
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.theme import load_css, badge, lock_row
from utils.mock_data import INTERLOCK
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="调度联控 · 防溜车系统", page_icon="🎮", layout="wide")
load_css()

st.markdown("""
<div style="padding:4px 0 12px">
  <div style="font-size:18px;font-weight:500;color:#e2e8f0">智能调度联控中心</div>
  <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;margin-top:2px">
    指令管理 · 逻辑互锁 · 任务分配
  </div>
</div>""", unsafe_allow_html=True)
st.divider()

col_cmd, col_lock = st.columns(2)

# ── 指令下发 ──────────────────────────────────────────────
with col_cmd:
    st.markdown('<div class="rail-card"><div class="rail-card-title">指令下发</div>', unsafe_allow_html=True)

    target = st.selectbox("目标设备", ["A01 · 1股道 · G105", "A02 · 2股道 · G182", "A03 · 充电基地"])

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔵 放铁鞋", use_container_width=True):
            st.success(f"✓ 指令已下发：{target} → 放铁鞋")
        if st.button("⬜ 节能待机", use_container_width=True):
            st.info(f"✓ 指令已下发：{target} → 节能待机")
    with c2:
        if st.button("🔵 取铁鞋", use_container_width=True):
            st.success(f"✓ 指令已下发：{target} → 取铁鞋")
        if st.button("⬜ 返回充电", use_container_width=True):
            st.info(f"✓ 指令已下发：{target} → 返回充电")
    with c3:
        if st.button("🔴 紧急停机", use_container_width=True, type="primary"):
            st.error(f"⚠ 紧急停机：{target}")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("**近期指令记录**")

    log_data = {
        "时间": ["14:30:12","14:28:05","14:15:44","14:02:11"],
        "设备": ["A02","A01","A03","A04"],
        "指令": ["放铁鞋 · 2股道前轮","放铁鞋 · 1股道后轮","返回充电","放铁鞋 · 4股道前轮"],
        "状态": ["执行中","完成","完成","失败 E-214"],
    }
    df_log = pd.DataFrame(log_data)

    def style_status(val):
        if "完成" in val:    return "color:#10b981;font-family:'JetBrains Mono',monospace"
        if "执行中" in val:  return "color:#3b82f6;font-family:'JetBrains Mono',monospace"
        if "失败" in val:    return "color:#ef4444;font-family:'JetBrains Mono',monospace"
        return "color:#94a3b8;font-family:'JetBrains Mono',monospace"

  st.dataframe(df_log.style.map(style_status, subset=["status"]),
        use_container_width=True, hide_index=True, height=180,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ── 逻辑互锁 ──────────────────────────────────────────────
with col_lock:
    lock_html = '<div class="rail-card"><div class="rail-card-title">全过程逻辑互锁状态</div>'
    lock_html += '<div style="font-size:10px;color:#475569;font-family:\'JetBrains Mono\',monospace;margin-bottom:10px">所有项通过方可下发作业指令</div>'
    for text, status in INTERLOCK:
        lock_html += lock_row(text, status)
    lock_html += """
    <div style="margin-top:12px;padding:10px 14px;background:rgba(239,68,68,.06);
                border:1px solid rgba(239,68,68,.2);border-radius:5px;
                font-size:10px;color:#ef4444;font-family:'JetBrains Mono',monospace;line-height:1.8">
      ⚠ 当前禁止 A04 下发任何指令<br>
      原因：旋转电机过载（故障码 E-214）<br>
      请先排除故障后重新解锁
    </div></div>"""
    st.markdown(lock_html, unsafe_allow_html=True)

    # 多任务分配状态
    st.markdown('<div class="rail-card" style="margin-top:0"><div class="rail-card-title">智能任务分配状态</div>', unsafe_allow_html=True)
    task_data = {
        "设备": ["A01","A02","A03","A04"],
        "当前任务": ["放鞋·1股道·G105后轮","放鞋·2股道·G182前轮","自动充电对位","故障停机"],
        "电量": ["78%","55%","32%","61%"],
        "预计完成": ["14:35","14:40","15:10","—"],
    }
    st.dataframe(pd.DataFrame(task_data), use_container_width=True, hide_index=True, height=180)
    st.markdown("</div>", unsafe_allow_html=True)
