import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    data = pd.read_csv(file_path)
    return data

# Preprocess the dataset
def preprocess_data(data):
    # Convert date columns to datetime format
    if 'OPEN_DATE' in data.columns:
        data['OPEN_DATE'] = pd.to_datetime(data['OPEN_DATE'], errors='coerce', dayfirst=True)
    if 'CLOSE_DATE' in data.columns:
        data['CLOSE_DATE'] = pd.to_datetime(data['CLOSE_DATE'], errors='coerce', dayfirst=True)

    # Calculate complaint duration in days
    if 'OPEN_DATE' in data.columns and 'CLOSE_DATE' in data.columns:
        data['DURATION_DAYS'] = (data['CLOSE_DATE'] - data['OPEN_DATE']).dt.days.fillna(0)

    # Fill missing values in categorical columns with "Unknown"
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].fillna("Unknown")

    return data

# Perform trend analysis
def analyze_trends(data):
    # Trend 1: Number of complaints over time
    if 'OPEN_DATE' in data.columns:
        complaints_over_time = data.groupby(data['OPEN_DATE'].dt.to_period('M')).size()
        complaints_over_time.plot(kind='line', figsize=(10, 6), title='Number of Complaints Over Time', xlabel='Month', ylabel='Number of Complaints')
        plt.show()

    # Trend 2: Average resolution time by month
    if 'OPEN_DATE' in data.columns and 'DURATION_DAYS' in data.columns:
        avg_resolution_time = data.groupby(data['OPEN_DATE'].dt.to_period('M'))['DURATION_DAYS'].mean()
        avg_resolution_time.plot(kind='bar', figsize=(10, 6), title='Average Resolution Time by Month', xlabel='Month', ylabel='Average Resolution Time (days)')
        plt.show()

    # Trend 3: Complaints by type
    if 'COMPLAINT_TYPE' in data.columns:
        complaint_type_distribution = data['COMPLAINT_TYPE'].value_counts()
        complaint_type_distribution.plot(kind='bar', figsize=(10, 6), title='Complaint Type Distribution', xlabel='Complaint Type', ylabel='Count')
        plt.show()

# Placeholder function for insights generation (suggestions can be created with Copilot as you code)

def generate_insights(data):
    # Example actionable insights based on the analysis of the dataset

    # Assuming we have trends calculated already:
    complaints_over_time = data.groupby(data['OPEN_DATE'].dt.to_period('M')).size()
    avg_resolution_time = data.groupby(data['OPEN_DATE'].dt.to_period('M'))['DURATION_DAYS'].mean()
    complaint_type_distribution = data['COMPLAINT_TYPE'].value_counts()

    # Actionable Insights Generation (Copilot can suggest text here)
    insights = []

    # Insight 1: Trends in complaint volume over time
    if len(complaints_over_time) > 0:
        max_complaints_month = complaints_over_time.idxmax()
        insights.append(f"Complaints peaked in {max_complaints_month}. Consider investigating external factors contributing to this surge.")

    # Insight 2: Resolution time trends
    if len(avg_resolution_time) > 0:
        highest_resolution_time = avg_resolution_time.idxmax()
        insights.append(f"Resolution times were longest in {highest_resolution_time}. Explore ways to expedite case resolution during this period.")

    # Insight 3: Complaint type distribution
    if len(complaint_type_distribution) > 0:
        most_common_complaint = complaint_type_distribution.idxmax()
        insights.append(f"The most frequent complaint type is '{most_common_complaint}'. Targeting this area could lead to significant improvements in customer satisfaction.")

    # Combine insights into a final report
    print("Actionable Insights:")
    for insight in insights:
        print(f"- {insight}")


# Main function
def main(file_path):
    # Step 1: Load and preprocess data
    data = load_data(file_path)
    data = preprocess_data(data)

    # Step 2: Perform trend analysis
    analyze_trends(data)

    # Step 3: Generate actionable insights (manual for now, Copilot can assist here)
    generate_insights(data)

if __name__ == "__main__":
    file_path = r"C:\Users\techt\Downloads\Telecom-Complaint-Classification-main\Telecom-Complaint-Classification-main\env\Complaints.csv"  # Use raw string for Windows path
    try:
        main(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")