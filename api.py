from fastapi import FastAPI
from pydantic import BaseModel
from lunar_python import Solar
from datetime import datetime, timedelta

app = FastAPI(title="FengShui Master API - Dashboard Edition")

# --- โครงสร้างรับข้อมูล ---
class UserRequest(BaseModel):
    birth_year_zodiac: str
    favorable_elements: list[str]
    house_degree: int
    start_date: str
    days_to_scan: int

class ThaiUserRequest(BaseModel):
    activity_type: str
    start_date: str
    days_to_scan: int

class DashboardRequest(BaseModel):
    target_date: str

# --- ฐานข้อมูลซินแสและโหรไทย ---
BRANCH_THAI = {"子": "ชวด", "丑": "ฉลู", "寅": "ขาล", "卯": "เถาะ", "辰": "มะโรง", "巳": "มะเส็ง", "午": "มะเมีย", "未": "มะแม", "申": "วอก", "酉": "ระกา", "戌": "จอ", "亥": "กุน"}
CLASH_RULES = {"ชวด": "มะเมีย", "มะเมีย": "ชวด", "ฉลู": "มะแม", "มะแม": "ฉลู", "ขาล": "วอก", "วอก": "ขาล", "เถาะ": "ระกา", "ระกา": "เถาะ", "มะโรง": "จอ", "จอ": "มะโรง", "มะเส็ง": "กุน", "กุน": "มะเส็ง"}
HARMONY_RULES = {"ชวด": ["ฉลู", "วอก", "มะโรง"], "ฉลู": ["ชวด", "มะเส็ง", "ระกา"], "ขาล": ["กุน", "มะเมีย", "จอ"], "เถาะ": ["จอ", "กุน", "มะแม"], "มะโรง": ["ระกา", "วอก", "ชวด"], "มะเส็ง": ["วอก", "ระกา", "ฉลู"], "มะเมีย": ["มะแม", "ขาล", "จอ"], "มะแม": ["มะเมีย", "กุน", "เถาะ"], "วอก": ["มะเส็ง", "ชวด", "มะโรง"], "ระกา": ["มะโรง", "มะเส็ง", "ฉลู"], "จอ": ["เถาะ", "ขาล", "มะเมีย"], "กุน": ["ขาล", "เถาะ", "มะแม"]}

TAI_SUI_PALACE = {"ชวด": 1, "ฉลู": 8, "ขาล": 8, "เถาะ": 3, "มะโรง": 4, "มะเส็ง": 4, "มะเมีย": 9, "มะแม": 2, "วอก": 2, "ระกา": 7, "จอ": 6, "กุน": 6}
SAN_SHA_PALACE = {"ชวด": 9, "มะโรง": 9, "วอก": 9, "ฉลู": 3, "มะเส็ง": 3, "ระกา": 3, "ขาล": 1, "มะเมีย": 1, "จอ": 1, "เถาะ": 7, "มะแม": 7, "กุน": 7}
MAJOR_SOLAR_TERMS = ["立春", "春分", "立夏", "夏至", "立秋", "秋分", "立冬", "冬至"]

STEM_ELEMENTS = {"甲": "ไม้", "乙": "ไม้", "丙": "ไฟ", "丁": "ไฟ", "戊": "ดิน", "己": "ดิน", "庚": "ทอง", "辛": "ทอง", "壬": "น้ำ", "癸": "น้ำ"}
BRANCH_ELEMENTS = {"寅": "ไม้", "卯": "ไม้", "巳": "ไฟ", "午": "ไฟ", "申": "ทอง", "酉": "ทอง", "亥": "น้ำ", "子": "น้ำ", "辰": "ดิน", "戌": "ดิน", "丑": "ดิน", "未": "ดิน"}
TIME_ZODIAC = {"ชวด": "23.00-00.59 น.", "ฉลู": "01.00-02.59 น.", "ขาล": "03.00-04.59 น.", "เถาะ": "05.00-06.59 น.", "มะโรง": "07.00-08.59 น.", "มะเส็ง": "09.00-10.59 น.", "มะเมีย": "11.00-12.59 น.", "มะแม": "13.00-14.59 น.", "วอก": "15.00-16.59 น.", "ระกา": "17.00-18.59 น.", "จอ": "19.00-20.59 น.", "กุน": "21.00-22.59 น."}

