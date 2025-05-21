import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import re



st.set_page_config(
    page_title="كشف النصابين",
     page_icon="logo.jpg",
    layout="centered"
)


# إعداد الاتصال بـ Google Sheet
@st.cache_resource
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    sheet_id = "1B5GhDPdkWhdyo39RLStR0o10VDQ77Wlw01DigisNRN0"
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet

sheet = connect_to_sheet()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# تصميم الواجهة بالعربية
st.markdown(
    """
    <style>
        body, .stApp {
            direction: rtl;
            text-align: right;
            font-family: 'Arial', sans-serif;
        }
        .css-1d391kg {
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    st.image("logo.jpg", width=120 )
    st.write("الموقع مدعوم بالكامل من قبل فريق UFRC")
st.markdown("لينك الجروب : https://chat.whatsapp.com/HHDi9FdBzKp09Qp27Rd9LU")
st.markdown("تبليغ عن نصاب  : https://docs.google.com/forms/d/e/1FAIpQLSe3nP9yS7Bj227inkn5JH_jxI-1PD599qbkMj1QIfLKaHe5YQ/viewform")

st.title(" البحث عن الرقم في داتا النصابين")


# حقل إدخال مخصص بالاتجاه LTR
رقم_البحث = st.text_input("أدخل الرقم الذي ترغب في البحث عنه:")


def تنظيف_الرقم(رقم):
    # حذف كل ما ليس رقماً
    return re.sub(r"\D", "", رقم)
    
n=رقم_البحث.replace(" ","")
رقم_البحث= رقم_البحث.replace("+2","")
رقم_البحث= رقم_البحث.replace("+","")
n=n.replace("+2","")
n=n.replace("+","")
if st.button("بحث"):
    if not رقم_البحث:
        st.warning("يرجى إدخال رقم أولاً.")
    else:
        البيانات = sheet.col_values(1)[1:]  
        البيانات_المنظفة = [تنظيف_الرقم(رقم) for رقم in البيانات]
        if رقم_البحث in البيانات:
            رقم_الصف = البيانات.index(رقم_البحث) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{رقم_البحث} نصاب و موجود في البيانات.")
            st.write("محتوى الصف:")
            st.table([الصف_الكامل])
        elif n in البيانات_المنظفة:
            رقم_الصف = البيانات_المنظفة.index(n) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{n} نصاب و موجود في البيانات.")
            st.write("محتوى الصف:")
            st.table([الصف_الكامل])

        elif n in البيانات:
            رقم_الصف = البيانات.index(n) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{n} نصاب و موجود في البيانات.")
            st.write("محتوى الصف:")
            st.table([الصف_الكامل])

        elif رقم_البحث in البيانات_المنظفة:
            رقم_الصف = البيانات_المنظفة.index(n) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{n} نصاب و موجود في البيانات.")
            st.write("محتوى الصف:")
            st.table([الصف_الكامل])
        
        
        else:
            st.error(f"❌ الرقم {رقم_البحث} غير موجود.")
            st.info("ممكن يكون نصاب بس لسه متسجلش في الداتا معنى كدا اننا معندناش بيانات ليه، ممكن يبقى نصاب ولسة متسجلش، وممكن يكون امان فخد احتياطاتك \n No risk No rizk")

