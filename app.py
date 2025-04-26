from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("⭐ リクエスト受信しました！")  # まず絶対出す
    print(f"📦 Rawデータ内容: {request.data}")  # 本当のRAWデータを見る
    try:
        data = request.get_json(force=True)
        print(f"✅ JSON受信データ: {data}")
    except Exception as e:
        print(f"❌ JSONパースエラー: {e}")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)