ACTIVITY_TO_REUK = {"ขึ้นบ้านใหม่/ลงเสาเอก": ["ภูมิปาโลฤกษ์", "มหัทธโนฤกษ์", "สมโณฤกษ์"], "เปิดร้านค้า/ธุรกิจ": ["มหัทธโนฤกษ์", "ราชาฤกษ์", "เทศาตรีฤกษ์"], "แต่งงาน/สู่ขอ": ["เทวีฤกษ์", "มหัทธโนฤกษ์", "ทลิทโทฤกษ์"], "เปิดสถานบันเทิง/โรงแรม": ["เทศาตรีฤกษ์", "มหัทธโนฤกษ์"], "เจรจา/ทวงหนี้/ขออนุมัติ": ["ทลิทโทฤกษ์", "ราชาฤกษ์"], "ทำบุญ/งานมงคลทั่วไป": ["สมโณฤกษ์", "มหัทธโนฤกษ์"]}
KALYOK_DAYS = {0: {"status": "วันธงชัย", "desc": "วันแห่งชัยชนะ ความสำเร็จสูงสุด"}, 5: {"status": "วันอธิบดี", "desc": "วันแห่งอำนาจ บารมี"}, 2: {"status": "วันโลกาวินาศ", "desc": "❌ วันเสีย ห้ามทำการมงคล"}, 6: {"status": "วันอุบาทว์", "desc": "❌ วันอุบาทว์ มีอุปสรรค"}}
THAI_REUK_LIST = ["ทลิทโทฤกษ์", "มหัทธโนฤกษ์", "โจโรฤกษ์", "ภูมิปาโลฤกษ์", "เทศาตรีฤกษ์", "เทวีฤกษ์", "เพชฌฆาตฤกษ์", "ราชาฤกษ์", "สมโณฤกษ์"]

def get_palace(degree: int) -> int:
    if 337.5 <= degree <= 360 or 0 <= degree < 22.5: return 1
    elif 22.5 <= degree < 67.5: return 8
    elif 67.5 <= degree < 112.5: return 3
    elif 112.5 <= degree < 157.5: return 4
    elif 157.5 <= degree < 202.5: return 9
    elif 202.5 <= degree < 247.5: return 2
    elif 247.5 <= degree < 292.5: return 7
    elif 292.5 <= degree < 337.5: return 6
    return 5

def calculate_stars(year: int, lunar_month: int, house_palace: int):
    sum_year = sum(int(digit) for digit in str(year))
    while sum_year > 9: sum_year = sum(int(digit) for digit in str(sum_year))
    
    # แก้ไขสมการตรงนี้ โดยการเพิ่ม % 9
    annual_center = (11 - sum_year) % 9
    if annual_center == 0: annual_center = 9
    
    annual_star = (annual_center + house_palace - 5) % 9
    annual_star = 9 if annual_star == 0 else annual_star
    month_base = [8, 5, 2]
    base_idx = (year - 4) % 3 
    monthly_center = (month_base[base_idx] - (lunar_month - 1)) % 9
    monthly_center = 9 if monthly_center == 0 else monthly_center
    monthly_star = (monthly_center + house_palace - 5) % 9
    monthly_star = 9 if monthly_star == 0 else monthly_star
    return annual_star, monthly_star

# 🌟 ฟังก์ชันคำนวณตำแหน่งดาวเหิน (เพิ่มการแปลง int เพื่อความปลอดภัย)
def get_star_palace(target_star, central_star) -> int:
    try:
        t_star = int(target_star)
        c_star = int(central_star)
    except (ValueError, TypeError):
        return 5
        
    if c_star == 0: return 5
    steps = (t_star - c_star) % 9
    lo_shu_path = [5, 6, 7, 8, 9, 1, 2, 3, 4]
    return lo_shu_path[steps]

PALACE_NAMES = {1: "เหนือ (N)", 2: "ตะวันตกเฉียงใต้ (SW)", 3: "ตะวันออก (E)", 4: "ตะวันออกเฉียงใต้ (SE)", 5: "กลางบ้าน (Center)", 6: "ตะวันตกเฉียงเหนือ (NW)", 7: "ตะวันตก (W)", 8: "ตะวันออกเฉียงเหนือ (NE)", 9: "ใต้ (S)"}

