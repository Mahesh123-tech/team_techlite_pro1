# Hospital Emergency Room Analytics Pipeline

An automated data engineering and analytical pipeline built around the **Hospital Emergency Dataset**. Designed to parse historical emergency department records, compute standard efficiency metrics, track clinical flow anomalies, and produce production-grade analytical charts to evaluate ER performance.

## 📈 Key Clinical Performance Metrics

The processing engine computes critical metrics to assist operational management:

* **Total ER Visits**: Overall volume of incoming patient traffic ($N$).
* **Average Wait Time**: Expected duration before patient evaluation:
    $$\overline{W} = \frac{1}{N} \sum_{i=1}^{N} W_i$$
* **Target Efficiency Window**: Percentage of incoming patients whose wait time met target metrics ($W_i \le 30 \text{ mins}$).
* **Admission Rate**: The ratio of critical case outcomes resulting in full hospital admission:
    $$\text{Admission Rate} = \left( \frac{\sum \text{Admitted Patients}}{N} \right) \times 100\%$$
* **Patient Satisfaction**: Quantified average from survey data feedback loop.

## 📁 Repository Structure

```text
hospital-er-analytics/
│
├── data/
│   └── Hospital ER_Data.csv          # Source Kaggle CSV file goes here
│
├── output/                           # Directory containing auto-generated charts
│   ├── er_summary_report.txt
│   ├── 1_wait_time_distribution.png
│   ├── 2_demographics_breakdown.png
│   ├── 3_department_referrals.png
│   └── 4_weekly_trends.png
│
├── requirements.txt                  # System package prerequisites
├── main.py                           # Structured analytics script
└── README.md                         # Documentation
