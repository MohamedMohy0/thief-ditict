import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

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

st.title("🔍 البحث عن رقم داخل جدول جوجل")

رقم_البحث = st.text_input("أدخل الرقم الذي ترغب في البحث عنه:")

if st.button("بحث"):
    if not رقم_البحث:
        st.warning("يرجى إدخال رقم أولاً.")
    else:
        البيانات = sheet.col_values(1)[1:]  # تجاهل الصف الأول (العنوان)

        if رقم_البحث in البيانات:
            رقم_الصف = البيانات.index(رقم_البحث) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم {رقم_البحث} موجود في البيانات.")
            st.write("محتوى الصف:")
            st.table([الصف_الكامل])
        else:
            st.error(f"❌ الرقم {رقم_البحث} غير موجود.")
