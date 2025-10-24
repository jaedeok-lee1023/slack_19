import os
import sys
import datetime
import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2026-02-17",  # 설날
    "2026-09-25",  # 추석
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f":loudspeaker: *『평택 클러스터 에어컨 및 전등 OFF 확인』* <!channel>\n\n"

        notice_msg = (
            f"안녕하세요? 인사총무팀 총무/시설팀 입니다.\n"
            f"\n"
            f"각 층 사무실, 휴게실, 일용직 대기공간, 컬리스라운지, 락커룸 *에어컨 및 전등 off 확인 요청* 드립니다.\n\n"
            f"\n"
            f"*[확인 필요 공간]*\n"
            f">1층 / 4층 / 5층 *일용직 대기공간*\n"
            f">1층 *냉장*, *HUB* 사무실 / 2층 *교육실*, *회의실*, *탕비실*, *통합사무실*\n"
            f">4층 *냉동*, *재고관리* 사무실, *QC검품실(7번게이트)* / 5층 *건강관리실*, *K라운지*, *상온* 사무실\n"
            f">6층 *컬리스라운지*, *상용직 락커룸* , *SFA* 사무실\n\n"
            f"*[미 확인 공간]*\n"
            f">1층 *자동화설비* 사무실 (7번게이트) / 7층 *넥스트마일* 사무실 (7번게이트)\n\n"
            f"\n"
            f":alert: *<중요사항>* :alert: \n"
            f"> 전등 관련하여 사무실 내 사용자 (사람) 이 있을 경우 *전등 미 OFF 해주시면 됩니다.*\n\n"
            f"\n"
            f"본 메시지의 스레드로 OFF 여부 *사진과 같이 공유* 부탁드립니다.\n\n"
            f"\n"
            f"감사합니다.\n"
        )
 
# 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
