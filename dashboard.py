import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


st.set_page_config(
    page_title="Netflix Data Dashboard", page_icon="🎬", layout="wide"
)
st.markdown("""
<style>
.stApp{
background-color: #121212;
    color: white;
    text-align: center;;
}
</style>
""", unsafe_allow_html=True)




col1,col2=st.columns([1,8])
with col1:
    st.image("logo.jpg",width=100)
with col2:st.title("Netflix Movies and TV Shows Dashboard")

   
@st.cache_data
def load_data():
  df = pd.read_csv("cleaned_netflix_titles.csv")
  return df
df = load_data()

st.markdown("---")
col_a, col_b = st.columns(2)
with col_a:
  st.subheader("1. Movies vs. TV Shows")
  sns.set_theme(style="darkgrid")
  fig,ax=plt.subplots(figsize=(6, 4),facecolor="black")
  ax.set_facecolor("black")
  sns.countplot(data=df, x='type', ax=ax,palette='Set1')
  ax.set_title('Count of Movies and TV Shows on Netflix',fontsize=14,color='white')
  ax.set_xlabel('Type of Content',fontsize=12,color='white')
  ax.set_ylabel('Count',fontsize=12,color='white')
  ax.tick_params(axis="x", colors="white", labelcolor="white")
  ax.tick_params(axis="y", colors="white", labelcolor="white")
  st.pyplot(fig)

with col_b:
  fig,ax=plt.subplots(figsize=(10, 6),facecolor="black")
  ax.set_facecolor("black")
  top_countries = df['country'].value_counts().head(10).reset_index()
  top_countries.columns=["country","count"]
 
  st.subheader("2. Top 10 Countries with Most Content")
  
  sns.barplot(data=top_countries,x="count",y="country",palette="Set2",orient="h", ax=ax)
  ax.set_title('Top 10 Countries with Most Content on Netflix',fontsize=14,color='white')
  ax.set_xlabel('Number of Titles',fontsize=12,color='white')
  ax.set_ylabel('Country',fontsize=12,color='white')
  ax.tick_params(axis="x", colors="white", labelcolor="white")
  ax.tick_params(axis="y", colors="white", labelcolor="white")
  st.pyplot(fig)


st.markdown("---")
st.subheader("3. Distribution of Content Ratings")
fig,ax=plt.subplots(figsize=(12, 6),facecolor="black")
ax.set_facecolor("black")
sns.countplot(data=df,x='rating',order=df['rating'].value_counts().index,hue='rating',legend=False,palette='Set3', ax=ax)
ax.set_title('Distribution of Ratings on Netflix',fontsize=14,color='white')
ax.set_xlabel('Rating',fontsize=12,color='white')
ax.set_ylabel('Number of Titles',fontsize=12,color='white')
ax.tick_params(axis="x", colors="white", labelcolor="white")
ax.tick_params(axis="y", colors="white", labelcolor="white")
st.pyplot(fig)

st.markdown("---")
st.subheader("4. Content Added Over the Years")
df["year_added"] = pd.to_datetime(df["date_added"].str.strip()).dt.year
yearly_counts = df["year_added"].value_counts().sort_index().reset_index()
yearly_counts.columns = ["year", "count"]

fig,ax=plt.subplots(figsize=(12, 6),facecolor="black")
ax.set_facecolor("black")
sns.lineplot(data=yearly_counts,
    x="year",
    y="count",
    marker="o",
    color="red",
    linewidth=2.5,
    ax=ax
)

ax.set_title("Content Added to Netflix Over the Years", fontsize=14,color='white')
ax.set_xlabel("Year", fontsize=12,color='white')
ax.set_ylabel("Number of Titles Added", fontsize=12,color='white')
ax.tick_params(axis="x", colors="white", labelcolor="white")
ax.tick_params(axis="y", colors="white", labelcolor="white")

st.pyplot(fig)


st.markdown("---")
movies_df = df[df["type"] == "Movie"].copy()
movies_df["duration_int"] = (
    movies_df["duration"].str.replace(" min", "").astype(float)
)
st.subheader("5. Distribution of Movie Durations (Histogram)")
fig,ax=plt.subplots(figsize=(10, 6),facecolor="black")
ax.set_facecolor("black")
sns.histplot(
    movies_df["duration_int"], bins=30, kde=True, color="purple", ax=ax
)

plt.title("Distribution of Movie Durations", fontsize=14,color='white')
plt.xlabel("Duration (Minutes)", fontsize=12,color='white')
plt.ylabel("Count", fontsize=12,color='white')
plt.tick_params(axis="x", colors="white", labelcolor="white")
plt.tick_params(axis="y", colors="white", labelcolor="white")
st.pyplot(fig)

st.markdown("---")
st.subheader("6. Top 10 Actors")
cast_df = (
    df["cast"].dropna().str.split(", ").explode().reset_index(drop=True)
)
top_cast = cast_df.value_counts().head(10).reset_index()
top_cast.columns = ["actor", "count"]
fig,ax=plt.subplots(figsize=(10, 6),facecolor="black")
ax.set_facecolor="black"
sns.barplot(data=top_cast, x="count", y="actor", palette="magma",ax=ax)

ax.set_title("Top 10 Netflix Actors", fontsize=14,color="black")
ax.set_xlabel("Number of Titles", fontsize=12,color="black")
ax.set_ylabel("Actor", fontsize=12,color="black")
plt.tick_params(axis="x", colors="white", labelcolor="white")
plt.tick_params(axis="y", colors="white", labelcolor="white")
st.pyplot(fig)


st.markdown("---")
st.subheader("7. Movies VS TV Shows")
df["year_added"] = pd.to_datetime(df["date_added"].str.strip()).dt.year
time_df = df.dropna(subset=["year_added"])
yearly_type = (
    time_df.groupby(["year_added", "type"]).size().reset_index(name="count")
)

fig,ax=plt.subplots(figsize=(12, 6),facecolor="black")
ax.set_facecolor="black"

sns.lineplot(
    data=yearly_type,
    x="year_added",
    y="count",
    hue="type",
    marker="o",
    linewidth=2.5,
)

plt.title("Comparison of Movies vs. TV Shows Added Over Time", fontsize=14,color="white")
plt.xlabel("Year", fontsize=12,color="black")
plt.ylabel("Number of Titles Added", fontsize=12,color="white")
plt.tick_params(axis="x", colors="white", labelcolor="white")
plt.tick_params(axis="y", colors="white", labelcolor="white")
st.pyplot(fig)

