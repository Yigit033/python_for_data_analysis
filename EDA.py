import pandas as pd
import seaborn as sns
from datasets import load_dataset
import ast
import matplotlib.pyplot as plt

# Loading Data

dataset = load_dataset("lukebarousse/data_jobs")

df = dataset["train"].to_pandas()

"""print(df.head(5))
"""
# data cleanup

df["job_posted_date"] = pd.to_datetime(df["job_posted_date"])
df["job_skills"] = df["job_skills"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)

"""print(df["job_skills"])
"""

# Filter for US Data Analyst Role

df_DA_US = df[(df["job_country"] == "United States") & (df["job_title_short"] == "Data Analyst")]

df_plot_US= df_DA_US["job_location"].value_counts().head(10).to_frame()

"""sns.set_theme(style="ticks")
sns.barplot(data=df_plot_US, x = "count", y = "job_location", hue="count", palette="dark:b_r")
sns.despine()
plt.title("Number of jobs per Job Title in US")
plt.xlabel("Number of Data Analyst")
plt.ylabel("Cities in US ")
plt.show()"""




dict_column = {
  "job_work_from_home": "Work from home offered",
  "job_no_degree_mention": "Degree Requirement",
  "job_health_insurance": "Health Insurance Offer"
}

fig, ax = plt.subplots(1, 3)

fig.set_size_inches((12,5))


for i, (column, title) in enumerate(dict_column.items()):
  ax[i].pie(df_DA_US[column].value_counts(), labels=["False", "True"], autopct="%1.1f%%", startangle = 90)
  ax[i].set_title(title)


plt.show()




"""df_plot_US= df_DA_US["company_name"].value_counts().head(10).to_frame()

sns.set_theme(style="ticks")
sns.barplot(data=df_plot_US, x = "count", y = "company_name", hue="count", palette="dark:b_r")
sns.despine()
plt.title("Number of Companies per Job Title in US")
plt.xlabel("Number of Data Analyst")
plt.ylabel("Cities in US ")
plt.show()"""