import streamlit as st
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.theme import load_css, badge

st.set_page_config(page_title="系统设置 · 防溜车系统", page_icon="⚙️", layout="wide")
load_css()

st.markdown("""
<div style="padding:4px 0 12px">
  <div style="font-size:18px;font-weight:500;color:#e2e8f0">系统管理后台</div>
  <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;margin-top:2px">
    权限管理 · 阈值配置 · 设备档案
  </div>
</div>""", unsafe_allow_html=True)
st.divider()

tab1, tab2, tab3 = st.tabs(["🔑 权限管理", "⚙️ 阈值配置", "📋 设备档案"])

# ── 权限管理 ──────────────────────────────────────────────
with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="rail-card"><div class="rail-card-title">角色权限矩阵</div>', unsafe_allow_html=True)
        perm_html = """
        <table style="width:100%;border-collapse:collapse;font-size:12px">
          <thead>
            <tr style="border-bottom:1px solid #1e3260">
              <th style="text-align:left;padding:8px;color:#475569;font-family:'JetBrains Mono',monospace;font-weight:500">角色</th>
              <th style="padding:8px;color:#475569;font-family:'JetBrains Mono',monospace;font-weight:500">调度指令</th>
              <th style="padding:8px;color:#475569;font-family:'JetBrains Mono',monospace;font-weight:500">报表导出</th>
              <th style="padding:8px;color:#475569;font-family:'JetBrains Mono',monospace;font-weight:500">参数配置</th>
              <th style="padding:8px;color:#475569;font-family:'JetBrains Mono',monospace;font-weight:500">用户管理</th>
            </tr>
          </thead>
          <tbody>"""
        roles = [
            ("管理员", True, True, True, True),
            ("调度员", True, True, False, False),
            ("查看者", False, True, False, False),
        ]
        for role, *perms in roles:
            perm_html += f'<tr style="border-bottom:1px solid #1e3260"><td style="padding:8px;color:#e2e8f0">{role}</td>'
            for p in perms:
                icon = '<span style="color:#10b981">✓</span>' if p else '<span style="color:#475569">—</span>'
                perm_html += f'<td style="padding:8px;text-align:center">{icon}</td>'
            perm_html += "</tr>"
        perm_html += "</tbody></table></div>"
        st.markdown(perm_html, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="rail-card"><div class="rail-card-title">用户管理</div>', unsafe_allow_html=True)
        with st.form("add_user"):
            u_name  = st.text_input("用户名")
            u_role  = st.selectbox("角色", ["管理员", "调度员", "查看者"])
            u_pwd   = st.text_input("初始密码", type="password")
            if st.form_submit_button("添加用户", use_container_width=True):
                st.success(f"✓ 用户 {u_name}（{u_role}）已创建")
        st.markdown("</div>", unsafe_allow_html=True)

# ── 阈值配置 ──────────────────────────────────────────────
with tab2:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="rail-card"><div class="rail-card-title">安全阈值配置</div>', unsafe_allow_html=True)
        with st.form("threshold_form"):
            low_batt   = st.slider("低电量预警阈值 (%)",    10, 50, 20)
            resp_time  = st.slider("紧急停机响应上限 (ms)", 100, 500, 200)
            conf_min   = st.slider("视觉置信度下限 (%)",    80, 99, 90)
            dock_tol   = st.slider("自动补能对接容差 (mm)", 5, 50, 20)
            temp_max   = st.slider("设备温度上限 (°C)",     40, 80, 55)
            if st.form_submit_button("保存配置", use_container_width=True):
                st.success("✓ 阈值配置已保存")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="rail-card"><div class="rail-card-title">当前生效阈值</div>', unsafe_allow_html=True)
        params = [
            ("低电量预警阈值",     "20%",    "amber"),
            ("紧急停机响应上限",   "200ms",  "blue"),
            ("视觉置信度下限",     "90%",    "green"),
            ("自动补能对接容差",   "±20mm",  "green"),
            ("环境温度上限",       "55°C",   "amber"),
            ("系统开机率目标",     "≥99.9%", "green"),
            ("防护等级要求",       "IP65",   "green"),
        ]
        rows = ""
        for name, val, color in params:
            rows += f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:8px 0;border-bottom:1px solid #1e3260;font-size:12px">
              <span style="color:#94a3b8">{name}</span>
              <span style="font-family:'JetBrains Mono',monospace;color:#e2e8f0">{val}</span>
            </div>"""
        st.markdown(rows + "</div>", unsafe_allow_html=True)

# ── 设备档案 ──────────────────────────────────────────────
with tab3:
    dev_sel = st.selectbox("选择设备", ["A01", "A02", "A03", "A04"])
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown('<div class="rail-card"><div class="rail-card-title">设备基本信息</div>', unsafe_allow_html=True)
        info = [
            ("设备编号", dev_sel), ("型号", "ARV-2000"),
            ("投运日期", "2026-01-15"), ("累计作业次数", "1,284"),
            ("总运行时长", "2,156 h"), ("上次维保", "2026-03-01"),
            ("下次维保", "2026-06-01"), ("防护等级", "IP65"),
        ]
        for k, v in info:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:7px 0;
                        border-bottom:1px solid #1e3260;font-size:12px">
              <span style="color:#475569">{k}</span>
              <span style="color:#e2e8f0;font-family:'JetBrains Mono',monospace">{v}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_d2:
        st.markdown('<div class="rail-card"><div class="rail-card-title">维保记录</div>', unsafe_allow_html=True)
        import pandas as pd
        maint = pd.DataFrame({
            "日期": ["2026-03-01","2026-01-20","2025-12-05"],
            "类型": ["定期维保","镜头清洁","机械臂润滑"],
            "执行人": ["张工","李工","张工"],
            "结果": ["正常","正常","正常"],
        })
        st.dataframe(maint, use_container_width=True, hide_index=True, height=160)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="rail-card"><div class="rail-card-title">维护提醒</div>', unsafe_allow_html=True)
        reminders = [
            ("镜头清洁",     "下次：2026-04-01", "amber"),
            ("机械臂润滑",   "下次：2026-06-01", "green"),
            ("电池检测",     "下次：2026-05-15", "green"),
        ]
        for name, due, color in reminders:
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:7px 0;border-bottom:1px solid #1e3260;font-size:12px">
              <span style="color:#94a3b8">{name}</span>
              <span style="font-family:'JetBrains Mono',monospace;color:#475569;font-size:11px">{due}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
