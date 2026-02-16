# 📚 AI-Powered Online Course Recommendation System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)

## 🚀 Live Demo
**[Click Here to Try the App](https://clean-course-app-jtofgtbgrchtrbkzwnpgde.streamlit.app/)**

> **Note:** If the app is in "Sleep Mode", simply click **"Yes, get this app back up!"**. It runs on free cloud resources and pauses after inactivity. It will wake up in 30 seconds.

---

## 📝 Project Overview
This project is a **Content-Based Recommendation System** designed to suggest online courses to users based on their preferences. By analyzing course attributes such as **Description, Difficulty Level, Price, and Instructor**, the system identifies and recommends the most relevant alternatives to a selected course.

The goal is to solve the **"Information Overload"** problem in e-learning platforms where users struggle to choose from thousands of available courses.

---

## 🧠 Model Selection & Justification

### Selected Model: **Content-Based Filtering (Cosine Similarity)**

We chose a Content-Based approach over Collaborative Filtering for the following reasons:

1.  **No Cold-Start Problem for Items:**
    * *Collaborative Filtering* needs thousands of users to rate a new course before it can be recommended.
    * *Content-Based* can recommend a **brand new course** immediately because it looks at the course *features* (Description, Tags, Price), not user history.
2.  **User Independence:**
    * Recommendations are based on the intrinsic quality and features of the course, not influenced by the biased ratings of other users.
3.  **Transparency:**
    * It is easy to explain *why* a course was recommended (e.g., *"Because you liked 'Python for Data Science', here is 'Advanced Machine Learning' which covers similar topics"*).

---

## 📊 Performance & Metrics

Since this is an Unsupervised Learning system (Ranking/Similarity), standard "Accuracy" percentages (like 95%) do not apply directly. Instead, we evaluate using **Relevance Metrics**:

* **Precision@K (Top-5):** Measures how many of the top 5 recommended courses are actually relevant (share the same Topic/Difficulty).
* **Qualitative Analysis:**
    * *Input:* "Python for Beginners" (Price: $50, Level: Beginner)
    * *Output:* Consistently returns other Python/Coding courses within the $30-$80 range.
* **Similarity Score Threshold:** The system only returns courses with a Cosine Similarity score > 0.6 to ensure quality.

---

## 🌍 Real-Life Implementation
This engine can be integrated into EdTech platforms (like Coursera, Udemy, or internal Corporate Learning Systems) to:
1.  **Increase Engagement:** Keep users on the platform by showing relevant next steps.
2.  **Personalized Learning Paths:** Automatically suggest the next logical course after a user finishes a beginner module.
3.  **Marketing:** Send targeted emails (e.g., *"Since you enjoyed Course A, check out Course B"*).

---

## 🛠️ Challenges Faced & Solutions

During the development and deployment of this project, we encountered significant technical hurdles. Here is how we resolved them:

### 🔴 Challenge 1: The "700MB File" Crash
* **The Problem:** The Cosine Similarity Matrix for thousands of courses resulted in a `.pkl` file size of **over 700MB**. GitHub limits uploads to 100MB, and Streamlit Cloud crashed instantly upon loading.
* **The Solution:** We wrote a custom optimization script (`generate_optimized_dict.py`). Instead of saving the massive matrix of *every* course vs *every* course, we pre-calculated the **Top 20 matches** for each course and saved them in a lightweight Python dictionary.
* **Result:** File size dropped from **700MB → 5MB** (99% reduction) with zero loss in recommendation quality.

### 🔴 Challenge 2: "Works on My Machine"
* **The Problem:** The app worked locally but failed on the Cloud with `ModuleNotFoundError`.
* **The Solution:** We learned that Streamlit Cloud creates a fresh Linux environment. We fixed this by:
    1.  Creating a clean `requirements.txt` file.
    2.  Ensuring file paths were dynamic using `os.path.join` instead of hardcoded Windows paths (e.g., `C:\Users\...`).

---

## 💻 How to Run Locally

If you want to run this project on your own computer:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Adityamh19/Clean-Course-App.git](https://github.com/Adityamh19/Clean-Course-App.git)
    cd Clean-Course-App
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

---

## 📂 Project Structure
* `app.py`: The main application script for the web interface.
* `Recommend.ipynb`: Jupyter Notebook containing EDA, Feature Engineering, and Model Training logic.
* `generate_optimized_dict.py`: The script used to compress the model size.
* `models/`: Contains the optimized recommendation dictionary and course data.
* `requirements.txt`: List of dependencies required to run the app.

---

*Developed by Aditya | Powered by Streamlit*
