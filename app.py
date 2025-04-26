from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("⭐ リクエスト受信")  # ← 追加（確実にリクエスト到達をログ出す）
    data = request.get_json(force=True)  # ← force=True
    if data is None:
        print("⚠️ データが来ていない！")
    else:
        print(f"✅ 受信データ: {data}")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)