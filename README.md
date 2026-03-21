# 防溜车监控系统 · 部署指南

## 项目结构

```
antislip/
├── app.py                  # 主入口
├── style.css               # 全局深色主题
├── requirements.txt        # 依赖
├── utils/
│   ├── theme.py            # 主题工具函数
│   └── mock_data.py        # 模拟数据（后期替换真实接口）
└── pages/
    ├── 1_监控大屏.py
    ├── 2_调度联控.py
    ├── 3_故障报警.py
    ├── 4_报表中心.py
    └── 5_系统设置.py
```

---

## 本地运行步骤

### 第一步：克隆或下载代码

```bash
git clone https://github.com/你的用户名/antislip.git
cd antislip
```

### 第二步：创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 第三步：安装依赖

```bash
pip install -r requirements.txt
```

### 第四步：运行

```bash
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`

---

## 部署到 Streamlit Cloud（免费）

### 第一步：推送到 GitHub

```bash
git init
git add .
git commit -m "init: 防溜车监控系统"
git branch -M main
git remote add origin https://github.com/你的用户名/antislip.git
git push -u origin main
```

### 第二步：在 Streamlit Cloud 部署

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 点击 **New app**
3. 选择你的 GitHub 仓库
4. Main file path 填写：`app.py`
5. 点击 **Deploy**

部署完成后获得公网访问链接，可直接分享给评委。

---

## 接入真实数据（后续扩展）

`utils/mock_data.py` 中的所有函数均为模拟数据，替换为真实接口时只需修改对应函数：

| 函数 | 替换为 |
|------|--------|
| `VEHICLES` | 从串口/MQTT读取防溜车实时状态 |
| `ALARMS` | 从数据库查询报警记录 |
| `gen_records()` | 从数据库查询作业记录 |
| `DIM_STATUS` | 从传感器采集12维度数据 |

### MQTT 接入示例

```python
import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    st.session_state["vehicle_status"] = data

client = mqtt.Client()
client.on_message = on_message
client.connect("your-mqtt-broker", 1883)
client.subscribe("antislip/vehicles/#")
client.loop_start()
```

---

## 常见问题

**Q: 字体加载慢？**
A: style.css 中 Google Fonts 需要网络访问，如内网部署可替换为本地字体文件。

**Q: 图表不显示深色背景？**
A: 确认 plotly 图表设置了 `paper_bgcolor="rgba(0,0,0,0)"` 和 `plot_bgcolor="rgba(0,0,0,0)"`。

**Q: 自动刷新导致页面闪烁？**
A: 在侧边栏关闭"自动刷新"开关，手动点击右上角刷新按钮即可。
