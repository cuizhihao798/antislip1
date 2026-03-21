import streamlit as st
import pathlib

def load_css():
    css_path = pathlib.Path(__file__).parent.parent / "style.css"
    with open(css_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def badge(text, color="gray"):
    return f'<span class="badge badge-{color}">{text}</span>'

def alarm_strip(title, sub, level="red"):
    return f"""
    <div class="alarm-strip alarm-{level}">
      <div>
        <div class="alarm-title">{title}</div>
        <div class="alarm-sub">{sub}</div>
      </div>
    </div>"""

def lock_row(text, status):
    if status == "ok":
        icon_class, icon, badge_html = "l-ok", "✓", badge("通过", "green")
    elif status == "warn":
        icon_class, icon, badge_html = "l-warn", "!", badge("等待中", "amber")
    else:
        icon_class, icon, badge_html = "l-err", "✗", badge("未通过", "red")
    return f"""
    <div class="lock-row">
      <div class="lock-icon {icon_class}">{icon}</div>
      <span style="flex:1">{text}</span>
      {badge_html}
    </div>"""

def flow_steps(steps, active_idx):
    html = '<div class="flow-wrap">'
    for i, s in enumerate(steps):
        if i < active_idx:
            cls = "done"
        elif i == active_idx:
            cls = "active"
        else:
            cls = ""
        html += f'<span class="fstep {cls}">{s}</span>'
        if i < len(steps) - 1:
            html += '<span class="farrow">›</span>'
    html += '</div>'
    return html

def metric_accent(label, value, hint, color):
    color_map = {
        "blue":   "#3b82f6",
        "green":  "#10b981",
        "amber":  "#f59e0b",
        "red":    "#ef4444",
        "cyan":   "#06b6d4",
        "purple": "#8b5cf6",
    }
    c = color_map.get(color, "#e2e8f0")
    return f"""
    <div style="background:#0f1729;border:1px solid #1e3260;border-radius:8px;
                padding:14px 16px;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;right:0;width:40%;height:2px;
                  background:linear-gradient(90deg,transparent,{c})"></div>
      <div style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;
                  letter-spacing:.05em;margin-bottom:8px;">{label}</div>
      <div style="font-size:26px;font-weight:700;font-family:'JetBrains Mono',monospace;
                  color:{c};line-height:1;">{value}</div>
      <div style="font-size:10px;color:#475569;margin-top:6px;">{hint}</div>
    </div>"""
