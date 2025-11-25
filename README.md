# 💪 LifeStyle Pro: AI-Powered Fitness & Nutrition Assistant

LifeStyle Pro is an end-to-end Data Science web application designed to help users manage their workout and nutrition goals using Machine Learning models deployed on Streamlit.

🔗 **Live Demo:** [Buraya Streamlit Linki Gelecek - Birazdan Alacağız]

## 🚀 Features

### 🔥 1. SmartBurn AI (Regression)
Predicts calories burned during a workout based on user physiology and activity details.
* **Model:** XGBoost Regressor
* **Performance:** High Accuracy on synthetic workout data.
* **Key Tech:** Feature Engineering, One-Hot Encoding, Pipeline Integration.

### 🥗 2. NutriFit AI (Classification)
Analyzes meal macros (Protein, Carbs, Fat, Sugar) to determine if a meal fits "Healthy" criteria based on custom nutritional logic.
* **Model:** Random Forest Classifier
* **Performance:** 99% Accuracy on labeled dataset.
* **Key Tech:** Class Balancing (SMOTE/Weights), Binning, Rule-Based Labeling.

### 📋 3. FitPlan AI (Recommender System)
Recommends specific exercises based on target muscle group, difficulty level, and available equipment.
* **Tech:** Content-Based Filtering & Pandas Logic.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Machine Learning:** Scikit-Learn, XGBoost, Random Forest
* **Data Processing:** Pandas, NumPy, Joblib
* **Deployment:** Streamlit Community Cloud

## 📂 Project Structure
* `app.py`: Main Streamlit application code containing the UI and logic.
* `SmartBurn_AI.ipynb`: Script used to train and save the SmartBurn XGBoost model.
* `nutriFit_AI.ipynb`: Script used to train and save the NutriFit Random Forest model.
* `requirements.txt`: List of dependencies for deployment.
* `*.pkl`: Serialized machine learning models and column transformers.

## 👨‍💻 Author
**Ihsan Taymas** - Computer Engineering Student
* [https://www.linkedin.com/in/ihsan-taymas-2aab26304/]
* [https://www.kaggle.com/hsantaymas]
