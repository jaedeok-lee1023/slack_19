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
    "2025-10-06",  # 추석
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
            f"각 층 사무실, 휴게실, 일용직 대기공간 *에어컨 및 전등 off 확인 요청* 드립니다.\n"
            f"\n"
            f"\n"
            f"\n"
            f"본 메시지의 스레드로 OFF 여부 *사진과 같이 공유* 부탁드립니다.\n\n"
            f"\n"
            f"*[스레드 공유 예시]*\n"
            f">1층 일용직 대기실, HUB / 냉장 사무실 에어컨 및 전등 OFF 완료\n"
            f"\n"
            f"\n"
            f"감사합니다.\n"
            f"\n"
        )
 
# 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
