import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials


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
    sheet_id = "1pnvdIINNVru-ZaoXuzSRBCYGdo2KL4QYa_CfgrNV1f4"
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
st.title(" البحث عن الرقم في داتا النصابين")

رقم_البحث = st.text_input("أدخل الرقم الذي ترغب في البحث عنه:")
st.link_button("اضافة رقم نصاب ", url="https://docs.google.com/forms/d/e/1FAIpQLSe3nP9yS7Bj227inkn5JH_jxI-1PD599qbkMj1QIfLKaHe5YQ/viewform")

if st.button("بحث"):
    if not رقم_البحث:
        st.warning("يرجى إدخال رقم أولاً.")
    else:
        البيانات = sheet.col_values(1)[1:]  # تجاهل الصف الأول (العنوان)

        if رقم_البحث in البيانات:
            رقم_الصف = البيانات.index(رقم_البحث) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{رقم_البحث} نصاب و موجود في البيانات.")
            st.write("محتوى الصف:")
            st.table([الصف_الكامل])
        else:
            st.error(f"❌ الرقم {رقم_البحث} غير موجود.")
            st.info("ممكن يكون نصاب بس لسه متسجلش في الداتا معنى كدا اننا معندناش بيانات ليه، ممكن يبقى نصاب ولسة متسجلش، وممكن يكون امان فخد احتياطاتك")

