from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

np.random.seed(43)

X_train = np.random.rand(1000, 4)

X_train[:, 0] = X_train[:, 0] * 50 + 20
X_train[:, 1] = X_train[:, 1] * 60 + 50
X_train[:, 2] = X_train[:, 2] * 90 + 70
X_train[:, 3] = X_train[:, 3] * 50 + 10

y_train = ((X_train[:, 0] * 0.2017) + (X_train[:, 1] * 0.09063) + (X_train[:, 2] * 0.6309) - 55.0969) * (X_train[:, 3] / 4.184)

ml_model = RandomForestRegressor(n_estimators=100, random_state=43)
ml_model.fit(X_train, y_train)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data instead of form data
        data = request.get_json()
        
        age = float(data['age'])
        weight = float(data['weight'])
        heart_rate = float(data['heart_rate'])
        duration = float(data['duration'])

        user_features = np.array([[age, weight, heart_rate, duration]])
        predicted_calories = ml_model.predict(user_features)[0]
        predicted_calories = max(0, predicted_calories)

        # Return JSON response
        return jsonify({
            'calories': round(predicted_calories),
            'success': True
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug info in terminal
        return jsonify({
            'error': 'Invalid input. Please enter valid numbers.',
            'success': False
        }), 400

    
if __name__ == '__main__':
    app.run(debug=True)