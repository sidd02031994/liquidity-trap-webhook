from flask import Flask, request, send_file
import csv
import os

app = Flask(__name__)
CSV_FILE = "liquidity_trap_dataset.csv"

# ──────────────────────────────────────────────────────────────
# 1) Create the CSV (with headers) if it doesn't exist
# ──────────────────────────────────────────────────────────────
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "symbol", "timestamp", "trap_type", "open", "high", "low", "close",
            "volume", "avg_vol20", "relative_vol", "ema50", "ema200",
            "body_pct", "wick_pct", "session_code"
        ])

# ──────────────────────────────────────────────────────────────
# 2) Webhook endpoint (TradingView posts JSON here)
# ──────────────────────────────────────────────────────────────
@app.route("/", methods=["POST"])
def log_trap():
    data = request.get_json()
    if data:
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                data.get("sym"), data.get("ts"), data.get("type"),
                data.get("o"),  data.get("h"),  data.get("l"),  data.get("c"),
                data.get("v"),  data.get("av20"), data.get("rv"),
                data.get("ema50"), data.get("ema200"),
                data.get("body"), data.get("wick"), data.get("sess")
            ])
    return {"status": "ok"}, 200

# ──────────────────────────────────────────────────────────────
# 3) NEW: Download endpoint → GET /download
# ──────────────────────────────────────────────────────────────
@app.route("/download", methods=["GET"])
def download_csv():
    # If the file is empty or missing, return 404
    if not os.path.exists(CSV_FILE):
        return {"error": "CSV not found"}, 404
    return send_file(CSV_FILE, as_attachment=True)

# ──────────────────────────────────────────────────────────────
# 4) Run the server
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
