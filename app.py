from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("⭐ リクエスト受信しました！")
    data = request.get_json(force=True)

    # 受信データを取り出す
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

    # ファイルに書き込む
    save_path = "/tmp/main.tex"  # Renderサーバーなら/tmp/に書く
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(latex_template)

    print(f"✅ main.texファイル作成完了: {save_path}")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)

# テストコメント
