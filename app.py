import streamlit as st
import pathlib

st.set_page_config(
    page_title="防溜车监控系统",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
)

css = (pathlib.Path(__file__).parent / "style.css").read_text(encoding='utf-8')
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="padding:20px 16px 18px;border-bottom:1px solid #1e3260;margin-bottom:8px">
  <div style="font-size:14px;font-weight:700;color:#e2e8f0;letter-spacing:.05em">防溜车监控系统</div>
  <div style="font-size:10px;color:#475569;margin-top:4px;font-family:'JetBrains Mono',monospace;letter-spacing:.08em">RAIL ANTI-SLIP · v2.0</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:80px 0 40px">
  <div style="font-size:32px;font-weight:700;color:#e2e8f0;margin-bottom:12px">🚂 防溜车监控系统</div>
  <div style="font-size:14px;color:#475569;font-family:'JetBrains Mono',monospace">请点击左侧导航栏选择功能模块</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div style="background:#0f1729;border:1px solid #1e3260;border-radius:8px;padding:20px;text-align:center">
      <div style="font-size:28px">📡</div>
      <div style="color:#e2e8f0;font-weight:500;margin-top:8px">监控大屏</div>
      <div style="color:#475569;font-size:12px;margin-top:4px">实时场站拓扑与设备状态</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div style="background:#0f1729;border:1px solid #1e3260;border-radius:8px;padding:20px;text-align:center">
      <div style="font-size:28px">🎮</div>
      <div style="color:#e2e8f0;font-weight:500;margin-top:8px">调度联控</div>
      <div style="color:#475569;font-size:12px;margin-top:4px">指令下发与逻辑互锁</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div style="background:#0f1729;border:1px solid #1e3260;border-radius:8px;padding:20px;text-align:center">
      <div style="font-size:28px">📊</div>
      <div style="color:#e2e8f0;font-weight:500;margin-top:8px">报表中心</div>
      <div style="color:#475569;font-size:12px;margin-top:4px">溯源记录与数据分析</div>
    </div>""", unsafe_allow_html=True)
