from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from model import analyze_number, is_prime, is_perfect
import statistics

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        numbers = data.get('numbers', [])
        
        if not numbers:
            return jsonify({"error": "No numbers provided"}), 400
        
        results = [analyze_number(n) for n in numbers]
        
        mean_val = statistics.mean(numbers)
        median_val = statistics.median(numbers)
        mode_list = statistics.multimode(numbers)
        mode_display = ", ".join(str(m) for m in mode_list)
        
        stats_summary = {
            "total": len(numbers),
            "mean": round(mean_val, 2),
            "median": round(median_val, 2),
            "modes": mode_display
        }
        
        return jsonify({
            "results": results,
            "statistics": stats_summary
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save-report', methods=['POST'])
def save_report():
    try:
        data = request.get_json()
        results = data.get('results', [])
        statistics_data = data.get('statistics', {})
        filename = data.get('filename', 'number_analysis_report.txt')
        
        default_dir = "reports"
        os.makedirs(default_dir, exist_ok=True)
        
        filename = os.path.basename(filename)
        if not filename.lower().endswith('.txt'):
            filename += '.txt'
        
        full_path = os.path.join(default_dir, filename)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("NUMBER ANALYZER PRO+ REPORT\n\n")
            if results:
                for r in results:
                    f.write(f"{r['Number']}   {r['Even/Odd']} | Prime: {r['Prime']} | Perfect: {r['Perfect']} | {r['Positive/Negative']}\n")
            else:
                f.write("No numbers were entered.\n")
            
            if statistics_data:
                f.write("\n=== STATISTICS SUMMARY ===\n")
                f.write(f"Total: {statistics_data.get('total', 0)}\n")
                f.write(f"Mean: {statistics_data.get('mean', 0):.2f}\n")
                f.write(f"Median: {statistics_data.get('median', 0):.2f}\n")
                f.write(f"Mode(s): {statistics_data.get('modes', 'N/A')}\n")
        
        return jsonify({
            "message": "Report saved successfully",
            "filepath": full_path
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download-report/<filename>', methods=['GET'])
def download_report(filename):
    try:
        default_dir = "reports"
        filename = os.path.basename(filename)
        full_path = os.path.join(default_dir, filename)
        
        if os.path.exists(full_path):
            return send_file(full_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)