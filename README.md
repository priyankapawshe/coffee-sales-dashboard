# Afficionado Coffee Roasters — Sales Analysis
Afficionado Coffee Roasters — Sales Trend & Time-Based Performance Analysis

![image alt]() 

![image alt]() 


A transaction-level exploratory data analysis (EDA) of 149,116 point-of-sale records from three Afficionado Coffee Roasters store locations in New York City — Hell's Kitchen, Astoria, and Lower Manhattan — for the year 2025. The project moves store operations from intuition-based scheduling toward evidence-based decision-making by quantifying when demand occurs, what drives revenue, and how performance varies across locations and product lines.

Data Science & Analytics Internship Project — Unified Mentor


Key Results

MetricValueTotal Revenue$698,812.33Total Transactions149,116Average Order Value$4.69Peak Hour10:00 AMPeak Time PeriodMorning Rush (7–10 AM) — 45.8% of daily revenueBest-Performing StoreHell's KitchenBest-Performing CategoryCoffee (38.6% of revenue)

Headline insight: Just six hours of the ~14-hour operating day (Morning Rush + Lunch Rush) generate 63.2% of total revenue, and the three stores each contribute within a tight 32.9%–33.8% band of total revenue — indicating a consistent, replicable business model rather than one flagship location carrying the brand.


Project Structure

.
├── AFFICIONADO_COFFEE_ROASTERS.ipynb   # Main analysis notebook (all phases below)
├── Afficionado_Coffee_Roasters_Research_Paper.docx  # Full write-up: methodology, findings, recommendations
├── afficionado_coffee_cleaned_df_final.csv          # Cleaned + feature-engineered dataset (output of the notebook)
└── README.md


Methodology

The notebook is organized into seven phases:


Data Ingestion & Validation — load the raw CSV, check data types, missing values, duplicates, and logical consistency (transaction_qty > 0, unit_price > 0).
Feature Engineering — derive revenue, hour, minute, and a four-way time_period bucket (Morning Rush, Lunch Rush, Afternoon, Off Peak).
Store & Location Analysis — revenue, transaction count, and average order value per store.
Product & Category Analysis — revenue and unit volume by category, product type, and individual product.
Time-Based Trends — revenue and transaction volume by hour of day and time-of-day bucket.
Price & Quantity Insights — price distributions and high-value (top 1%) transaction analysis.
Final Summary Dashboard — consolidated business-ready summary of all key insights.


The dataset passed validation cleanly with zero missing values, duplicates, or invalid rows across all 149,116 records — no rows required removal.


Tech Stack


Python — pandas, numpy
Visualization — Plotly Express, Plotly Graph Objects, Matplotlib
Environment — Jupyter Notebook


Dataset

The raw dataset contains 11 columns: transaction_id, year, transaction_time, transaction_qty, unit_price, store_id, store_location, product_id, product_category, product_type, and product_detail.


Note: The dataset includes a time-of-day field but no full calendar-date field, which limited the analysis to hour-of-day and time-period patterns rather than day-of-week or weekly trend analysis. See the research paper (Section 7) for full details on this scope limitation.




Business Recommendations

Staffing: Concentrate peak staffing 7:00–10:00 AM; maintain moderate staffing through the flat 11 AM–6 PM plateau; taper sharply after 7 PM.
Merchandising: Prioritize Coffee and Tea inventory; promote large-size/specialty variants; feature branded merchandise near checkout.
Off-peak demand: Run targeted promotions during off-peak and late-afternoon windows to smooth the demand curve.
Data roadmap: Capture a full transaction-date field in future extracts to unlock day-of-week and weekly trend analysis.
