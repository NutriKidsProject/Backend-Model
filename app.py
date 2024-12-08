import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path file CSV
CSV_FILE = "food-data.csv"

# Membaca file CSV
try:
    df = pd.read_csv(CSV_FILE)
    print("Dataset berhasil dimuat.")
except FileNotFoundError:
    print(f"Error: File {CSV_FILE} tidak ditemukan.")
    exit()

# Path untuk model dan file data
MODEL_PATH = 'model_nutrition_stat.h5'
DATA_FILE = 'data.json'

# Load model TensorFlow
model = tf.keras.models.load_model(MODEL_PATH)

# Load atau inisialisasi data.json
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)  # Inisialisasi file dengan array kosong
else:
    with open(DATA_FILE, 'r') as f:
        try:
            data_store = json.load(f)
        except json.JSONDecodeError:
            data_store = []

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Ambil data dari request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "Input JSON tidak ditemukan atau salah format."}), 400
        
        # Validasi parameter input
        required_keys = ["tb", "bb", "usia", "jenis_kelamin"]
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            return jsonify({
                "error": "Data input tidak lengkap.",
                "missing_keys": missing_keys,
                "message": "Harap lengkapi data: tb (tinggi badan), bb (berat badan), jenis_kelamin, dan usia."
            }), 400

        tb = data["tb"]
        bb = data["bb"]
        usia = data["usia"]
        jenis_kelamin = data["jenis_kelamin"]

        # Validasi tipe data
        if not isinstance(tb, (int, float)) or not isinstance(bb, (int, float)):
            return jsonify({"error": "tb dan bb harus berupa angka."}), 400
        if not isinstance(usia, (int, float)) or usia <= 0:
            return jsonify({"error": "usia harus berupa angka positif."}), 400
        if jenis_kelamin not in ["Laki-laki", "Perempuan"]:
            return jsonify({"error": "jenis_kelamin harus diisi dengan 'Laki-laki' atau 'Perempuan'."}), 400

        # Preprocessing input data
        gender = 1 if jenis_kelamin == "Laki-laki" else 0  # Encode gender
        input_features = np.array([[tb / 100, bb, usia]])
        reshaped_input = input_features.reshape(1, 1, 3)

        # Prediksi dengan model
        predictions = model.predict(reshaped_input)
        predicted_index = np.argmax(predictions)  # Ambil index dengan probabilitas tertinggi
        confidence_score = float(predictions[0][predicted_index])  # Probabilitas prediksi
        labels = ["Gizi Baik", "Gizi Kurang", "Gizi Lebih"]  # Label kategori
        prediction_label = labels[predicted_index]

        # Ambil rekomendasi makanan berdasarkan hasil prediksi
        recommendations = get_food_recommendations(prediction_label, n=5)

        # Penjelasan hasil prediksi
        descriptions = {
            "Gizi Baik": "Anak memiliki berat badan yang sesuai dengan tinggi badan dan usianya. Untuk menjaga status gizi yang baik, kami merekomendasikan makanan dengan kandungan nutrisi seimbang yang mendukung pertumbuhan optimal serta menjaga energi dan kesehatan tubuh.",
            "Gizi Kurang": "Anak memiliki berat badan yang kurang dibandingkan tinggi badan dan usianya. Untuk membantu mencapai status gizi yang baik, kami merekomendasikan makanan dengan kandungan kalori dan protein tinggi untuk mendukung pertumbuhan berat badan dan energi tubuh.",
            "Gizi Lebih": "Anak memiliki berat badan yang lebih dibandingkan tinggi badan dan usianya. Untuk membantu mencapai status gizi yang baik, kami merekomendasikan makanan rendah kalori, tinggi serat, dan rendah lemak untuk mengontrol berat badan tanpa mengorbankan kebutuhan nutrisi tubuh."
        }

        # Simpan data ke data.json
        new_entry = {
            "id": len(data_store) + 1,
            "tb": tb,
            "bb": bb,
            "usia": usia,
            "jenis_kelamin": jenis_kelamin,
            "prediction": prediction_label,
            "description": descriptions[prediction_label],
            "recommendations": recommendations,
            "confidence": confidence_score
        }
        data_store.append(new_entry)
        with open(DATA_FILE, 'w') as f:
            json.dump(data_store, f, indent=4)

        # Respons
        return jsonify({
            "prediction": prediction_label,
            "confidence": confidence_score,
            "description": descriptions[prediction_label],
            "recommendations": recommendations,
        }), 200

    except Exception as e:
        # Tangani error lainnya
        return jsonify({
            "message": "Terjadi kesalahan dalam prediksi.",
            "error": str(e)
        }), 500

@app.route("/recommendations", methods=["GET"])
def food_recommendations():
    """
    Endpoint untuk memberikan rekomendasi makanan berdasarkan hasil prediksi gizi.
    Query Parameters:
        category (str): Kategori gizi (e.g., "Gizi Baik", "Gizi Kurang", "Gizi Lebih")
        n (int): Jumlah rekomendasi makanan yang diinginkan (default: 5)
    """
    category = request.args.get("category")
    n = int(request.args.get("n", 5))

    # Validasi input kategori
    if category not in ["Gizi Baik", "Gizi Kurang", "Gizi Lebih"]:
        return jsonify({"error": "Kategori tidak valid. Gunakan 'Gizi Baik', 'Gizi Kurang', atau 'Gizi Lebih'."}), 400

    # Ambil rekomendasi makanan
    recommendations = get_food_recommendations(category, n=n)
    if not recommendations:
        return jsonify({"message": f"Tidak ditemukan makanan untuk kategori '{category}'."}), 404

    return jsonify({
        "category": category,
        "recommendations": recommendations
    }), 200

# Fungsi untuk mendapatkan rekomendasi makanan berdasarkan kategori gizi
def get_food_recommendations(category, n=5):
    """
    Mengambil rekomendasi makanan berdasarkan kategori gizi.
    Args:
        category (str): Kategori gizi (e.g., "Gizi Baik", "Gizi Kurang", "Gizi Lebih")
        n (int): Jumlah rekomendasi yang ingin diambil (default: 5)
    Returns:
        list: Daftar rekomendasi makanan.
    """
    if category == "Gizi Baik":
        # Filter makanan dengan kalori moderat dan protein mencukupi
        filtered_data = df[(df["Caloric Value"] > 50) & (df["Caloric Value"] < 200) & (df["Protein"] > 5)]
    elif category == "Gizi Kurang":
        # Filter makanan dengan kalori dan protein tinggi
        filtered_data = df[(df["Caloric Value"] >= 200) & (df["Protein"] > 10)]
    elif category == "Gizi Lebih":
        # Filter makanan dengan kalori rendah dan lemak rendah
        filtered_data = df[(df["Caloric Value"] < 50) & (df["Fat"] < 5)]
    else:
        # Jika kategori tidak valid, kembalikan daftar kosong
        return []

    # Pilih n rekomendasi secara acak
    if filtered_data.empty:
        return []
    return filtered_data.sample(min(n, len(filtered_data)))[["food", "Caloric Value", "Protein"]].to_dict(orient="records")

@app.route("/data", methods=["GET"])
def get_data():
    """Mengambil semua data yang telah disimpan."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data), 200

@app.route("/data/<int:id>", methods=["GET"])
def get_data_by_id(id):
    """Mengambil data berdasarkan ID."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    result = next((item for item in data if item["id"] == id), None)
    if result:
        return jsonify(result), 200
    return jsonify({"error": "Data tidak ditemukan untuk ID tersebut."}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
