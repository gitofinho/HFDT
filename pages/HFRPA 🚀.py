import streamlit as st
import time
import numpy as np
from streamlit_timeline import timeline

st.set_page_config(page_title='HFDT-Platform' ,layout="wide",page_icon='🚀')

"## 🚀 HFRPA"
st.write("")

st.subheader('Dev Summary')

with st.spinner(text="Building line"):
    with open('timeline.json', "r", encoding='utf-8') as f:
        data = f.read()
        timeline(data, height=350)

st.write('''**Total RPA dev** 🖥️: 3''')
st.write('''**Total budget savings** 💸: 176,993,000 KRW''')
st.write('''**Total work reduction** ⏰: 106.8 hour/month''')
st.write(''':rainbow[*If you have any ideas or work related to RPA, please contact **Inho Jeong**.*]''')

st.divider()
st.subheader('RPA Cases')

class ColumnDisplay:
    def __init__(self, title, department, period, work_reduction, cost_saving, image_path, image_alt):
        self.title = title
        self.department = department
        self.period = period
        self.work_reduction = work_reduction
        self.cost_saving = cost_saving
        self.image_path = image_path
        self.image_alt = image_alt

    def display(self, column):
        with column:
            st.markdown(f"<p style='font-size:16px;'>{self.title}</p>", unsafe_allow_html=True)
            st.image(self.image_path, self.image_alt)
            st.markdown(
                f"""
                - **담당부서** : {self.department}
                - **개발기간** : {self.period}
                - **업무감소** : {self.work_reduction}
                - **예산절감** : {self.cost_saving}
                """,
                unsafe_allow_html=True
            )

# 사용 예시
col1, col2, col3 = st.columns(3)

col1_display = ColumnDisplay(
    "보증료수납대사", "주택보증부", "18영업일('23.7.24. ~ '23.8.17.)",
    "월 26.4시간", "54,088천원", "./img/test.gif", "시연 영상"
)
col1_display.display(col1)

col2_display = ColumnDisplay(
    "촉탁등기 세금신고", "유동화자산부", "17영업일('23.9.5. ~ '23.9.27.)",
    "월 63.3시간", "73,780천원", "./img/test.gif", "시연 영상"
)
col2_display.display(col2)

col3_display = ColumnDisplay(
    "SWAP 풀별 교차검증", "신탁자산부", "7영업일('23.11.15. ~ '23.11.23.)",
    "월 17.1시간", "49,125천원", "./img/test.gif", "시연 영상"
)
col3_display.display(col3)