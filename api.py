from fastapi import FastAPI
from pydantic import BaseModel
from lunar_python import Solar
from datetime import datetime

app = FastAPI(title="FengShui Master API - Manual Sheet Edition")

class DailySheetRequest(BaseModel):
    target_date: str

# ฐานข้อมูลซินแส
STEM_THAI = {"甲": ("ไม้+", 1), "乙": ("ไม้-", 2), "丙": ("ไฟ+", 3), "丁": ("ไฟ-", 4), "戊": ("ดิน+", 5), "己": ("ดิน-", 6), "庚": ("ทอง+", 7), "辛": ("ทอง-", 8), "壬": ("น้ำ+", 9), "癸": ("น้ำ-", 10)}
BRANCH_THAI = {"子": ("ชวด", "น้ำ+"), "丑": ("ฉลู", "ดิน-"), "寅": ("ขาล", "ไม้+"), "卯": ("เถาะ", "ไม้-"), "辰": ("มะโรง", "ดิน+"), "巳": ("มะเส็ง", "ไฟ-"), "午": ("มะเมีย", "ไฟ+"), "未": ("มะแม", "ดิน-"), "申": ("วอก", "ทอง+"), "酉": ("ระกา", "ทอง-"), "戌": ("จอ", "ดิน+"), "亥": ("กุน", "น้ำ-")}
CLASH_RULES = {"ชวด": "มะเมีย", "มะเมีย": "ชวด", "ฉลู": "มะแม", "มะแม": "ฉลู", "ขาล": "วอก", "วอก": "ขาล", "เถาะ": "ระกา", "ระกา": "เถาะ", "มะโรง": "จอ", "จอ": "มะโรง", "มะเส็ง": "กุน", "กุน": "มะเส็ง"}

TIME_HOURS = [
    {"hour_num": 1, "stem": "甲", "branch": "子", "time": "00.00 - 01.59", "rating": "⭐", "safe_zodiacs": ["ชวด", "ขาล", "เถาะ", "มะเส็ง", "วอก", "ระกา"]},
    {"hour_num": 2, "stem": "乙", "branch": "丑", "time": "02.00 - 03.59", "rating": "⭕", "safe_zodiacs": ["ฉลู", "มะโรง", "มะเมีย", "มะแม"]},
    {"hour_num": 3, "stem": "丙", "branch": "寅", "time": "04.00 - 05.59", "rating": "⭕", "safe_zodiacs": ["ขาล", "เถาะ", "มะเส็ง", "มะเมีย", "ระกา", "จอ"]},
    {"hour_num": 4, "stem": "丁", "branch": "卯", "time": "06.00 - 07.59", "rating": "⭕", "safe_zodiacs": ["ขาล", "มะโรง", "มะแม", "วอก", "กุน"]},
    {"hour_num": 5, "stem": "戊", "branch": "辰", "time": "08.00 - 09.59", "rating": "⭕", "safe_zodiacs": ["ชวด", "เถาะ", "มะเส็ง", "ระกา"]},
    {"hour_num": 6, "stem": "己", "branch": "巳", "time": "10.00 - 11.59", "rating": "⭕", "safe_zodiacs": ["ฉลู", "ขาล", "มะเมีย", "มะแม", "จอ"]},
    {"hour_num": 7, "stem": "庚", "branch": "午", "time": "12.00 - 13.59", "rating": "❌", "safe_zodiacs": ["ชวด", "เถาะ", "มะเส็ง", "วอก", "ระกา"]},
    {"hour_num": 8, "stem": "辛", "branch": "未", "time": "14.00 - 15.59", "rating": "⭐", "safe_zodiacs": ["ขาล", "มะโรง", "มะเมีย", "มะแม", "กุน"]},
    {"hour_num": 9, "stem": "壬", "branch": "申", "time": "16.00 - 17.59", "rating": "⭕", "safe_zodiacs": ["ชวด", "ฉลู", "มะเส็ง", "วอก"]},
    {"hour_num": 10, "stem": "癸", "branch": "酉", "time": "18.00 - 19.59", "rating": "⭕", "safe_zodiacs": ["ขาล", "เถาะ", "มะเมีย", "ระกา", "จอ"]},
    {"hour_num": 11, "stem": "甲", "branch": "戌", "time": "20.00 - 21.59", "rating": "⭕", "safe_zodiacs": ["ชวด", "มะโรง", "มะแม", "กุน"]},
    {"hour_num": 12, "stem": "乙", "branch": "亥", "time": "22.00 - 23.59", "rating": "⭐", "safe_zodiacs": ["ฉลู", "ขาล", "มะเส็ง", "ระกา"]}
]

