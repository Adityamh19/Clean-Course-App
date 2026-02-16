import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("⏳ Loading your data...")
# Load the dataset
df = pd.read_excel('online_course_recommendation_v2 (3).xlsx')

# 1. Clean and Deduplicate
# We keep only what we need. 
course_df = df[['course_id', 'course_name', 'difficulty_level', 'course_price', 'instructor']].drop_duplicates(subset='course_id').reset_index(drop=True)

print(f"✅ Loaded {len(course_df)} unique courses.")

# 2. THE FIX: Create a "Tags" Column
# We combine the Name and Difficulty. This forces the model to match "Python" with "Python".
# We intentionally DO NOT include the instructor here to stop the bias.
course_df['tags'] = course_df['course_name'] + " " + course_df['difficulty_level']

# 3. Vectorize (Convert text to numbers)
# This counts words. If two courses both have "Python", they get a high score.
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(course_df['tags']).toarray()

# 4. Calculate Similarity
print("⏳ Calculating similarities...")
similarity = cosine_similarity(vectors)

# 5. Compress Model (Keep Top 10)
print("⏳ Compressing model...")
recommendation_dict = {}
course_ids = course_df['course_id'].values

for idx, row in enumerate(similarity):
    # Get indices of top 10 matches
    top_indices = row.argsort()[-11:-1][::-1]
    recommendation_dict[course_ids[idx]] = course_ids[top_indices]

# 6. Save Files
if not os.path.exists('models'):
    os.makedirs('models')

print("💾 Saving optimized files...")
joblib.dump(recommendation_dict, 'models/recommendation_dict.pkl')
joblib.dump(course_df, 'models/content_df.pkl')

print("🎉 DONE! Logic Fixed: Now prioritizes Course Name over Instructor.")
