import os
import csv
from datetime import datetime

# メモファイルのパス
MEMO_FILE_NAME = "huge_memo.csv"


def initialize_memo_file():
    """ファイルが存在しない場合、ヘッダーを追加して作成する"""
    if not os.path.exists(MEMO_FILE_NAME):
        with open(MEMO_FILE_NAME, mode="w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Datetime", "Content"])


def clear_screen():
    """コンソール画面をクリアする"""
    os.system("cls" if os.name == "nt" else "clear")


def read_today_entries():
    """今日のエントリーを読み込んで返す"""
    today = datetime.now().date()
    entries = []
    with open(MEMO_FILE_NAME, mode="r", encoding="utf-8", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            entry_datetime = datetime.strptime(row['Datetime'], "%Y-%m-%d %H:%M")
            if entry_datetime.date() == today:
                time_str = entry_datetime.strftime("%H:%M")
                entries.append((time_str, row['Content']))
    return entries


def display_log(entries):
    """エントリーを指定の形式で表示する"""
    clear_screen()
    today_str = datetime.now().strftime("%m/%d")
    print(today_str)
    for time, content in entries:
        print(f"{time} {content}")
    print(">> ", end="", flush=True)  # プロンプトを表示


def append_entry(content):
    """新しいエントリーをCSVファイルに追加する"""
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M")
    with open(MEMO_FILE_NAME, mode="a", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime_str, content])


def main():
    initialize_memo_file()
    while True:
        # 今日のエントリーを読み込んで表示
        today_entries = read_today_entries()
        display_log(today_entries)

        # ユーザー入力を受け付け
        user_input = input()
        if user_input.lower() == 'exit':
            print("\nメモの記録を終了します。")
            break
        if user_input.strip() == "":
            continue  # 空の入力は無視
        append_entry(user_input)
        # エントリー追加後、自動的に再ループして再表示される


if __name__ == "__main__":
    main()
