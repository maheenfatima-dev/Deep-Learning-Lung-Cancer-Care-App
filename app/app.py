# app/__init__.py

from flask import Flask, request, jsonify
from pymongo import MongoClient
from config.config import Config
from routes.user_routes import user_bp
from routes.schedule_routes import schedule_bp
import tensorflow as tf
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
from flask_cors import CORS
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
client = OpenAI()

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    # Set the GPU visible to TensorFlow
    tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
    # Limit TensorFlow to use only the GPU memory it requires
    tf.config.experimental.set_memory_growth(gpus[0], True)
    print(gpus[0])
else:
    print("No GPU found")

    
model = tf.keras.models.load_model('C:/Users/haide/OneDrive/Desktop/FYP/Backend/best.h5')



# Define a function to preprocess the image
def preprocess_image(image_file):
    img = tf.keras.preprocessing.image.load_img(image_file, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


app = Flask(__name__)

CORS(app)

# Load configuration from Config class
app.config.from_object(Config)

# Initialize MongoDB client
mongo_client = MongoClient(app.config['MONGO_URI'])

# Select database
db = mongo_client[app.config['DATABASE_NAME']]


app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(schedule_bp, url_prefix='/api')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image file and other parameters from the request
        image_file = request.files['image']
        param1 = request.form.get('param1')  # Example of getting other parameters from form data

        # Save the image temporarily
        image_path = 'temp_image.jpg'
        image_file.save(image_path)

        # Preprocess the image
        img_array = preprocess_image(image_path)

        # Make predictions
        predictions = model.predict(img_array)

        # Decode the predictions
        predicted_class = np.argmax(predictions[0])
        class_names = ['malignant', 'benign', 'normal']
        print(predicted_class)  
        # Here you might need a dictionary or mapping to convert the predicted class index to its corresponding label

        # Return the predictions along with other data
        response = {'predicted_class':class_names[predicted_class] }

        return jsonify(response)

    finally:
        # Delete the saved image
        if os.path.exists(image_path):
            os.remove(image_path)


@app.route('/chatbot',methods=['POST'])
def botanswers():
    data = request.json
    question = data.get('question')
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": """You are an specialist at the AALCAA medical firm user will ask typical questions and you need to answer them. Ques:	Can you explain how this lung cancer detection application works?

ans : The lung cancer detection application utilizes deep learning algorithms to analyze medical images, identifying patterns indicative of cancerous growths. It employs convolutional neural networks to process images and provide accurate diagnoses based on features such as shape, texture, and size of detected anomalies.

Ques:	What is the purpose of using this application for lung cancer detection?

ans : The application aims to improve early detection of lung cancer, enabling timely intervention and treatment. By accurately identifying suspicious abnormalities in medical images, it enhances the chances of successful treatment outcomes and potentially saves lives through early intervention.

Ques:	What are the symptoms of lung cancer?

ans : Common symptoms of lung cancer include persistent cough, chest pain, shortness of breath, coughing up blood, hoarseness, unexplained weight loss, fatigue, and recurrent respiratory infections. However, symptoms may vary depending on the type and stage of the cancer. Early detection is crucial for effective treatment.

Ques:	What are the risk factors for lung cancer?

ans : Major risk factors for lung cancer include smoking (both active and passive), exposure to radon gas, occupational exposure to carcinogens (like asbestos, arsenic, and diesel fumes), family history of lung cancer, previous radiation therapy to the chest, and certain genetic factors. Reducing exposure to these risks can lower the likelihood of developing lung cancer. 

Ques:	What are the different types of lung cancer?


ans : Lung cancer is broadly categorized into two main types: non-small cell lung cancer (NSCLC) and small cell lung cancer (SCLC). NSCLC includes adenocarcinoma, squamous cell carcinoma, and large cell carcinoma, while SCLC is characterized by its rapid growth and tendency to spread early. Subtypes exist within these categories.

Ques:	What are the stages of lung cancer?

ans : Lung cancer staging typically follows the TNM system: T (tumor size and extent), N (lymph node involvement), and M (metastasis). Stages range from 0 (localized cancer) to IV (advanced cancer that has spread). This classification helps determine treatment options and prognosis.


Ques:	How is lung cancer treated?
ans :  Lung cancer treatment depends on factors like cancer type, stage, and overall health. Options include surgery, chemotherapy, radiation therapy, targeted therapy, immunotherapy, or a combination. Treatment aims to remove or shrink the tumor, alleviate symptoms, and improve quality of life.


Ques:	What are my options for treatment?
ans : Your treatment options depend on factors such as cancer type, stage, overall health, and personal preferences. Options may include surgery, chemotherapy, radiation therapy, targeted therapy, immunotherapy, or participation in clinical trials. Discuss with your healthcare team to determine the most suitable approach for you.

Ques:	What lifestyle changes can reduce the risk of developing lung cancer?
ans  : Lifestyle changes that can reduce the risk of developing lung cancer include quitting smoking, avoiding exposure to secondhand smoke, minimizing exposure to carcinogens (such as asbestos and radon), maintaining a healthy diet rich in fruits and vegetables, exercising regularly, and attending regular check-ups with healthcare providers.

Ques:	What are the risks and benefits of each treatment?
ans :  The risks and benefits of each lung cancer treatment vary depending on factors such as cancer type, stage, and individual health. Generally, treatments like surgery, chemotherapy, radiation, targeted therapy, and immunotherapy carry potential side effects and varying success rates. Discussing with healthcare providers helps weigh risks against potential benefits for each option.


"""},
    {"role": "user", "content": f"{question}"}
  ]
)
    response = completion.choices[0].message.content
    print(response)
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
