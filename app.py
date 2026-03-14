# import streamlit as st
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score

# # عنوان التطبيق
# st.title("Waze Churn Prediction App")

# # تحميل الداتا
# df = pd.read_excel("waze_dataset.xlsx")

# st.subheader("Dataset Preview")
# st.write(df.head())

# # تنظيف البيانات
# df = df.drop(columns=["ID"], errors="ignore")
# df = df.dropna(subset=["label"])

# # تحويل label
# df["label"] = df["label"].replace({
#     "retained": 1,
#     "churned": 0
# })

# # تحويل device
# if "device" in df.columns:
#     df["device"] = df["device"].replace({
#         "Android": 0,
#         "iPhone": 1
#     })

# # تقسيم الداتا
# X = df.drop(columns=["label"])
# y = df["label"]

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# # تدريب الموديل
# model = DecisionTreeClassifier(max_depth=4)
# model.fit(X_train, y_train)

# # تقييم الموديل
# y_pred = model.predict(X_test)
# acc = accuracy_score(y_test, y_pred)

# st.subheader("Model Accuracy")
# st.write(acc)

# # واجهة التنبؤ
# st.subheader("Predict New User")

# user_input = {}

# for col in X.columns:

#     if col == "device":
#         val = st.selectbox(col, ["Android", "iPhone"])
#         val = 0 if val == "Android" else 1
#     else:
#         val = st.number_input(col, value=0.0)

#     user_input[col] = val


# if st.button("Predict"):

#     input_df = pd.DataFrame([user_input])

#     prediction = model.predict(input_df)

#     if prediction[0] == 1:
#         st.success("User will stay (Retained)")
#     else:
#         st.error("User may churn")

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Waze Churn Prediction", page_icon="🚗", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load("classifier.pkl")

model = load_model()

st.title("توقع بقاء/مغادرة مستخدمي Waze 🚗")
st.write("أدخل بيانات المستخدم لتوقع ما إذا كان سيستمر في استخدام التطبيق (Retained) أم سيغادر (Churned).")

col1, col2 = st.columns(2)

with col1:
    sessions = st.number_input("عدد الجلسات (sessions)", min_value=0, value=100)
    drives = st.number_input("عدد مرات القيادة (drives)", min_value=0, value=80)
    total_sessions = st.number_input("إجمالي الجلسات (total_sessions)", min_value=0.0, value=150.0)
    n_days_after_onboarding = st.number_input("عدد الأيام منذ التسجيل", min_value=0, value=1000)
    driven_km_drives = st.number_input("المسافة المقطوعة (كم)", min_value=0.0, value=3000.0)

with col2:
    duration_minutes_drives = st.number_input("مدة القيادة (بالدقائق)", min_value=0.0, value=1500.0)
    total_navigations_fav1 = st.number_input("الذهاب للمكان المفضل 1", min_value=0, value=50)
    total_navigations_fav2 = st.number_input("الذهاب للمكان المفضل 2", min_value=0, value=10)
    activity_days = st.number_input("أيام النشاط", min_value=0, max_value=31, value=15)
    driving_days = st.number_input("أيام القيادة", min_value=0, max_value=31, value=10)

device = st.selectbox("نوع الجهاز (Device)", ["iPhone", "Android"])

if st.button("توقع حالة المستخدم"):
    device_encoded = 1 if device == "iPhone" else 0 
    
    input_data = pd.DataFrame({
        'sessions': [sessions],
        'drives': [drives],
        'total_sessions': [total_sessions],
        'n_days_after_onboarding': [n_days_after_onboarding],
        'total_navigations_fav1': [total_navigations_fav1],
        'total_navigations_fav2': [total_navigations_fav2],
        'driven_km_drives': [driven_km_drives],
        'duration_minutes_drives': [duration_minutes_drives],
        'activity_days': [activity_days],
        'driving_days': [driving_days],
        'device': [device_encoded]
    })
    
    prediction = model.predict(input_data)
    
    st.markdown("---")
    if prediction[0] == 1 or prediction[0] == 'retained':
        st.success("🎉 النتيجة: المستخدم سيستمر في استخدام التطبيق (Retained)")
    else:
        st.error("⚠️ النتيجة: المستخدم سيغادر التطبيق (Churned)")