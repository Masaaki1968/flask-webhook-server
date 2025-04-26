from flask import Flask, request
import os
import sys

app = Flask(__name__)

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
            save_path = "/tmp/main.tex"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(latex_template)

            print(f"✅ main.texファイル作成完了: {save_path}")

    except Exception as e:
        print(f"❌ 例外発生: {e}")
    finally:
        sys.stdout.flush()

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
