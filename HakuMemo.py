import datetime

# メモを保存するファイルのパス
LOG_FILE = "memo_log.txt"

def log_entry(entry):
    """エントリをログファイルに記録し、最新のエントリを表示する"""
    # 現在の時間を取得
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ログをタイムスタンプ付きでファイルに書き込む
    with open(LOG_FILE, "a") as file:
        log_line = f"{current_time} - {entry}\n"
        file.write(log_line)
    
    # 新しいエントリをリアルタイムで表示
    print(log_line.strip())

def main():
    """メインのループ"""
    print("メモを入力してください。終了するには 'exit' を入力してください。")
    while True:
        # ユーザーからの入力を取得
        entry = input("> ")
        
        # 'exit' と入力されたらループを終了
        if entry.lower() == "exit":
            break
        
        # エントリを記録し、リアルタイムで表示
        log_entry(entry)

if __name__ == "__main__":
    main()
