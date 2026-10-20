import streamlit as st
import requests
from datetime import date, datetime

st.set_page_config(page_title="ระบบผู้เชี่ยวชาญฤกษ์ยาม", page_icon="☯️", layout="centered")

st.markdown("""
    <style>
    .stButton>button { background-color: #D4AF37; color: white; border-radius: 25px; border: none; font-weight: bold; font-size: 1rem; padding: 10px 24px; transition: all 0.3s; }
    .stButton>button:hover { background-color: #B5952F; box-shadow: 0px 4px 12px rgba(212, 175, 55, 0.4); }
    div[data-testid="stForm"] { border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); border: 1px solid #e0e0e0; padding: 20px; background-color: #ffffff; }
    .dash-card { background-color: #f8f9fa; border-left: 5px solid #D4AF37; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2C3E50;'>☯️ ระบบผู้เชี่ยวชาญฤกษ์ยาม (AI ซินแส)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7F8C8D; margin-bottom: 25px;'>รวมศาสตร์ฮวงจุ้ยดาว 9 ยุค ปาจื่อ และ โหราศาสตร์ไทยกาลโยค</p>", unsafe_allow_html=True)

# 🌟 เพิ่มแท็บหน้าแรก
tab_home, tab_chinese, tab_thai = st.tabs(["🏠 หน้าแรก (Dashboard)", "☯️ ฤกษ์จีน (หาวันมงคล)", "☸️ ฤกษ์ไทย (สแกนฤกษ์ล่าง)"])

# ==========================================
# TAB 0: DASHBOARD หน้าแรก (ใหม่ล่าสุด)
# ==========================================
with tab_home:
    st.markdown("### 🗓️ ภาพรวมพลังงานประจำวัน (Daily Dashboard)")
    st.markdown("ตรวจสอบทิศทางดี-ร้าย และพลังงานของวันแบบทันที")
    
    selected_date = st.date_input("📅 เลือกวันที่ต้องการดูสรุป", date.today(), key="dash_date")
    
    if st.button("📊 สรุปพลังงานวันนี้", use_container_width=True, key="btn_dash"):
        with st.spinner("กำลังโหลดข้อมูลพลังงานฟ้าดิน..."):
            try:
                res = requests.post("http://127.0.0.1:8000/daily-dashboard", json={"target_date": str(selected_date)}).json()
                
                # การ์ดสรุปฤกษ์
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div class='dash-card'><b>☯️ ปาจื่อ (จีน):</b> วัน{res['chinese']['day_zodiac']}<br><span style='color:red;'>⚠️ ชงกับคนปี: {res['chinese']['clash']}</span></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='dash-card'><b>☸️ โหรไทย:</b> {res['thai']['kalyok']}<br><span style='color:#2980b9;'>🌟 ฤกษ์ล่าง: {res['thai']['reuk']}</span></div>", unsafe_allow_html=True)
                
                # ดาวจรศูนย์กลาง
                st.markdown("#### 🧭 ดาวจร 9 ยุค (ดาวที่สถิตกลางบ้าน)")
                sc1, sc2, sc3 = st.columns(3)
                sc1.metric("ดาวจรปี (Annual)", f"ดาว {res['stars']['year']}")
                sc2.metric("ดาวจรเดือน (Monthly)", f"ดาว {res['stars']['month']}")
                sc3.metric("ดาวจรวัน (Daily)", f"ดาว {res['stars']['day']}")
                
                # ทิศห้ามกระทบ
                st.markdown("#### 🚫 ทิศห้ามกระทบ (ห้ามเคาะ ทุบ เจาะ ซ่อมแซมหน้าดิน)")
                st.error(f"⚔️ **ทิศไท้ส่วย (เทพประจำปี):** {res['taboos']['tai_sui']}\n\n"
                         f"👹 **ทิศอสูร (ซาสั่วะ):** {res['taboos']['san_sha']}\n\n"
                         f"💥 **ทิศดาว 5 เหลือง (ดาววิบัติประจำปี):** {res['taboos']['year_5']}\n\n"
                         f"⚠️ **ทิศดาว 5 เหลือง (ดาววิบัติประจำเดือน):** {res['taboos']['month_5']}")
                
            except Exception as e:
                st.error("🔌 ไม่สามารถเชื่อมต่อกับ Backend ได้ กรุณาตรวจสอบการรันเซิร์ฟเวอร์")

# ==========================================
# TAB 1: ฤกษ์จีน (เหมือนเดิม)
# ==========================================
with tab_chinese:
    with st.form("chinese_form"):
        col1, col2 = st.columns(2)
        with col1:
            zodiac_c = st.selectbox("ปีเกิดนักษัตรของคุณ", ["ชวด", "ฉลู", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะเมีย", "มะแม", "วอก", "ระกา", "จอ", "กุน"])
            fav_elements = st.multiselect("ธาตุส่งเสริม", ["ไม้", "ไฟ", "ดิน", "ทอง", "น้ำ"], default=["ทอง", "น้ำ"])
        with col2:
            start_date_c = st.date_input("วันที่เริ่มค้นหาฤกษ์", date.today())
            house_degree = st.number_input("องศาหน้าบ้าน (0-359)", min_value=0, max_value=359, value=0)
            days_c = st.slider("จำนวนวันที่สแกน", 1, 30, 7)
        submit_chinese = st.form_submit_button("🔮 คำนวณฤกษ์จีน", use_container_width=True)

    if submit_chinese:
        payload = {"birth_year_zodiac": zodiac_c, "favorable_elements": fav_elements, "house_degree": int(house_degree), "start_date": str(start_date_c), "days_to_scan": int(days_c)}
        try:
            res_c = requests.post("http://127.0.0.1:8000/analyze-dates", json=payload).json()
            st.subheader("📊 ปฏิทินฤกษ์มงคลจีน")
            
            # --- สร้างปฏิทินแบบ Grid ---
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
# TAB 2: ฤกษ์ไทย (เหมือนเดิม)
# ==========================================
with tab_thai:
    with st.form("thai_form"):
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
            res_t = requests.post("http://127.0.0.1:8000/analyze-thai-dates", json=payload_thai).json()
            st.subheader("📊 รายงานผลฤกษ์ไทย")
            for day in res_t["data"]:
                icon = "✅" if day["status"] == "Green Zone" else "❌" if day["status"] == "Red Zone" else "⚠️"
                bd = "#4caf50" if day["status"] == "Green Zone" else "#f44336" if day["status"] == "Red Zone" else "#ffc107"
                st.markdown(f"<div style='background-color:#f9f9f9; padding:12px; border-radius:8px; margin-bottom:8px; border-left: 5px solid {bd};'><b>{icon} วัน{day['weekday']}ที่ {day['date']}</b> | ฤกษ์: <u>{day['thai_reuk']}</u> ({day['kalyok']})<br><small>{day['reason']}</small></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("ไม่สามารถเชื่อมต่อกับ Backend ได้")