from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
client = OpenAI()
question = "How can I dignose ?"
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


print(completion.choices[0].message.content)