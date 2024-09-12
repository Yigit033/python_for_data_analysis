

import ast
import pandas as pd
import seaborn as sns
from datasets import load_dataset
import matplotlib.pyplot as plt  

# Loading Data
dataset = load_dataset('lukebarousse/data_jobs')
df = dataset['train'].to_pandas()

# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)



df_USA = df[(df["job_country"] == "United State")].dropna(subset=["salary_year_avg"])


job_titles = df_USA["job_title_short"].value_counts(ascending=False).index[:6].tolist()

df_USA_top6 = df_USA[df_USA["job_title_short"].isin(job_titles)]

job_order = df_USA_top6.groupby("job_title_short")["salary_year_avg"].median().sort_values(ascending=False).index


print(job_order)






















































