import pandas as pd

# Load CSV data
df = pd.read_csv('20250520/midterm_scores.csv')

# Subjects to check
subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']

# Create a list to store students with 4 or more failing subjects
failing_students = []

# Iterate through each student and find failing subjects
for idx, row in df.iterrows():
    failed_subjects = [subj for subj in subjects if row[subj] < 60]
    if len(failed_subjects) >= 4:  # Check if the student has 4 or more failing subjects
        failing_students.append({
            'Name': row['Name'],
            'StudentID': row['StudentID'],
            'FailedSubjects': ', '.join(failed_subjects)
        })

# Convert the list to a DataFrame and save to CSV
failing_students_df = pd.DataFrame(failing_students)
failing_students_df.to_csv('failing_students.csv', index=False)
print("The list of students with 4 or more failing subjects has been saved to 'failing_students.csv'.")