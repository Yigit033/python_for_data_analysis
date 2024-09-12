**Overview**

Welcome to my analysis of the data analytics job market, focusing on data analyst roles. This project was created out of a desire to navigate and understand the job market more effectively. It delves into the top-paying and in-demand skills to help find optimal job opportunities for data analysts.

The data is sourced from Luke Barousse's Python Course on YouTube, which provides the foundation for my analysis. It contains detailed information on job titles, salaries, locations, and essential skills. Through a series of Python scripts, I explore key questions such as the most demanded skills, salary trends and the intersection of demand and salary in data analytics.

**The Questions**

Below are the questions I want to answer in my project:

1. What are the skills most in demand for the top 3 most popular data roles?
2. How are in-demand skills trending for Data Analysts
3. How well do jobs and skills pay for Data Analysts?
4. What are the most optimal skills for Data Analysts to learn? (High Demand AND High Paying)

**Tools Used**

For my analysis into the Data Analyst jobs market, I harnessed the power of several key tools:

- Python: Backbone of analysis, allowing me to analyze the data and find critical insights
    - Pandas Library
    - Matplotlib Library
    - Seaborn Library
- Jupyter Notebooks: tool used to execute Python scripts
- Visual Studio Code: IDE used to store project and write Python code

**Import Libraries and Load Data Source**

```
# import libraries

import ast
import pandas as pd
import seaborn as sns
from datasets import load_dataset
import matplotlib.pyplot as plt

# loading data

dataset = load_dataset('lukebarousse/data_jobs')
df = dataset['train'].to_pandas()

# data cleanup

df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])

# use apply() to clean 'job_skills' >> makes the column a list datatype instead of string

df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else(x))
```

**The Analysis**

**1. What are the most demanded skills for the top 3 most popular data roles?**

To find the most demanded skills for the top 3 most popular data roles, I filtered out those positions by which ones were the most popular, and acquired the top 5 skills for these top 3 roles. This script highlights the most popular job titles and their top skills, showing which skills I should pay attention to depending on my taget role.

**Visualize Data**

```
fig, ax = plt.subplots(len(job_titles), 1)

sns.set_theme(style='ticks')

# iterating through

for i, job_title in enumerate(job_titles):
    df_plot = df_skills_perc[df_skills_perc['job_title_short'] == job_title].head(5)
    sns.barplot(data=df_plot, x='skill_percent', y='job_skills', ax=ax[i], hue='skill_count', palette='dark:b_r')
    ax[i].set_title(job_title)
    ax[i].set_ylabel('')
    ax[i].set_xlabel('')
    ax[i].legend().remove()
    ax[i].set_xlim(0, 78)

    # labeling graph

    for n, v in enumerate(df_plot['skill_percent']):
        ax[i].text(v + 1, n, f'{v:.0f}%', va='center')

# removing repetitive x axes
    if i != len(job_titles) - 1:
        ax[i].set_xticks([])

fig.suptitle('Likelihood of Skills Requested in US Job Postings', fontsize=15)
plt.tight_layout(h_pad=0.5) # fixes overlap
plt.show()
```

**Results**

**Insights**

- Python is a versatile skill, highly demanded across all three roles, but most prominently for Data Scientists (72%) and Data Engineers (65%).
- SQL is the most requested skill for Data Analysts and Data Scientists, found in over half of the job postings.
- Data Engineers require more specialized technical skills (AWS, Azure, Spark) compared to Data Analysts and Data Scientists, who are expected to be proficient in more general data management and analysis tools (Excel, Tableau).

**2. How are in-demand skills trending for Data Analysts?**

**Visualize Data**

```
df_plot = df_DA_US_percent.iloc[:, :5]

sns.lineplot(data=df_plot, dashes=False, palette='tab10')
sns.set_theme(style='ticks')
sns.despine()

plt.title('Trending Top Skills for Data Analysts in US')
plt.ylabel('Likelihood in Job Posting')
plt.xlabel('2023')
plt.legend().remove()

# formatting y axis as percent
from matplotlib.ticker import PercentFormatter

ax = plt.gca()
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))

#labeling each line since we removed legend
for i, col in enumerate(df_plot.columns):
    if col == 'tableau':
        plt.text(11.2, df_plot.iloc[-1, i] + 1.5, col)  # move 'tableau' label up
    elif col == 'python':
        plt.text(11.2, df_plot.iloc[-1, i] - 1.5, col)  # move 'python' label down
    else:
        plt.text(11.2, df_plot.iloc[-1, i], col)

plt.show()
```

*Line graph visualizing the top trending skills for data analysts in the US in 2023*


**Insights:**

- SQL remains the most consistently demanded skill throughout the year, followed by Excel as the second most in demand.
- Both Python and Tableau show relatively stable demand throughout the year but remain essenential skills for data analysts.

**How well do jobs and skills pay for Data Analysts?**

