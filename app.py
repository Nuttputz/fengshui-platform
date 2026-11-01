import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="ใบปฏิทินซินแสประจำวัน", page_icon="📜", layout="wide")

# CSS สำหรับจำลองหน้ากระดาษหนังสือซินแส
st.markdown("""
    <style>
    .paper-container {
        background-color: #FAFAFA;
        border: 2px solid #333333;
        padding: 25px;
        border-radius: 5px;
        font-family: 'Kanit', sans-serif;
        color: #222;
        max-width: 950px;
        margin: 0 auto;
    }
    .header-title { text-align: right; font-size: 1.4rem; font-weight: bold; color: #111; }
    .header-sub { text-align: right; font-size: 0.95rem; color: #444; }
    .bazi-box {
        border: 1px solid #000;
        text-align: center;
        padding: 5px;
        background: #fff;
        font-size: 0.9rem;
    }
    .bazi-title { background: #eee; font-weight: bold; border-bottom: 1px solid #000; padding: 2px; }
    .sector-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 5px;
        text-align: center;
        margin-top: 10px;
    }
    .sector-card {
        border: 1px solid #999;
        padding: 8px;
        border-radius: 4px;
        background: #fff;
        font-size: 0.85rem;
    }
    .sector-forbidden {
        background: #444444 !important;
        color: #ffffff !important;
    }
    .sheet-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.8rem;
        margin-top: 15px;
        text-align: center;
    }
    .sheet-table th, .sheet-table td {
        border: 1px solid #444;
        padding: 4px 2px;
    }
    .sheet-table th { background-color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

st.title("📜 ปฏิทินซินแสรายวัน (Feng Shui Manual Sheet)")

# ตัวเลือกวันที่
col_input, _ = st.columns([1, 2])
with col_input:
    selected_date = st.date_input("เลือกวันที่ต้องการสร้างใบปฏิทิน", date.today())

if st.button("🔮 ดึงใบปฏิทินซินแสประจำวัน", use_container_width=True):
    with st.spinner("กำลังประกอบใบปฏิทิน..."):
        try:
            res = requests.post("https://fengshui-platform.onrender.com/generate-daily-sheet", json={"target_date": str(selected_date)}).json()
            
            # --- เริ่มวาดกระดาษปฏิทิน ---
            st.markdown("<div class='paper-container'>", unsafe_allow_html=True)
            
            # 1. ส่วนหัวกระดาษ (Header)[cite: 8, 9]
            head_col1, head_col2 = st.columns([1, 1])
            with head_col1:
                st.markdown(f"**ดีกับคนรหัส:** {res['good_person_gua']}")
                st.markdown(f"**ดีกับบ้านรหัส:** {res['good_house_gua']}")
            with head_col2:
                st.markdown(f"<div class='header-title'>{res['date_str']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='header-sub'>{res['day_element']}</div>", unsafe_allow_html=True)
                
            st.markdown("---")
            
            # 2. ส่วนตรงกลาง: ปาจื่อ + ทิศทาง 8 ทิศ + คำแนะนำ[cite: 8, 9]
            mid_col1, mid_col2 = st.columns([1.2, 1])
            
            with mid_col1:
                st.markdown("#### 🧭 ผังพลังงาน 8 ทิศ & 24 ขุนเขา")
                st.caption("พื้นที่แรเงาสีเข้ม คือ **ห้าม รบกวน เคาะ ตอก เจาะ ขุด**[cite: 8, 9]")
                
                # วาดการ์ด 8 ทิศ (3x3 Grid)
                sec = res['sectors']
                grid_html = f"""
                <div class='sector-grid'>
                    <div class='sector-card {"sector-forbidden" if sec[7]["forbidden"] else ""}'><b>{sec[7]["dir"]}</b><br>ดาว {sec[7]["star"]}<br>{sec[7]["label"]}</div>
                    <div class='sector-card {"sector-forbidden" if sec[0]["forbidden"] else ""}'><b>{sec[0]["dir"]}</b><br>ดาว {sec[0]["star"]}<br>{sec[0]["label"]}</div>
                    <div class='sector-card {"sector-forbidden" if sec[1]["forbidden"] else ""}'><b>{sec[1]["dir"]}</b><br>ดาว {sec[1]["star"]}<br>{sec[1]["label"]}</div>
                    <div class='sector-card {"sector-forbidden" if sec[6]["forbidden"] else ""}'><b>{sec[6]["dir"]}</b><br>ดาว {sec[6]["star"]}<br>{sec[6]["label"]}</div>
                    <div class='sector-card' style='background:#fff8e1;'><b>กลางบ้าน</b><br>ดาว 1</div>
                    <div class='sector-card {"sector-forbidden" if sec[2]["forbidden"] else ""}'><b>{sec[2]["dir"]}</b><br>ดาว {sec[2]["star"]}<br>{sec[2]["label"]}</div>
                    <div class='sector-card {"sector-forbidden" if sec[5]["forbidden"] else ""}'><b>{sec[5]["dir"]}</b><br>ดาว {sec[5]["star"]}<br>{sec[5]["label"]}</div>
                    <div class='sector-card {"sector-forbidden" if sec[4]["forbidden"] else ""}'><b>{sec[4]["dir"]}</b><br>ดาว {sec[4]["star"]}<br>{sec[4]["label"]}</div>
                    <div class='sector-card {"sector-forbidden" if sec[3]["forbidden"] else ""}'><b>{sec[3]["dir"]}</b><br>ดาว {sec[3]["star"]}<br>{sec[3]["label"]}</div>
                </div>
                """
                st.markdown(grid_html, unsafe_allow_html=True)
                
            with mid_col2:
                # แสดงตารางปาจื่อ 3 เสา[cite: 8, 9]
                st.markdown("#### 📜 ดิถีและ 3 เสาชะตา")
                bz = res['bazi']
                bazi_html = f"""
                <table style='width:100%; border-collapse:collapse; text-align:center; font-size:0.85rem;'>
                    <tr style='background:#eee;'><th>วัน</th><th>เดือน</th><th>ปี</th></tr>
                    <tr>
                        <td><b>{bz['day']['stem']}</b> ({bz['day']['stem_info'][0]})<br><b>{bz['day']['branch']}</b> ({bz['day']['branch_info'][0]})</td>
                        <td><b>{bz['month']['stem']}</b> ({bz['month']['stem_info'][0]})<br><b>{bz['month']['branch']}</b> ({bz['month']['branch_info'][0]})</td>
                        <td><b>{bz['year']['stem']}</b> ({bz['year']['stem_info'][0]})<br><b>{bz['year']['branch']}</b> ({bz['year']['branch_info'][0]})</td>
                    </tr>
                </table>
                <div style='text-align:center; color:red; margin-top:5px; font-weight:bold;'>{res['clash_info']}</div>
                """
                st.markdown(bazi_html, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"💡 **ข้อแนะนำประจำวัน:**\n{res['advice']}")
                st.warning(res['remedy'])

            # 3. ส่วนล่าง: ตาราง 12 ชั่วยามพร้อมเช็กลิสต์นักษัตรปลอดภัย
            st.markdown("<br><h4>⏰ ตารางยามดี-ร้าย และ ทิศปลอดภัยประจำยาม</h4>", unsafe_allow_html=True)
            
            # สร้างตาราง HTML สไตล์หนังสือ[cite: 8, 9, 10]
            z_headers = "".join([f"<th>{z}</th>" for z in res['zodiac_headers']])
            table_html = f"""
            <table class='sheet-table'>
                <thead>
                    <tr>
                        <th>ยาม</th>
                        <th>ก้าน/กิ่ง</th>
                        <th>ธาตุ</th>
                        <th>ยามดี-ร้าย</th>
                        <th>เวลา</th>
                        {z_headers}
                    </tr>
                </thead>
                <tbody>
            """
            
            for row in res['hours_table']:
                # สร้างเครื่องหมาย ✓ สำหรับนักษัตรที่ปลอดภัย[cite: 8, 9, 10]
                checks = "".join([f"<td>{'✓' if z in row['safe_zodiacs'] else ''}</td>" for z in res['zodiac_headers']])
                table_html += f"""
                    <tr>
                        <td><b>{row['hour_num']}</b></td>
                        <td><b>{row['stem']}{row['branch']}</b></td>
                        <td>{row['element']}</td>
                        <td>{row['rating']}</td>
                        <td>{row['time']}</td>
                        {checks}
                    </tr>
                """
            table_html += "</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"ไม่สามารถเชื่อมต่อกับ Backend ได้: {e}")