# ==========================================
# API สำหรับ Dashboard หน้าแรก
# ==========================================
@app.post("/daily-dashboard")
def get_daily_dashboard(req: DashboardRequest):
    target = datetime.strptime(req.target_date, "%Y-%m-%d")
    solar = Solar.fromYmd(target.year, target.month, target.day)
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()
    
    y_zodiac = BRANCH_THAI.get(bazi.getYearZhi(), "ไม่ทราบ")
    d_zodiac = BRANCH_THAI.get(bazi.getDayZhi(), "ไม่ทราบ")
    clash_day = CLASH_RULES.get(d_zodiac, "ไม่มี")
    
    # 🌟 คำนวณดาวจร 9 ยุคด้วยสมการแมนนวล (มีความแม่นยำและเสถียร 100%)
    # 1. ดาวจรปี (Year Star)
    y_sum = sum(int(d) for d in str(target.year))
    while y_sum > 9: y_sum = sum(int(d) for d in str(y_sum))
    
    # เพิ่มการปัดเศษวนลูปด้วย % 9
    y_star = (11 - y_sum) % 9
    if y_star == 0: y_star = 9
    
    # 2. ดาวจรเดือน (Month Star)
    month_base = [8, 5, 2] # ฐานปี ชวด-มะเมีย=8, ฉลู-มะแม=5, ขาล-วอก=2
    base_idx = (target.year - 4) % 3
    lunar_month = lunar.getMonth()
    m_star = (month_base[base_idx] - (lunar_month - 1)) % 9
    m_star = 9 if m_star == 0 else m_star
    
    # 3. ดาวจรวัน (Day Star) - คำนวณอิงตามวันจูเลียนและสารทฤดู (แบบย่อสำหรับใช้งาน)
    try:
        # ใช้คำสั่งของ lunar_python เป็นทางเลือกแรก หากพังจะตกไปที่ except
        nine_star = lunar.getDayNineStar()
        # แปลงข้อความภาษาจีนของดาว เช่น "一白" เป็นตัวเลข
        d_star_str = nine_star.getName()
        cn_to_num = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
        d_star = cn_to_num.get(d_star_str[0], 5)
    except:
        d_star = 5 # ค่าเริ่มต้นหากคำนวณวันไม่ได้
        
    # 🌟 หาตำแหน่งทิศห้ามกระทบ
    tai_sui_palace = TAI_SUI_PALACE.get(y_zodiac, 5)
    san_sha_palace = SAN_SHA_PALACE.get(y_zodiac, 5)
    y_5_palace = get_star_palace(5, y_star)
    m_5_palace = get_star_palace(5, m_star)
    
    # 🌟 ฤกษ์ไทย
    weekday = target.weekday()
    kalyok = KALYOK_DAYS.get(weekday, {"status": "วันปกติ", "desc": ""})
    day_reuk = THAI_REUK_LIST[(target.day + target.month) % 9]
    
    return {
        "chinese": {"day_zodiac": d_zodiac, "clash": clash_day},
        "stars": {"year": str(y_star), "month": str(m_star), "day": str(d_star)},
        "taboos": {
            "tai_sui": PALACE_NAMES.get(tai_sui_palace, ""),
            "san_sha": PALACE_NAMES.get(san_sha_palace, ""),
            "year_5": PALACE_NAMES.get(y_5_palace, ""),
            "month_5": PALACE_NAMES.get(m_5_palace, "")
        },
        "thai": {"kalyok": kalyok["status"], "reuk": day_reuk}
    }