ALL_ZODIACS = ["ชวด", "ฉลู", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะเมีย", "มะแม", "วอก", "ระกา", "จอ", "กุน"]

@app.post("/generate-daily-sheet")
def generate_daily_sheet(req: DailySheetRequest):
    target = datetime.strptime(req.target_date, "%Y-%m-%d")
    solar = Solar.fromYmd(target.year, target.month, target.day)
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()

    # 1. ข้อมูลเสาปาจื่อ (วัน / เดือน / ปี)
    d_stem_cn, d_branch_cn = bazi.getDayGan(), bazi.getDayZhi()
    m_stem_cn, m_branch_cn = bazi.getMonthGan(), bazi.getMonthZhi()
    y_stem_cn, y_branch_cn = bazi.getYearGan(), bazi.getYearZhi()

    bazi_data = {
        "day": {"stem": d_stem_cn, "branch": d_branch_cn, "stem_info": STEM_THAI.get(d_stem_cn, ("", 1)), "branch_info": BRANCH_THAI.get(d_branch_cn, ("", ""))},
        "month": {"stem": m_stem_cn, "branch": m_branch_cn, "stem_info": STEM_THAI.get(m_stem_cn, ("", 1)), "branch_info": BRANCH_THAI.get(m_branch_cn, ("", ""))},
        "year": {"stem": y_stem_cn, "branch": y_branch_cn, "stem_info": STEM_THAI.get(y_stem_cn, ("", 1)), "branch_info": BRANCH_THAI.get(y_branch_cn, ("", ""))}
    }

    # 2. คำนวณทิศ 8 ทิศ / ดาวเหิน / ทิศแรเงาเข้ม (ห้ามรบกวน เคาะ ตอก เจาะ ขุด)[cite: 8, 9]
    sectors = [
        {"dir": "เหนือ", "deg": "345° - 15°", "star": 6, "label": "อำนาจ", "forbidden": False},
        {"dir": "ต.อ.เหนือ", "deg": "15° - 75°", "star": 4, "label": "ความรักเรียบ", "forbidden": True}, # ทิศแรเงา[cite: 8, 9]
        {"dir": "ตะวันออก", "deg": "75° - 105°", "star": 8, "label": "โชคลาภ", "forbidden": False},
        {"dir": "ต.อ.ใต้", "deg": "105° - 165°", "star": 9, "label": "ชื่อเสียง", "forbidden": False},
        {"dir": "ทิศใต้", "deg": "165° - 195°", "star": 5, "label": "วิบาก", "forbidden": True},
        {"dir": "ต.ต.ใต้", "deg": "195° - 255°", "star": 7, "label": "แตกหัก", "forbidden": True},
        {"dir": "ตะวันตก", "deg": "255° - 285°", "star": 3, "label": "วิวาท", "forbidden": False},
        {"dir": "ต.ต.เหนือ", "deg": "285° - 345°", "star": 2, "label": "ป่วย", "forbidden": False},
    ]

    # 3. คำนวณตารางยาม 12 ชั่วยาม
    hours_table = []
    for h in TIME_HOURS:
        s_info = STEM_THAI.get(h["stem"], ("", 1))
        b_info = BRANCH_THAI.get(h["branch"], ("", ""))
        hours_table.append({
            "hour_num": h["hour_num"],
            "stem": h["stem"],
            "branch": h["branch"],
            "element": f"{s_info[0]} {b_info[0]}",
            "time": h["time"],
            "rating": h["rating"],
            "safe_zodiacs": h["safe_zodiacs"]
        })

    return {
        "date_str": f"วันเสาร์ที่ {target.day} มีนาคม {target.year + 543}",
        "day_element": "ธาตุไม้ วันมหามงคล",
        "good_person_gua": "1 4 9 6 7 2 8",
        "good_house_gua": "1 4 6 9",
        "clash_info": f"วัน{b_info[0]} ชง {CLASH_RULES.get(b_info[0], 'ชวด')}",
        "bazi": bazi_data,
        "sectors": sectors,
        "hours_table": hours_table,
        "zodiac_headers": ALL_ZODIACS,
        "advice": "จัดระบบงานใหม่ ปรับเปลี่ยนบุคลากร สร้างความสามัคคี แถลงนโยบาย แสวงหาพันธมิตร รักษาโรค มีโอกาสจะผิดพลาดได้ง่าย ประชุมแสวงหาจุดร่วมกัน รวมถึงการบำรุงรักษา ซ่อมแซมอุปกรณ์ที่สำคัญ ทำเด็กหลอดแก้ว รับพนักงานใหม่ ชวนคนมาร่วมธุรกิจ แสวงหาโอกาสใหม่ ๆ สมัครงาน",
        "remedy": "ถ้าพบปัญหา... จงหาคนหรือสิ่งที่มีชื่อเกี่ยวกับ 'ไฟ' จะช่วยได้"
    }
