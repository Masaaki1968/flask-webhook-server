from flask import Flask, request
import os
import sys

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("⭐ リクエスト受信しました！")
    print(f"📦 Rawデータ内容: {request.data}")
    try:
        data = request.get_json(force=True)
        print(f"✅ JSON受信データ: {data}")
    except Exception as e:
        print(f"❌ JSONパースエラー: {e}")
    sys.stdout.flush()  # 追加
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)