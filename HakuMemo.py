import os
import csv
from datetime import datetime, timedelta

# メモファイルのパス
MEMO_DATA_DIR = "memo_data"
MEMO_FILE_NAME = os.path.join(MEMO_DATA_DIR, "huge_memo.csv")


def initialize_memo_file():
    """メモファイルが存在しない場合、ヘッダーを追加して作成する。"""
    os.makedirs(MEMO_DATA_DIR, exist_ok=True)
    if not os.path.exists(MEMO_FILE_NAME) or os.path.getsize(MEMO_FILE_NAME) == 0:
        with open(MEMO_FILE_NAME, mode="w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Datetime", "Content"])


def clear_screen():
    """コンソール画面をクリアする"""
    os.system("cls" if os.name == "nt" else "clear")


def read_entries():
    """昨日と今日のエントリーを読み込んで返す"""
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    entries = {yesterday: [], today: []}
    with open(MEMO_FILE_NAME, mode="r", encoding="utf-8", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                entry_datetime = datetime.strptime(row['Datetime'], "%Y-%m-%dT%H:%M:%S.%f")
                entry_date = entry_datetime.date()
                time_str = entry_datetime.strftime("%H:%M")
                if entry_date in entries:
                    entries[entry_date].append((time_str, row['Content']))
            except (ValueError, KeyError):
                continue  # フォーマットが正しくない行やキーが存在しない場合は無視
    return entries[yesterday], entries[today]


def display_entries(date_entries, date_label):
    """特定の日付のエントリーを表示する"""
    if date_entries:
        print(date_label)
        for time, content in date_entries:
            print(f"{time} {content}")


def display_log(yesterday_entries, today_entries):
    """エントリーを指定の形式で表示する"""
    clear_screen()
    if yesterday_entries:
        display_entries(yesterday_entries, (datetime.now() - timedelta(days=1)).strftime("%m/%d"))
        if today_entries:
            print("")  # 日付間に改行を追加
    if today_entries:
        display_entries(today_entries, datetime.now().strftime("%m/%d"))
    print(">> ", end="", flush=True)  # プロンプトを表示


def append_entry(content):
    """新しいエントリーをCSVファイルに追加する"""
    datetime_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    with open(MEMO_FILE_NAME, mode="a", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime_str, content])


def main():
    initialize_memo_file()
    while True:
        # 昨日と今日のエントリーを読み込んで表示
        yesterday_entries, today_entries = read_entries()
        display_log(yesterday_entries, today_entries)

        # ユーザー入力を受け付け
        user_input = input()
        if user_input.lower() == 'exit':
            break
        if user_input.strip() == "":
            continue  # 空の入力は無視
        append_entry(user_input)


if __name__ == "__main__":
    main()