**Salary Analysis for Data Jobs**

**Visualize Data**

```
# box plot code

from matplotlib.ticker import FuncFormatter

sns.boxplot(df_US_top6, x='salary_year_avg', y='job_title_short', order=job_order)
sns.set_theme(style='ticks')

plt.title('Salary Distribution in the United States')
plt.xlabel('Yearly Salary (USD)')
plt.ylabel('')
plt.xlim(0, 600000)
ticks_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
plt.gca().xaxis.set_major_formatter(ticks_x)
plt.show()
```

**Results**

*Box plot visualizing the salary distributions for the top 6 data job titles.*


**Insights:**

- There is a significant variation in salary ranges across different job titles. Senior Data Scientist positions tend to have the highest salary potential, reaching up to $600K, highlighting the high value placed on advanced data and mathematical skills, as well as industry experience.
- Senior Data Engineer and Senior Data Scientist roles exhibit a significant number of high-end salary outliers, suggesting that exceptional skills or circumstances can lead to substantial pay in these positions. In contrast, Data Analyst roles show more consistency in salary, with fewer outliers.
- The median salaries increase with the seniority and specialization of the roles. As responsibilities increase, there is a greater variance in compensation.

**Highest Paid and Most Demanded Skills for Data Analysts**

**Visualize Data**

```
fig, ax = plt.subplots(2, 1)

sns.set_theme(style='ticks')

#df_DA_top_pay[::-1].plot(kind='barh', y='median', ax=ax[0], legend=False)

sns.barplot(data=df_DA_top_pay, x='median', y=df_DA_top_pay.index, ax=ax[0], hue='median', palette='dark:b_r')
ax[0].legend().remove()

ax[0].set_title('Top 10 Highest Paid Skills for Data Analysts')
ax[0].set_ylabel('')
ax[0].set_xlabel('')
ax[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'${int(x/1000)}K'))

sns.barplot(data=df_DA_skills, x='median', y=df_DA_skills.index, ax=ax[1], hue='median', palette='light:b')
ax[1].legend().remove()

ax[1].set_title('Top 10 Most In-Demand Skills for Data Analysts')
ax[1].set_ylabel('')
ax[1].set_xlabel('Median Salary (USD)')
ax[1].set_xlim(ax[0].get_xlim())
ax[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'${int(x/1000)}K'))

fig.tight_layout()
```

*Two separate bar graphs visualizing the highest paid skills and most in-demand skills for data analysts in the US.*


**Insights:**

- The top graph reveals that specialized technical skills like `dplyr`, `BitBucket`, and `GitLab` are linked to higher salaries, with some reaching up to $200K.
- The bottom graph highlights that foundational skills like `Excel`, `PowerPoint`, and `SQL` are the most in-demand, even though they may not offer the highest salaries. This underscores the importance of these core skills for employability in data analysis roles.

**4. What is the most optimal skill to learn for Data Analysts?**

**Visualize Data**

```
# recreating plot

from adjustText import adjust_text
from matplotlib.ticker import PercentFormatter

# df_plot.plot(kind='scatter', x='skill_percent', y='median_salary')

sns.scatterplot(
    data=df_plot,
    x='skill_percent',
    y='median_salary',
    hue='technology'
)

sns.despine()
sns.set_theme(style='ticks')

texts = []
for i, txt in enumerate(df_DA_skills_high_demand.index):
    texts.append(plt.text(df_DA_skills_high_demand['skill_percent'].iloc[i], df_DA_skills_high_demand['median_salary'].iloc[i], txt))

adjust_text(texts, arrowprops=dict(arrowstyle='->', color ='gray', lw=1))

# adjusting axis
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K'))
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))

plt.xlabel('Percent of Data Analyst Jobs')
plt.ylabel('Median Yearly Salary ($USD)')
plt.title('Most Optimal Skills for Data Analysts in the US')

plt.tight_layout()
plt.show()
```

*A scatter plot visualizing the most optimal skills (along with annual salaries and frequency in job postings) for Data Analysts*


**Insights:**

- The scatter plot reveals that most `programming` skills (colored blue) tend to cluster at higher salary levels compared to other categories, suggesting that programming expertise may offer greater salary benefits within the data analytics field.
- Analyst tools (colored green), including Tableau and Power BI, are prevelant in job postings and offer competitive salaries, illustrating that visualization is crucial for current data analyst roles.

**Conclusion**

After this introductory exploration into the data science job market, I've learned what skills and trends are shaping this evolving field. The insights gained by analyzing the data and creating visualizations offer actionable insights for those seeking to break into the data science ecosystem, as well as existing data analysts who want to improve their skills. It is well known that Excel and SQL are the fundamental attributes for any data analyst. Based off the insights in this project, I would recommend learning Python and a BI tool such as Tableau to those who want to take their skills (and salary) to the next level.
