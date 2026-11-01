import streamlit as st
import requests
from datetime import date, datetime

st.set_page_config(page_title="ระบบผู้เชี่ยวชาญฤกษ์ยาม (ปฏิทินฮวงจุ้ย)", page_icon="☯️", layout="centered")

# --- CSS จัดสไตล์เลย์เอาต์แผ่นปฏิทินและตาราง ---
st.markdown("""
    <style>
    .stButton>button { background-color: #D4AF37; color: white; border-radius: 25px; border: none; font-weight: bold; font-size: 1rem; padding: 10px 24px; transition: all 0.3s; }
    .stButton>button:hover { background-color: #B5952F; box-shadow: 0px 4px 12px rgba(212, 175, 55, 0.4); }
    
    .calendar-paper { background-color: #FAFAFA; border: 2px solid #2C3E50; border-radius: 12px; padding: 20px; box-shadow: 0px 5px 15px rgba(0,0,0,0.08); margin-bottom: 20px; }
    .header-date { text-align: right; font-size: 1.4rem; font-weight: bold; color: #2C3E50; }
    .header-subtext { text-align: right; font-size: 0.95rem; color: #555; }
    
    .bazi-table { width: 100%; border-collapse: collapse; text-align: center; margin-top: 10px; margin-bottom: 15px; }
    .bazi-table th, .bazi-table td { border: 1px solid #BDC3C7; padding: 6px; }
    .bazi-table th { background-color: #ECF0F1; color: #2C3E50; }
    
    .shaded-box { background-color: #2C3E50; color: #FFFFFF; padding: 8px 12px; border-radius: 6px; font-weight: bold; text-align: center; margin-top: 10px; }
    
    .hourly-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; margin-top: 15px; }
    .hourly-table th, .hourly-table td { border: 1px solid #D5D8DC; padding: 6px 4px; text-align: center; }
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
                
                st.markdown("<div class='calendar-paper'>", unsafe_allow_html=True)
                
                st.markdown(f"<div class='header-date'>{res['thai_date_label']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='header-subtext'>{res['day_element_label']} | {res['kalyok_label']} (ฤกษ์ไทย: {res['thai_reuk']})</div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                c_kua1, c_kua2 = st.columns(2)
                with c_kua1:
                    st.markdown(f"**ดีกับคนรหัส:** `{res['good_kua_people']}`")
                with c_kua2:
                    st.markdown(f"**ดีกับบ้านรหัส:** `{res['good_kua_house']}`")
                
                col_left, col_right = st.columns([1.2, 1])
                
                with col_left:
                    st.markdown("<h4 style='text-align:center; color:#2C3E50;'>🧭 ทิศทางและพลังงานประจำวัน</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center; font-size:0.9rem; margin-bottom:10px;'>ดาวจรศูนย์กลาง: ปี <b>{res['stars']['year']}</b> | เดือน <b>{res['stars']['month']}</b> | วัน <b>{res['stars']['day']}</b></div>", unsafe_allow_html=True)
                    
                    compass_css = "<style>.compass-container { width: 100%; max-width: 280px; margin: 0 auto; padding: 15px; background-color: #FAFAFA; border: 3px solid #2C3E50; border-radius: 50%; aspect-ratio: 1 / 1; display: flex; align-items: center; justify-content: center; box-shadow: inset 0px 0px 15px rgba(0,0,0,0.05), 0px 5px 15px rgba(0,0,0,0.1); } .compass-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 1fr 1fr 1fr; width: 100%; height: 100%; gap: 4px; } .c-cell { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; border-radius: 50%; border: 1px solid #E5E7E9; font-size: 0.95rem; font-weight: bold; color: #2C3E50; background-color: #ffffff; } .c-center { border: 2px solid #D4AF37; background-color: #FEF9E7; } .c-shaded { background-color: #34495E !important; color: #ffffff !important; border: none; } .c-label { font-size: 0.65rem; font-weight: normal; margin-top: 2px; } .c-shaded .c-label { color: #BDC3C7; }</style>"
                    
                    def check_shade(code):
                        return "c-shaded" if any(f"({code})" in s for s in res['shaded_palaces']) else ""
                    
                    html_compass = f"{compass_css}<div class='compass-container'><div class='compass-grid'><div class='c-cell {check_shade('SE')}'>SE<br><span class='c-label'>เฉียงใต้</span></div><div class='c-cell {check_shade('S')}'>S<br><span class='c-label'>ใต้</span></div><div class='c-cell {check_shade('SW')}'>SW<br><span class='c-label'>เฉียงใต้</span></div><div class='c-cell {check_shade('E')}'>E<br><span class='c-label'>ตะวันออก</span></div><div class='c-cell c-center {check_shade('Center')}'>C<br><span class='c-label'>กลาง</span></div><div class='c-cell {check_shade('W')}'>W<br><span class='c-label'>ตะวันตก</span></div><div class='c-cell {check_shade('NE')}'>NE<br><span class='c-label'>เฉียงเหนือ</span></div><div class='c-cell {check_shade('N')}'>N<br><span class='c-label'>เหนือ</span></div><div class='c-cell {check_shade('NW')}'>NW<br><span class='c-label'>เฉียงเหนือ</span></div></div></div><div style='text-align:center; margin-top:15px; font-size:0.85rem; color:#E74C3C;'><b>⚠️ พื้นที่วงกลมสีเข้ม คือ ห้าม รบกวน เคาะ ตอก เจาะ ขุด</b></div>"
                    st.markdown(html_compass, unsafe_allow_html=True)

                with col_right:
                    st.markdown("<h4 style='color:#2C3E50;'>📜 เสาชะตาปาจื่อ (3 กาล)</h4>", unsafe_allow_html=True)
                    bazi = res['bazi_3_pillars']
                    
                    bazi_html = f"<table class='bazi-table'><tr><th style='width:33%;'>วัน</th><th style='width:33%;'>เดือน</th><th style='width:33%;'>ปี</th></tr><tr><td style='font-size:1.2rem;'><b>{bazi['day']['cn']}</b></td><td style='font-size:1.2rem;'><b>{bazi['month']['cn']}</b></td><td style='font-size:1.2rem;'><b>{bazi['year']['cn']}</b></td></tr><tr><td>{bazi['day']['element']}<br>{bazi['day']['zodiac']}</td><td>{bazi['month']['element']}<br>{bazi['month']['zodiac']}</td><td>{bazi['year']['element']}<br>{bazi['year']['zodiac']}</td></tr></table>"
                    st.markdown(bazi_html, unsafe_allow_html=True)
                    
                    if res['clash_zodiac']:
                        st.markdown(f"<div style='color:#E74C3C; text-align:center; font-weight:bold; margin-top:10px;'>⚠️ วัน{bazi['day']['zodiac']} ชงกับ {res['clash_zodiac']}</div>", unsafe_allow_html=True)
                    
                    safe_element = bazi['day']['element'].replace('+', '').replace('-', '')
                    tip_box = f"<div style='background-color:#FDF2E9; border-left:4px solid #E67E22; padding:15px; margin-top:20px; font-size:0.9rem; color:#D35400; border-radius:5px;'><b>💡 คำแนะนำจากซินแสประจำวัน:</b><br><br>ถ้าพบปัญหา... จงหาคนหรือสิ่งที่มีชื่อเกี่ยวกับ <b>\"ธาตุ{safe_element}\"</b> จะช่วยแก้ไขสถานการณ์ได้</div>"
                    st.markdown(tip_box, unsafe_allow_html=True)

                # --- ตาราง 12 ชั่วยาม ---
                st.markdown("<br>#### ⏰ ตารางยามดี-ร้าย และ 12 ราศีที่ปลอดภัยประจำยาม", unsafe_allow_html=True)
                
                table_rows = ""
                for h in res['hourly_table']:
                    q_symbol = f"<span class='star-spec'>{h['quality']}</span>" if h['quality'] == "⭐" else f"<span class='star-good'>{h['quality']}</span>" if h['quality'] == "O" else f"<span class='star-bad'>{h['quality']}</span>"
                    safe_z_str = ", ".join(h['safe_zodiacs'][:6]) + "..."
                    table_rows += f"<tr><td><b>ดาว {h['star']}</b></td><td><b>{h['pillar_cn']}</b></td><td>{h['element']}</td><td>{q_symbol}</td><td>{h['time']}</td><td style='text-align:left;'>{safe_z_str}</td></tr>"
                
                full_table_html = f"<table class='hourly-table'><thead><tr><th style='width: 10%;'>ดาว</th><th style='width: 12%;'>ยาม</th><th style='width: 18%;'>ธาตุ/นักษัตร</th><th style='width: 12%;'>ฤกษ์</th><th style='width: 20%;'>ช่วงเวลา</th><th>ราศีปลอดภัยประจำยาม</th></tr></thead><tbody>{table_rows}</tbody></table>"
                
                st.markdown(full_table_html, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"🔌 เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# ==========================================
# TAB 2: ฤกษ์จีน (ค้นหามหาฤกษ์)
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
            res_c = requests.post("https://fengshui-platform.onrender.com/analyze-dates", json=payload).json()
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
            st.error(f"🔌 เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# ==========================================
# TAB 3: ฤกษ์ไทย (สแกนฤกษ์ล่าง)
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
            st.error(f"🔌 เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
