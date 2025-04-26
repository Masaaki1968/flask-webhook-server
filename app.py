
import shutil
import subprocess
import os
import sys
from flask import Flask, request

app = Flask(__name__)

# あなたのGitHubリポジトリURLに書き換えてください！
GIT_REMOTE_URL = "https://Masaaki1968:ghp_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@github.com/Masaaki1968/flask-webhook-server.git"

@app.route("/webhook", methods=["POST"])
def webhook():
    print("⭐ リクエスト受信しました！")
    sys.stdout.flush()

    try:
        # リクエストの生データを表示
        print(f"📦 Rawデータ内容: {request.data}")
        sys.stdout.flush()

        # JSONデータを取得
        data = request.get_json(force=True)

        if data is None:
            print("⚠️ JSONデータが空です。")
        else:
            print(f"✅ 受信データ: {data}")

            # データからtitle, author, bodyを取り出す
            title = data.get("title", "タイトルなし")
            author = data.get("author", "著者なし")
            body = data.get("body", "本文なし")

            # LaTeXテンプレートを作成
            latex_template = f"""
\\documentclass{{article}}
\\usepackage{{xeCJK}}
\\setCJKmainfont{{IPAexGothic}}

\\title{{{title}}}
\\author{{{author}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{body}

\\end{{document}}
"""

            # /tmpディレクトリにmain.texとして保存
            tmp_path = "/tmp/main.tex"
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(latex_template)

            print(f"✅ /tmp/main.texファイル作成完了")

            # プロジェクトフォルダにコピー
            project_root = os.path.dirname(os.path.abspath(__file__))
            destination_path = os.path.join(project_root, "main.tex")
            shutil.copy(tmp_path, destination_path)

            print(f"✅ main.texファイルをプロジェクトにコピー: {destination_path}")

            # Gitユーザー設定
            try:
                subprocess.run(["git", "config", "--global", "user.email", "yourname@example.com"], check=True)
                subprocess.run(["git", "config", "--global", "user.name", "Your Name"], check=True)
                print("✅ Gitユーザー設定完了！")
            except subprocess.CalledProcessError as e:
                print(f"❌ Gitユーザー設定エラー: {e}")

            # Gitリモート設定
            try:
                subprocess.run(["git", "remote", "add", "origin", GIT_REMOTE_URL], check=True)
                print("✅ Gitリモート(origin)を設定しました！")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Gitリモート設定エラー（たぶん既に設定済み）: {e}")

            # Git add, commit, push
            try:
                subprocess.run(["git", "add", "main.tex"], check=True)
                subprocess.run(["git", "commit", "-m", "Update main.tex from webhook"], check=True)
                subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
                print("✅ Git Push完了！Overleafに反映されます！")
            except subprocess.CalledProcessError as e:
                print(f"❌ Git操作エラー: {e}")

    except Exception as e:
        print(f"❌ 例外発生: {e}")
    finally:
        sys.stdout.flush()

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
