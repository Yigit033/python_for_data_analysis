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

"""print(df_skills[["job_skills", "job_title_short"]])
"""

df_skills_count = df_skills.groupby(["job_skills", "job_title_short"]).size()


"""print(df_skills_count)
"""

df_skills_count = df_skills_count.reset_index(name = "skill_count")

"""print(df_skills_count)"""


df_skills_count.sort_values(by="skill_count", ascending=False, inplace=True)

"""print(df_skills_count)"""


job_titles = df_skills_count["job_title_short"].unique().tolist()

"""print(job_titles)"""

job_titles = job_titles[:3]

"""print(job_titles)
"""

"""fig, ax = plt.subplots(len(job_titles), 1)
sns.set_theme(style="ticks")

for i, job_title in enumerate(job_titles):
  df_plot = df_skills_count[df_skills_count["job_title_short"] == job_title].head(5)
  df_plot.plot(kind="barh", x = "job_skills", y = "skill_count", ax= ax[i], title = job_title)
  ax[i].invert_yaxis()
  ax[i].set_ylabel("")
  ax[i].legend().set_visible(False)
  ax[i].set_xlabel("")
  ax[i].get_legend().remove()
  ax[i].set_xlim(0,45000)


fig.suptitle("Counts of Top Skills in Job Posting", fontsize=15)
fig.tight_layout(h_pad=0.5) # fix the overlap
plt.show()"""


df_total_jobs = df_Us["job_title_short"].value_counts(ascending=False).reset_index(name="total_jobs_number")
# print(df_total_jobs)




df_skill_perc =pd.merge(df_skills_count, df_total_jobs, how="left", on="job_title_short")

df_skill_perc["skill_percent"] = 100*(df_skill_perc["skill_count"]) / df_skill_perc["total_jobs_number"]

print(df_skill_perc)



fig, ax = plt.subplots(len(job_titles), 1)


for i, job_title in enumerate(job_titles):
  df_job_plot = df_skill_perc[df_skill_perc["job_title_short"] == job_title].head(5)[::-1]
  df_job_plot.plot(kind= "barh", x = "job_skills", y = "skill_percent", ax = ax[i], title = job_title)
  ax[i].invert_yaxis()
  ax[i].set_ylabel("")
  ax[i].legend().set_visible(False)
  ax[i].set_xlabel("")
  ax[i].get_legend().remove()
  ax[i].set_xlim(0,78)
  
  if i != len(job_titles) - 1:
        ax[i].set_xticks([])

  # label the percentage on the bars
  for n, v in enumerate(df_job_plot['skill_percent']):
      ax[i].text(v + 1, n, f'{v:.0f}%', va='center')


fig.suptitle("Percent of Job Skills in Job Posting", fontsize=15)
fig.tight_layout(h_pad=.8) # fix the overlap
plt.show()































































