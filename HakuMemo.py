import os
import csv
from datetime import datetime

# メモファイルのパス
MEMO_DATA_DIR = "memo_data"
MEMO_FILE_NAME = os.path.join(MEMO_DATA_DIR, "huge_memo.csv")


def initialize_memo_file():
    """ファイルが存在しない場合、ヘッダーを追加して作成する。存在する場合はヘッダーを確認し、欠けていれば追加する。"""
    
    # ディレクトリが存在しない場合は作成する
    if not os.path.exists(MEMO_DATA_DIR):
        os.makedirs(MEMO_DATA_DIR)
    
    file_exists = os.path.exists(MEMO_FILE_NAME)
    if not file_exists or os.path.getsize(MEMO_FILE_NAME) == 0:
        # ファイルがないか、サイズが0の場合は書き込みモードでヘッダーを追加
        with open(MEMO_FILE_NAME, mode="a", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Datetime", "Content"])
    else:
        # ファイルが存在する場合は読み込みモードでヘッダーを確認
        with open(MEMO_FILE_NAME, mode="r", encoding="utf-8", newline='') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            if headers != ["Datetime", "Content"]:
                # ヘッダーがない場合は書き込みモードで追加
                with open(MEMO_FILE_NAME, mode="a", encoding="utf-8", newline='') as write_file:
                    writer = csv.writer(write_file)
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
            try:
                entry_datetime = datetime.strptime(row['Datetime'], "%Y-%m-%dT%H:%M:%S.%f")
                if entry_datetime.date() == today:
                    time_str = entry_datetime.strftime("%H:%M")
                    entries.append((time_str, row['Content']))
            except (ValueError, KeyError):
                continue  # フォーマットが正しくない行やキーが存在しない場合は無視
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
    datetime_str = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
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
            break
        if user_input.strip() == "":
            continue  # 空の入力は無視
        append_entry(user_input)


if __name__ == "__main__":
    main()
