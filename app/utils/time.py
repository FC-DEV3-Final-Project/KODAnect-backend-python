from datetime import datetime


# 현재 시간 출력 및 포맷팅(ex. 오후 04:17)
def get_current_time():
    now = datetime.now()
    period = "오전" if now.hour < 12 else "오후"  # 오전/오후
    hour_12 = now.hour % 12 if now.hour != 0 else 12  # 12시간제로 변경

    return f"{period} {hour_12:02d}:{now.minute:02d}"
