import streamlit as st
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.theme import load_css, badge, lock_row
from utils.state import init_state, dispatch_command
import pandas as pd

st.set_page_config(page_title="调度联控 · 防溜车系统", page_icon="🎮", layout="wide")
load_css()
init_state()

st.markdown("""
<div style="padding:4px 0 12px">
  <div style="font-size:18px;font-weight:500;color:#e2e8f0">智能调度联控中心</div>
  <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;margin-top:2px">
    调度中心权限最高 · 指令实时同步至监控大屏与报表中心
  </div>
</div>""", unsafe_allow_html=True)
st.divider()

vehicles  = st.session_state.vehicles
interlock = st.session_state.interlock
cmd_log   = st.session_state.cmd_log

col_cmd, col_lock = st.columns(2)

with col_cmd:
    st.markdown('<div class="rail-card"><div class="rail-card-title">指令下发</div>', unsafe_allow_html=True)

    vehicle_options = [f"{v['id']} · {v['track']} · {v['train']} · {badge(v['status'], v['color'])}" for v in vehicles]
    target_idx = st.selectbox("目标设备", range(len(vehicle_options)),
                               format_func=lambda i: f"{vehicles[i]['id']} · {vehicles[i]['track']} · {vehicles[i]['status']}",
                               label_visibility="collapsed")
    target_veh = vehicles[target_idx]

    st.markdown(f"""
    <div style="padding:8px 12px;background:#141f38;border-radius:6px;margin-bottom:12px;font-size:11px;font-family:'JetBrains Mono',monospace;color:#94a3b8">
      选中：<span style="color:#e2e8f0">{target_veh['id']}</span>
      &nbsp;|&nbsp; 电量：<span style="color:#e2e8f0">{target_veh['battery']}%</span>
      &nbsp;|&nbsp; 当前任务：<span style="color:#e2e8f0">{target_veh['task']}</span>
      &nbsp;|&nbsp; 故障：<span style="color:{'#ef4444' if target_veh['fault'] else '#10b981'}">{target_veh['fault'] or '无'}</span>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔵 放铁鞋", use_container_width=True):
            ok, msg = dispatch_command(target_veh["id"], "放铁鞋")
            st.success(msg) if ok else st.error(f"⚠ 互锁拒绝：{msg}")
            st.rerun()
        if st.button("⬜ 节能待机", use_container_width=True):
            ok, msg = dispatch_command(target_veh["id"], "节能待机")
            st.info(msg) if ok else st.error(msg)
            st.rerun()
    with c2:
        if st.button("🔵 取铁鞋", use_container_width=True):
            ok, msg = dispatch_command(target_veh["id"], "取铁鞋")
            st.success(msg) if ok else st.error(f"⚠ 互锁拒绝：{msg}")
            st.rerun()
        if st.button("⬜ 返回充电", use_container_width=True):
            ok, msg = dispatch_command(target_veh["id"], "返回充电")
            st.info(msg) if ok else st.error(msg)
            st.rerun()
    with c3:
        if st.button("🔴 紧急停机", use_container_width=True, type="primary"):
            ok, msg = dispatch_command("ALL", "紧急停机")
            st.error(f"⚠ {msg}")
            st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="rail-card-title">近期指令记录（实时）</div>', unsafe_allow_html=True)

    def style_status(val):
        if "完成" in str(val):   return "color:#10b981;font-family:'JetBrains Mono',monospace"
        if "执行中" in str(val): return "color:#3b82f6;font-family:'JetBrains Mono',monospace"
        if "失败" in str(val):   return "color:#ef4444;font-family:'JetBrains Mono',monospace"
        return "color:#94a3b8;font-family:'JetBrains Mono',monospace"

    df_log = pd.DataFrame(cmd_log[:10])
    st.dataframe(df_log.style.applymap(style_status, subset=["status"]),
                 use_container_width=True, hide_index=True, height=220)
    st.markdown("</div>", unsafe_allow_html=True)

with col_lock:
    il = interlock
    ld = [
        ("列车已完全停稳",   "ok"   if il["train_stopped"]    else "err"),
        ("防溜车已到位",     "ok"   if il["vehicle_arrived"]  else "err"),
        ("视觉定位已锁定",   "ok"   if il["vision_locked"]    else "err"),
        ("发车前已撤回限界", "warn" if not il["vehicle_returned"] else "ok"),
        ("设备无故障",       "ok"   if il["no_fault"]         else "err"),
    ]
    lock_html = '<div class="rail-card"><div class="rail-card-title">全过程逻辑互锁（实时）</div>'
    lock_html += '<div style="font-size:10px;color:#475569;font-family:\'JetBrains Mono\',monospace;margin-bottom:10px">所有项通过方可下发作业指令</div>'
    for text, status in ld:
        lock_html += lock_row(text, status)
    all_ok = all(s == "ok" for _, s in ld)
    if not all_ok:
        faults = [v for v in vehicles if v["fault"]]
        fault_msg = "、".join([f"{v['id']}({v['fault']})" for v in faults]) if faults else "请检查互锁状态"
        lock_html += f"""
        <div style="margin-top:12px;padding:10px 14px;background:rgba(239,68,68,.06);
                    border:1px solid rgba(239,68,68,.2);border-radius:5px;
                    font-size:10px;color:#ef4444;font-family:'JetBrains Mono',monospace;line-height:1.8">
          ⚠ 当前存在未通过项<br>故障设备：{fault_msg}<br>请在故障报警页处理后解锁
        </div>"""
    else:
        lock_html += '<div style="margin-top:12px;padding:10px 14px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.2);border-radius:5px;font-size:10px;color:#10b981;font-family:\'JetBrains Mono\',monospace">✓ 全部通过，所有指令可正常下发</div>'
    lock_html += "</div>"
    st.markdown(lock_html, unsafe_allow_html=True)

    st.markdown('<div class="rail-card" style="margin-top:0"><div class="rail-card-title">当前设备任务状态</div>', unsafe_allow_html=True)
    task_data = {
        "设备":     [v["id"]     for v in vehicles],
        "当前任务": [v["task"]   for v in vehicles],
        "电量":     [f"{v['battery']}%" for v in vehicles],
        "状态":     [v["status"] for v in vehicles],
        "故障码":   [v["fault"] or "—" for v in vehicles],
    }
    st.dataframe(pd.DataFrame(task_data), use_container_width=True, hide_index=True, height=200)
    st.markdown("</div>", unsafe_allow_html=True)
