import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style for clean visualization
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10, 'axes.labelsize': 12, 'axes.titlesize': 14})

class HospitalERAnalyzer:
    def __init__(self, data_path, output_dir=None):
        self.data_path = data_path
        self.df = None
        
        # If no output directory is specified, default to an 'output' folder in the same directory as main.py
        if output_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.output_dir = os.path.join(base_dir, 'output')
        else:
            self.output_dir = output_dir
            
        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_and_clean_data(self):
        """Loads dataset and performs basic pre-processing and data type handling."""
        print(f"[1/4] Loading and cleaning dataset from: {self.data_path}")
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}. Please verify it is pushed to GitHub.")
        
        self.df = pd.read_csv(self.data_path)
        
        # Parse Patient Admission Date to datetime format
        self.df['Patient Admission Date'] = pd.to_datetime(self.df['Patient Admission Date'], errors='coerce')
        
        # Feature Engineering: Extract temporal components
        self.df['Admission Year'] = self.df['Patient Admission Date'].dt.year
        self.df['Admission Month'] = self.df['Patient Admission Date'].dt.strftime('%b')
        self.df['Admission DayOfWeek'] = self.df['Patient Admission Date'].dt.day_name()
        self.df['Admission Hour'] = self.df['Patient Admission Date'].dt.hour
        
        # Feature Engineering: Age Categorization
        bins = [0, 18, 35, 50, 65, 120]
        labels = ['0-18', '19-35', '36-50', '51-65', '65+']
        self.df['Age Group'] = pd.cut(self.df['Patient Age'], bins=bins, labels=labels, right=False)
        
        # Ensure boolean formatting for Admission Flag
        if self.df['Patient Admission Flag'].dtype == object:
            self.df['Patient Admission Flag'] = self.df['Patient Admission Flag'].astype(str).str.lower().map({'true': True, 'false': False, '1': True, '0': False})
            
        print(f"Successfully loaded {len(self.df)} patient records.")

    def calculate_kpis(self):
        """Computes key performance indicators for emergency room efficiency."""
        print("[2/4] Calculating Key Performance Indicators (KPIs)...")
        
        total_visits = len(self.df)
        avg_wait_time = self.df['Patient Waittime'].mean()
        
        # % of patients seen within 30 minutes threshold
        pct_under_30 = (self.df['Patient Waittime'] <= 30).mean() * 100
        
        # Admission Rate
        admission_rate = self.df['Patient Admission Flag'].mean() * 100
        
        # Average Patient Satisfaction
        avg_satisfaction = self.df['Patient Satisfaction Score'].mean()

        kpis = {
            "Total ER Visits": f"{total_visits:,}",
            "Average Wait Time": f"{avg_wait_time:.2f} minutes",
            "Seen within 30 Mins (%)": f"{pct_under_30:.2f}%",
            "Admission Rate (%)": f"{admission_rate:.2f}%",
            "Avg Satisfaction Score (1-10)": f"{avg_satisfaction:.2f}"
        }
        
        # Save KPIs to text file
        report_path = os.path.join(self.output_dir, 'er_summary_report.txt')
        with open(report_path, 'w') as f:
            f.write("=========================================\n")
            f.write("      HOSPITAL ER DASHBOARD SUMMARY      \n")
            f.write("=========================================\n")
            for k, v in kpis.items():
                f.write(f"{k}: {v}\n")
            f.write("=========================================\n")
            
        print(f"Summary report generated successfully at: {report_path}")
        return kpis

    def generate_visualizations(self):
        """Generates clear, insights-driven visualizations for data storage."""
        print("[3/4] Generating analytical visualizations...")

        # 1. Wait Time Distribution
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df['Patient Waittime'], bins=30, kde=True, color='teal')
        plt.axvline(30, color='red', linestyle='--', label='30-Min Target Window')
        plt.title('Distribution of Emergency Room Wait Times')
        plt.xlabel('Wait Time (Minutes)')
        plt.ylabel('Patient Count')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '1_wait_time_distribution.png'))
        plt.close()

        # 2. Demographic Breakdown (Age Group & Gender)
        plt.figure(figsize=(9, 5))
        sns.countplot(data=self.df, x='Age Group', hue='Patient Gender', palette='muted')
        plt.title('ER Visit Breakdown by Age Group and Gender')
        plt.xlabel('Age Category')
        plt.ylabel('Number of Visits')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '2_demographics_breakdown.png'))
        plt.close()

        # 3. Department Referrals and Admission Rate
        plt.figure(figsize=(10, 5))
        dept_order = self.df['Department Referral'].value_counts().index
        sns.countplot(data=self.df, y='Department Referral', order=dept_order, palette='viridis')
        plt.title('Patient Volume by Referring Department')
        plt.xlabel('Number of Referrals')
        plt.ylabel('Department')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '3_department_referrals.png'))
        plt.close()

        # 4. Weekly Trends: Busiest Days
        plt.figure(figsize=(8, 5))
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        sns.countplot(data=self.df, x='Admission DayOfWeek', order=day_order, palette='ch:s=-.2,r=.6')
        plt.title('ER Patient Volume by Day of the Week')
        plt.xlabel('Day of Week')
        plt.ylabel('Number of Visits')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '4_weekly_trends.png'))
        plt.close()

        print(f"All 4 analytic charts saved to folder: '{self.output_dir}/'")

    def run_pipeline(self):
        """Executes the entire data management pipeline."""
        self.load_and_clean_data()
        kpis = self.calculate_kpis()
        
        print("\n--- ER KPI Dashboard Preview ---")
        for k, v in kpis.items():
            print(f"{k}: {v}")
        print("---------------------------------\n")
        
        self.generate_visualizations()
        print("[4/4] Pipeline completed successfully!")


if __name__ == '__main__':
    # Get the absolute folder path where main.py sits right now
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Establish dynamic, cross-platform path to the CSV file
    DATA_FILE = os.path.join(BASE_DIR, 'data', 'Hospital ER_Data.csv')
    
    # Run the automated pipeline workflow
    analyzer = HospitalERAnalyzer(data_path=DATA_FILE)
    analyzer.run_pipeline()
