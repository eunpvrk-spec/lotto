import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="로또 번호 생성기", page_icon="🎱", layout="centered")


# 로또 번호 색상 반환 함수
def get_ball_color(number):
    if number <= 10:
        return "#fbc400", "#000000"  # 노란색 (글자색: 검정)
    elif number <= 20:
        return "#69c2f0", "#ffffff"  # 파란색 (글자색: 하양)
    elif number <= 30:
        return "#ff7272", "#ffffff"  # 빨간색 (글자색: 하양)
    elif number <= 40:
        return "#aaa", "#ffffff"  # 회색 (글자색: 하양)
    else:
        return "#b0d840", "#ffffff"  # 초록색 (글자색: 하양)


# 로또 공 HTML 생성 함수
def render_lotto_ball(number):
    bg_color, text_color = get_ball_color(number)
    return f"""
    <div style="
        display: inline-block;
        width: 45px;
        height: 45px;
        line-height: 45px;
        border-radius: 50%;
        background-color: {bg_color};
        color: {text_color};
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        margin: 4px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    ">
        {number}
    </div>
    """


# 세션 상태 초기화 (번호 세트 저장용)
if "lotto_history" not in st.session_state:
    st.session_state.lotto_history = []

# 제목 UI
st.title("🎱 로또 번호 생성기")
st.caption("최대 5개의 번호 세트까지 추출 및 저장됩니다.")

# 버튼 및 초기화 영역
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🎲 로또번호 생성", use_container_width=True):
        # 1~45 사이 중복 없는 6개 숫자추출 후 정렬
        new_numbers = sorted(random.sample(range(1, 46), 6))

        # 세션에 번호 저장 (최대 5개 유지)
        st.session_state.lotto_history.append(new_numbers)
        if len(st.session_state.lotto_history) > 5:
            st.session_state.lotto_history.pop(0)

with col2:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.lotto_history = []
        st.rerun()

st.markdown("---")

# 번호 출력 영역
if st.session_state.lotto_history:
    st.subheader("추출된 로또 번호")

    for idx, numbers in enumerate(reversed(st.session_state.lotto_history), 1):
        # 실제 보여질 순서 계산 (가장 최신 생성 건이 상단에 배치)
        set_num = len(st.session_state.lotto_history) - idx + 1

        # 공 번호들을 HTML로 묶어 표현
        balls_html = "".join([render_lotto_ball(num) for num in numbers])

        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                background-color: #f9f9f9;
                padding: 10px 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                border: 1px solid #eee;
            ">
                <span style="font-weight: bold; margin-right: 15px; min-width: 60px; color: #555;">
                    {set_num}회차
                </span>
                <div>{balls_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info(
        "아직 생성된 번호가 없습니다. [로또번호 생성] 버튼을 눌러주세요."
    )
