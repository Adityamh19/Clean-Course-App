import pandas as pd
import joblib
import os
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("⏳ Loading your data...")
# Load the dataset
df = pd.read_excel('online_course_recommendation_v2 (3).xlsx')

# Clean and Deduplicate
course_df = df[['course_id', 'course_name', 'instructor', 
                'course_duration_hours', 'certification_offered', 
                'difficulty_level', 'course_price', 
                'feedback_score', 'study_material_available']].drop_duplicates(subset='course_id').reset_index(drop=True)

print(f"✅ Loaded {len(course_df)} unique courses.")

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['course_duration_hours', 'course_price', 'feedback_score']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['difficulty_level', 'certification_offered', 'study_material_available', 'instructor'])
    ]
)

print("⏳ Calculating similarities (this takes 1 minute)...")
feature_matrix = preprocessor.fit_transform(course_df)
# Calculate the heavy matrix just once in memory
similarity_matrix = cosine_similarity(feature_matrix)

# --- THE COMPRESSION STEP ---
print("⏳ Compressing model...")
recommendation_dict = {}
course_ids = course_df['course_id'].values

# For every course, keep ONLY the top 20 matches
for idx, row in enumerate(similarity_matrix):
    # Get indices of top 20 (sorted)
    top_indices = row.argsort()[-21:-1][::-1]
    # Store only the IDs
    recommendation_dict[course_ids[idx]] = course_ids[top_indices]

# Save the small files
if not os.path.exists('models'):
    os.makedirs('models')

print("💾 Saving optimized files...")
joblib.dump(recommendation_dict, 'models/recommendation_dict.pkl')
joblib.dump(course_df, 'models/content_df.pkl')

print("🎉 DONE! You now have 'recommendation_dict.pkl' (Size: ~5MB).")