from datetime import datetime

# ==============================
# 현재 시간 출력 및 포맷팅 함수
# ==============================
def get_current_time():
    now = datetime.now()
    period = "오전" if now.hour < 12 else "오후"
    hour_12 = now.hour % 12 if now.hour != 0 else 12

    return f"{period} {hour_12:02d}:{now.minute:02d}"