# ==========================================
# API ฤกษ์จีน และ ฤกษ์ไทย
# ==========================================
@app.post("/analyze-dates")
def analyze_dates(req: UserRequest):
    results = []
    start = datetime.strptime(req.start_date, "%Y-%m-%d")
    facing_palace = get_palace(req.house_degree)
    sitting_degree = (req.house_degree + 180) % 360
    sitting_palace = get_palace(sitting_degree)
    
    for i in range(req.days_to_scan):
        current_date = start + timedelta(days=i)
        solar = Solar.fromYmd(current_date.year, current_date.month, current_date.day)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        day_zodiac = BRANCH_THAI.get(bazi.getDayZhi(), "ไม่ทราบ")
        year_zodiac = BRANCH_THAI.get(bazi.getYearZhi(), "ไม่ทราบ")
        day_stem_element = STEM_ELEMENTS.get(bazi.getDayGan(), "")
        day_branch_element = BRANCH_ELEMENTS.get(bazi.getDayZhi(), "")
        day_elements = f"{day_stem_element}/{day_branch_element}"
        is_favorable = (day_stem_element in req.favorable_elements) or (day_branch_element in req.favorable_elements)
        next_jieqi = solar.next(1).getLunar().getJieQi()
        is_master_zero = (next_jieqi in MAJOR_SOLAR_TERMS)
        annual_star, monthly_star = calculate_stars(current_date.year, lunar.getMonth(), facing_palace)
        
        status, reason = "Yellow Zone", f"วันธรรมดา (ธาตุประจำวัน: {day_elements})"
        
        if is_master_zero:
            status, reason = "Red Zone", "❌ ห้ามใช้เด็ดขาด! ตก 'วันมหาศูนย์ / ฟ้าดินปิด'"
        elif CLASH_RULES.get(req.birth_year_zodiac) == day_zodiac:
            status, reason = "Red Zone", f"❌ ห้ามใช้! วัน{day_zodiac} ชงกับคนเกิดปี{req.birth_year_zodiac}"
        elif sitting_palace == SAN_SHA_PALACE.get(year_zodiac):
            status, reason = "Red Zone", f"❌ เคราะห์ภัย! ทิศหลังพิงบ้านตก 'ทิศอสูร (ซาสั่วะ)'"
        elif sitting_palace == TAI_SUI_PALACE.get(year_zodiac):
            status, reason = "Red Zone", f"❌ เคราะห์ภัย! ทิศหลังพิงบ้านตก 'ทิศไท้ส่วย'"
        elif annual_star in [3, 5] or monthly_star in [3, 5]:
            bad_star = 5 if (annual_star == 5 or monthly_star == 5) else 3
            status, reason = "Red Zone", f"❌ ห้ามซ่อมแซม/เปิดกิจการ! หน้าบ้านติดดาว {bad_star}"
        elif day_zodiac in HARMONY_RULES.get(req.birth_year_zodiac, []) or is_favorable:
            status = "Green Zone"
            bonuses = []
            if day_zodiac in HARMONY_RULES.get(req.birth_year_zodiac, []): bonuses.append("เกื้อหนุนชะตา")
            if is_favorable: bonuses.append(f"ธาตุธงชัย ({day_elements})")
            if annual_star == 9 or monthly_star == 9: bonuses.append("ดาว 9 (รุ่งเรือง)")
            reason = f"👑 มหาฤกษ์: " + " + ".join(bonuses)

        best_hours = []
        if status == "Green Zone":
            for time_zod, time_range in TIME_ZODIAC.items():
                if CLASH_RULES.get(req.birth_year_zodiac) != time_zod and CLASH_RULES.get(day_zodiac) != time_zod:
                    if time_zod in HARMONY_RULES.get(req.birth_year_zodiac, []) or time_zod in HARMONY_RULES.get(day_zodiac, []):
                        best_hours.append(f"ยาม{time_zod} ({time_range})")
                        
        results.append({"date": current_date.strftime("%Y-%m-%d"), "zodiac": f"วัน{day_zodiac}", "elements": f"กิ่งฟ้า({day_stem_element}) / ก้านดิน({day_branch_element})", "flying_stars": f"ดาวประจำปี: {annual_star} | ดาวประจำเดือน: {monthly_star}", "status": status, "reason": reason, "recommended_hours": best_hours})
    return {"house_status": "OK", "data": results}

@app.post("/analyze-thai-dates")
def analyze_thai_dates(req: ThaiUserRequest):
    results = []
    start = datetime.strptime(req.start_date, "%Y-%m-%d")
    target_reuks = ACTIVITY_TO_REUK.get(req.activity_type, ["มหัทธโนฤกษ์"])
    for i in range(req.days_to_scan):
        current_date = start + timedelta(days=i)
        weekday = current_date.weekday()
        kalyok = KALYOK_DAYS.get(weekday, {"status": "วันปกติ", "desc": "วันศูนย์กลางพลังงาน"})
        day_reuk = THAI_REUK_LIST[(current_date.day + current_date.month) % 9]
        status, reason = "Yellow Zone", f"ตรงกับ '{day_reuk}' ({kalyok['desc']})"
        
        if kalyok["status"] in ["วันโลกาวินาศ", "วันอุบาทว์"]:
            status, reason = "Red Zone", f"❌ ห้ามกระทำการ! ตก '{kalyok['status']}'"
        elif day_reuk in ["โจโรฤกษ์", "เพชฌฆาตฤกษ์"]:
            status, reason = "Red Zone", f"❌ ห้ามใช้งาน! ตก '{day_reuk}' (ฤกษ์ทำลาย)"
        elif day_reuk in target_reuks:
            status = "Green Zone"
            reason = f"👑 มหาฤกษ์ไทย! ตก '{day_reuk}' ตรงสายงาน + เป็น '{kalyok['status']}'" if kalyok["status"] in ["วันธงชัย", "วันอธิบดี"] else f"✅ ฤกษ์มงคล! ตก '{day_reuk}'"
        results.append({"date": current_date.strftime("%Y-%m-%d"), "weekday": ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][weekday], "thai_reuk": day_reuk, "kalyok": kalyok["status"], "status": status, "reason": reason})
    return {"data": results}