import streamlit as st
import requests
from datetime import date, datetime

st.set_page_config(page_title="ระบบผู้เชี่ยวชาญฤกษ์ยาม (ปฏิทินฮวงจุ้ย)", page_icon="☯️", layout="centered")

# CSS จัดสไตล์เลย์เอาต์แผ่นปฏิทิน
st.markdown("""
    <style>
    .stButton>button { background-color: #D4AF37; color: white; border-radius: 25px; border: none; font-weight: bold; font-size: 1rem; padding: 10px 24px; transition: all 0.3s; }
    .stButton>button:hover { background-color: #B5952F; box-shadow: 0px 4px 12px rgba(212, 175, 55, 0.4); }
    
    /* กรอบสไตล์หน้าหนังสือปฏิทิน */
    .calendar-paper {
        background-color: #FAFAFA;
        border: 2px solid #2C3E50;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .header-date {
        text-align: right;
        font-size: 1.4rem;
        font-weight: bold;
        color: #2C3E50;
    }
    .header-subtext {
        text-align: right;
        font-size: 0.95rem;
        color: #555;
    }
    .bazi-table {
        width: 100%;
        border-collapse: collapse;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .bazi-table th, .bazi-table td {
        border: 1px solid #BDC3C7;
        padding: 6px;
    }
    .bazi-table th { background-color: #ECF0F1; color: #2C3E50; }
    
    .shaded-box {
        background-color: #2C3E50;
        color: #FFFFFF;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    
    /* ตารางยาม 12 ชั่วยาม */
    .hourly-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
        margin-top: 15px;
    }
    .hourly-table th, .hourly-table td {
        border: 1px solid #D5D8DC;
        padding: 6px 4px;
        text-align: center;
    }
    .hourly-table th { background-color: #34495E; color: white; }
    .star-good { color: #27AE60; font-weight: bold; font-size: 1.1rem; }
    .star-bad { color: #E74C3C; font-weight: bold; font-size: 1.1rem; }
    .star-spec { color: #D4AF37; font-weight: bold; font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2C3E50;'>☯️ ระบบผู้เชี่ยวชาญฤกษ์ยาม (AI ซินแส)</h1>", unsafe_allow_html=True)

# 🌟 เมนูหลัก 3 แท็บ
tab_home, tab_chinese, tab_thai = st.tabs(["📖 ปฏิทินฮวงจุ้ยรายวัน (หน้าแรก)", "☯️ ฤกษ์จีน (ค้นหามหาฤกษ์)", "☸️ ฤกษ์ไทย (สแกนฤกษ์ล่าง)"])

# ==========================================
# TAB 1: ปฏิทินฮวงจุ้ยรายวัน (หน้าแรกสไตล์หนังสือ)
# ==========================================
with tab_home:
    st.markdown("### 🗓️ ป้อนวันเดือนปี เพื่อเปิดแผ่นปฏิทินฮวงจุ้ย")
    selected_date = st.date_input("📅 เลือกวันที่ต้องการดู", date.today(), key="dash_date")
    
    if st.button("🔮 เปิดแผ่นปฏิทินฮวงจุ้ย", use_container_width=True, key="btn_dash"):
        with st.spinner("กำลังคำนวณผังปฏิทินฮวงจุ้ยและกาลเวลา..."):
            try:
                res = requests.post("https://fengshui-platform.onrender.com/daily-dashboard", json={"target_date": str(selected_date)}).json()
                
                # --- แผ่นปฏิทินรายวัน (Paper Layout) ---
                st.markdown("<div class='calendar-paper'>", unsafe_allow_html=True)
                
                # Header วันที่ & รหัสสมพงศ์
                st.markdown(f"<div class='header-date'>{res['thai_date_label']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='header-subtext'>{res['day_element_label']} | {res['kalyok_label']} (ฤกษ์ไทย: {res['thai_reuk']})</div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                c_kua1, c_kua2 = st.columns(2)
                with c_kua1:
                    st.markdown(f"**ดีกับคนรหัส:** `{res['good_kua_people']}`")
                with c_kua2:
                    st.markdown(f"**ดีกับบ้านรหัส:** `{res['good_kua_house']}`")
                
                # ส่วนเนื้อหาแบ่ง 2 คอลัมน์ (ซ้าย: ปาจื่อ/ทิศห้าม | ขวา: เสาชะตา 3 กาล)
                col_left, col_right = st.columns([1.2, 1])
                
                with col_left:
                    st.markdown("#### 🧭 ทิศทางและพลังงานประจำวัน")
                    st.write(f"• **ดาวจรศูนย์กลาง:** ปี {res['stars']['year']} | เดือน {res['stars']['month']} | วัน {res['stars']['day']}")
                    
                    # ทิศห้ามกระทบ/แรเงา
                    shaded_text = ", ".join(res['shaded_palaces']) if res['shaded_palaces'] else "ไม่มี"
                    st.markdown(f"<div class='shaded-box'>พื้นที่แรเงาเข้ม (ทิศอสูร/ไท้ส่วย/5เหลือง):<br>{shaded_text}<br><small style='font-weight:normal;'>ห้าม รบกวน เคาะ ตอก เจาะ ขุด</small></div>", unsafe_allow_html=True)

                with col_right:
                    st.markdown("#### 📜 เสาชะตาปาจื่อ (3 กาล)")
                    bazi = res['bazi_3_pillars']
                    bazi_html = f"""
                    <table class='bazi-table'>
                        <tr><th>วัน</th><th>เดือน</th><th>ปี</th></tr>
                        <tr>
                            <td><b>{bazi['day']['cn']}</b></td>
                            <td><b>{bazi['month']['cn']}</b></td>
                            <td><b>{bazi['year']['cn']}</b></td>
                        </tr>
                        <tr>
                            <td>{bazi['day']['element']}<br>{bazi['day']['zodiac']}</td>
                            <td>{bazi['month']['element']}<br>{bazi['month']['zodiac']}</td>
                            <td>{bazi['year']['element']}<br>{bazi['year']['zodiac']}</td>
                        </tr>
                    </table>
                    """
                    st.markdown(bazi_html, unsafe_allow_html=True)
                    if res['clash_zodiac']:
                        st.markdown(f"<div style='color:red; text-align:center; font-weight:bold;'>⚠️ วัน{bazi['day']['zodiac']} ชงกับ {res['clash_zodiac']}</div>", unsafe_allow_html=True)

                # --- ตาราง 12 ชั่วยาม (ยามดี-ร้าย & ทิศปลอดภัย) ---
                st.markdown("<br>#### ⏰ ตารางยามดี-ร้าย และ 12 ราศีที่ปลอดภัยประจำยาม", unsafe_allow_html=True)
                
                table_rows = ""
                for h in res['hourly_table']:
                    q_symbol = f"<span class='star-spec'>{h['quality']}</span>" if h['quality'] == "⭐" else f"<span class='star-good'>{h['quality']}</span>" if h['quality'] == "O" else f"<span class='star-bad'>{h['quality']}</span>"
                    safe_z_str = ", ".join(h['safe_zodiacs'][:6]) + "..."
                    
                    table_rows += f"""
                    <tr>
                        <td><b>ดาว {h['star']}</b></td>
                        <td><b>{h['pillar_cn']}</b></td>
                        <td>{h['element']}</td>
                        <td>{q_symbol}</td>
                        <td>{h['time']}</td>
                        <td style='text-align:left;'>{safe_z_str}</td>
                    </tr>
                    """
                
                full_table_html = f"""
                <table class='hourly-table'>
                    <thead>
                        <tr>
                            <th style='width: 10%;'>ดาว</th>
                            <th style='width: 12%;'>ยาม</th>
                            <th style='width: 18%;'>ธาตุ/นักษัตร</th>
                            <th style='width: 12%;'>ฤกษ์</th>
                            <th style='width: 20%;'>ช่วงเวลา</th>
                            <th>ราศีปลอดภัยประจำยาม</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                """
                st.markdown(full_table_html, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True) # ปิดแผ่นปฏิทิน
                
            except Exception as e:
                st.error("🔌 ไม่สามารถเชื่อมต่อกับ Backend ได้ กรุณาตรวจสอบการรันเซิร์ฟเวอร์")

# ==========================================
# TAB 2: ฤกษ์จีน (ค้นหามหาฤกษ์ - แท็บเดิม)
# ==========================================
with tab_chinese:
    with st.form("chinese_form"):
        st.markdown("### 📋 คำนวณฤกษ์จีน (ค้นหามหาฤกษ์รายวัน)")
        col1, col2 = st.columns(2)
        with col1:
            zodiac_c = st.selectbox("ปีเกิดนักษัตรของคุณ", ["ชวด", "ฉลู", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะเมีย", "มะแม", "วอก", "ระกา", "จอ", "กุน"])
            fav_elements = st.multiselect("ธาตุส่งเสริม", ["ไม้", "ไฟ", "ดิน", "ทอง", "น้ำ"], default=["ทอง", "น้ำ"])
        with col2:
            start_date_c = st.date_input("วันที่เริ่มค้นหาฤกษ์", date.today(), key="c_date")
            house_degree = st.number_input("องศาหน้าบ้าน (0-359)", min_value=0, max_value=359, value=0)
            days_c = st.slider("จำนวนวันที่สแกน", 1, 30, 7, key="c_slider")
        submit_chinese = st.form_submit_button("🔮 คำนวณฤกษ์จีน", use_container_width=True)

    if submit_chinese:
        payload = {"birth_year_zodiac": zodiac_c, "favorable_elements": fav_elements, "house_degree": int(house_degree), "start_date": str(start_date_c), "days_to_scan": int(days_c)}
        try:
            res_c = requests.post("https://fengshui-platform.onrender.com/analyze-dates", json=payload).json())
            st.subheader("📊 ปฏิทินฤกษ์มงคลจีน")
            
            weekdays = ["จันทร์", "อังคาร", "พุธ", "พฤหัส", "ศุกร์", "เสาร์", "อาทิตย์"]
            head_cols = st.columns(7)
            for i, d_name in enumerate(weekdays):
                head_cols[i].markdown(f"<div style='text-align: center; color: #7F8C8D; font-size: 0.85rem;'>{d_name}</div>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

            if len(res_c["data"]) > 0:
                start_wd = datetime.strptime(res_c["data"][0]["date"], "%Y-%m-%d").weekday()
                cols = st.columns(7)
                curr_col = 0
                for _ in range(start_wd):
                    cols[curr_col].empty()
                    curr_col += 1

                for day in res_c["data"]:
                    if curr_col > 6:
                        cols = st.columns(7)
                        curr_col = 0

                    bg = "#e8f5e9" if day["status"] == "Green Zone" else "#ffebee" if day["status"] == "Red Zone" else "#fff8e1"
                    bd = "#4caf50" if day["status"] == "Green Zone" else "#f44336" if day["status"] == "Red Zone" else "#ffc107"
                    d_num = day["date"].split("-")[2]
                    zod_name = day["zodiac"].replace("วัน", "").strip()

                    cols[curr_col].markdown(f"<div style='background-color:{bg}; border:2px solid {bd}; border-radius:8px; text-align:center; padding:5px; margin-bottom:8px;'><h3 style='margin:0; color:{bd};'>{d_num}</h3><small>{zod_name}</small></div>", unsafe_allow_html=True)
                    curr_col += 1
                
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 📱 รายละเอียดรายวัน")
                for day in res_c["data"]:
                    icon = "✅" if day["status"] == "Green Zone" else "❌" if day["status"] == "Red Zone" else "⚠️"
                    with st.expander(f"{icon} {day['date']} ({day['zodiac']})"):
                        st.markdown(f"**เหตุผล:** {day['reason']}")
                        if day.get("recommended_hours") and day["status"] == "Green Zone":
                            st.markdown(f"⏰ **เวลามงคล:** {' / '.join(day['recommended_hours'])}")
        except Exception as e:
            st.error("ไม่สามารถเชื่อมต่อกับ Backend ได้")

# ==========================================
# TAB 3: ฤกษ์ไทย (สแกนฤกษ์ล่าง - แท็บเดิม)
# ==========================================
with tab_thai:
    with st.form("thai_form"):
        st.markdown("### 📋 คำนวณฤกษ์ไทย (กาลโยค & ฤกษ์ล่าง)")
        col1, col2 = st.columns(2)
        with col1:
            activity = st.selectbox("กิจกรรมที่ต้องการทำ", ["ขึ้นบ้านใหม่/ลงเสาเอก", "เปิดร้านค้า/ธุรกิจ", "แต่งงาน/สู่ขอ", "เปิดสถานบันเทิง/โรงแรม", "เจรจา/ทวงหนี้/ขออนุมัติ", "ทำบุญ/งานมงคลทั่วไป"])
        with col2:
            start_date_t = st.date_input("วันที่เริ่มค้นหาฤกษ์", date.today(), key="t_date")
            days_t = st.slider("จำนวนวันที่สแกน", 1, 30, 7, key="t_slider")
        submit_thai = st.form_submit_button("☸️ คำนวณฤกษ์ไทย", use_container_width=True)

    if submit_thai:
        payload_thai = {"activity_type": activity, "start_date": str(start_date_t), "days_to_scan": int(days_t)}
        try:
            res_t = requests.post("https://fengshui-platform.onrender.com/analyze-thai-dates", json=payload_thai).json()
            st.subheader("📊 รายงานผลฤกษ์ไทย")
            for day in res_t["data"]:
                icon = "✅" if day["status"] == "Green Zone" else "❌" if day["status"] == "Red Zone" else "⚠️"
                bd = "#4caf50" if day["status"] == "Green Zone" else "#f44336" if day["status"] == "Red Zone" else "#ffc107"
                st.markdown(f"<div style='background-color:#f9f9f9; padding:12px; border-radius:8px; margin-bottom:8px; border-left: 5px solid {bd};'><b>{icon} วัน{day['weekday']}ที่ {day['date']}</b> | ฤกษ์: <u>{day['thai_reuk']}</u> ({day['kalyok']})<br><small>{day['reason']}</small></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("ไม่สามารถเชื่อมต่อกับ Backend ได้")
