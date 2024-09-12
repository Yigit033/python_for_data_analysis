import pandas as pd
import seaborn as sns
from datasets import load_dataset
import ast
import matplotlib.pyplot as plt


# Loading Data
dataset = load_dataset("lukebarousse/data_jobs")

df = dataset["train"].to_pandas()


# data cleanup
df["job_posted_date"] = pd.to_datetime(df["job_posted_date"])   
df["job_skills"] = df["job_skills"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)



df_DA_USA = df[(df["job_title_short"] == "Data Analyst") & (df["job_country"] == "United States")].copy()
# print(df_DA_USA)

df_DA_USA["job_posted_month_no"] = df_DA_USA["job_posted_date"].dt.month

df_DA_USA_exploded = df_DA_USA.explode("job_skills")

df_DA_USA_pivot = df_DA_USA_exploded.pivot_table(index="job_posted_month_no", columns="job_skills", aggfunc="size", fill_value=0)


# print(f" Exploded olan USA DataFrame: \n {df_DA_USA_exploded}")
# print(f" Pivotu yapılan DataFrame: \n {df_DA_USA_pivot}")


df_DA_USA_pivot.iloc[:, :5].plot(kind="line")

"""plt.title(" Random Job Skills published on the internet in USA")
plt.xlabel("Months")
plt.ylabel("Job Posted Count")
plt.legend()
plt.show()"""



DA_USA_total = df_DA_USA.groupby("job_posted_month_no").size()

# print(DA_USA_total)


df_DA_US_percent = df_DA_USA_pivot.iloc[:12].div(DA_USA_total/100, axis=0)

df_DA_US_percent = df_DA_US_percent.reset_index()
df_DA_US_percent["job_posted_month"] = df_DA_US_percent["job_posted_month_no"].apply(lambda x: pd.to_datetime(x, format="%m").strftime("%b"))
df_DA_US_percent = df_DA_US_percent.set_index("job_posted_month")
df_DA_US_percent = df_DA_US_percent.drop(columns="job_posted_month_no")

# print(df_DA_US_percent)





from matplotlib.ticker import PercentFormatter


df_plot = df_DA_US_percent.iloc[:, :5]
sns.lineplot(data=df_plot, dashes=False, legend="full", palette="tab10")
sns.set_theme(style="ticks")
sns.despine()


plt.title("Trending Top Skills for Data Analysis in the US")
plt.xlabel("2024")
plt.ylabel("Likehood in Job Posting")
plt.legend().remove()
plt.gca().yaxis.set_major_formatter(PercentFormatter(decimals=0))

for i in range(5):
  plt.text(11.2, df_plot.iloc[-1,1], df_plot.columns[i], color="black")

plt.show()



































