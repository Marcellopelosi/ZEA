import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Configuration ---
# Define the possible outcomes and their corresponding weights (probabilities)
# Probabilities must sum to 1 (or be proportional)
OUTCOMES = [None, "1", "2", "3", "4"]
WEIGHTS = [0.90, 0.025, 0.025, 0.025, 0.025] # 90% + 2.5% + 2.5% + 2.5% + 2.5% = 100%


# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app)

# Optional: Configure a temporary upload folder (though we don't save the file permanently here)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --- API Endpoint ---
@app.route('/predict', methods=['POST'])
def predict_image():
    """
    Receives an image file via POST request and returns a random prediction
    from a predefined list with specific probabilities.
    """
    # 1. Check if a file part is present in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # 2. Check if a file was actually selected and submitted
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 3. Check if the file object exists (basic check)
    if not file:
         return jsonify({"error": "File object is invalid"}), 400

    # --- File Received - Now Perform Random Selection ---
    # We don't actually need to process the image content for this task,
    # just confirm we received *a* file.

    try:
        # random.choices returns a list, so we take the first element [0]
        selected_result = random.choices(OUTCOMES, weights=WEIGHTS, k=1)[0]

        # Return the result as JSON
        return jsonify({"prediction": selected_result}), 200

    except Exception as e:
        # Catch potential errors during random selection (though unlikely here)
        app.logger.error(f"Error during random selection: {e}")
        return jsonify({"error": "Internal server error during prediction"}), 500


# --- Run the App ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
