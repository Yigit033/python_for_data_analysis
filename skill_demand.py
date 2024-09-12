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


df_Us = df[df["job_country"] == "United States"]

df_skills = df_Us.explode("job_skills")

"""print(df_skills[["job_title_short","job_skills"]])
print(df_skills["job_title_short"])
print(df_skills["job_skills"])
"""

df_skills_count = df_skills.groupby(["job_skills", "job_title_short"]).size()

df_skills_count = df_skills_count.reset_index(name = "skill_count")

# print(df_skills_count)

df_skills_count.sort_values(by="skill_count", ascending=False, inplace=True)

job_titles = df_skills_count["job_title_short"].unique().tolist()

job_titles = sorted(job_titles[:3])


# print(job_titles)

"""fig, ax = plt.subplots(len(job_titles), 1)

for i, job_title in enumerate(job_titles):
  df_plot = df_skills_count[df_skills_count["job_title_short"] == job_title].head(5)
  df_plot.plot(kind="barh", x = "job_skills", y = "skill_count", ax = ax[i], title=job_title)
  ax[i].invert_yaxis()
  ax[i].set_ylabel("")
  ax[i].legend().set_visible(False)

fig.suptitle("Counts of Top Skills in Job Posting", fontsize=15)
plt.show()"""





