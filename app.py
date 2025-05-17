import streamlit as st
import pandas as pd
import datetime
import calendar
import snowflake.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="India Tourism Planner", layout="wide")

# Initialize connection
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

conn = init_connection()

# Expand BEST_VISIT_MONTHS
def expand_months(month_str):
    if not month_str or pd.isna(month_str):
        return []
    month_str = month_str.replace("–", "-").replace("—", "-")
    parts = [m.strip() for m in month_str.split(",")]
    months = list(calendar.month_abbr)[1:]
    result = []
    for part in parts:
        if "-" in part:
            try:
                start, end = part.split("-")
                start_idx = months.index(start)
                end_idx = months.index(end)
                if start_idx <= end_idx:
                    result.extend(months[start_idx:end_idx + 1])
                else:
                    result.extend(months[start_idx:] + months[:end_idx + 1])
            except ValueError:
                continue
        elif part in months:
            result.append(part)
    return result

# Load data
@st.cache_data
def load_data():
    query = "SELECT * FROM tourist_destinations"
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        df['DESCRIPTION'] = df['DESCRIPTION'].fillna('')
        df['EXPANDED_MONTHS'] = df['BEST_VISIT_MONTHS'].apply(expand_months)
        return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Your Trip")
selected_date = st.sidebar.date_input("Select travel date", datetime.date.today())
month = selected_date.strftime("%b")
category = st.sidebar.multiselect("Select Categories", df['CATEGORY'].dropna().unique())
state = st.sidebar.multiselect("Select States", df['STATE'].dropna().unique())

# Apply filters
filtered_df = df[df['EXPANDED_MONTHS'].apply(lambda x: month in x)]
if category:
    filtered_df = filtered_df[filtered_df['CATEGORY'].isin(category)]
if state:
    filtered_df = filtered_df[filtered_df['STATE'].isin(state)]

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show header and results
st.title("🗺️ India Tourism Planner")
st.markdown("Discover India's rich cultural heritage through personalized travel suggestions.")

st.subheader("🌍 Recommended Destinations")
if filtered_df.empty:
    st.info("No matching destinations found. Adjust filters or ask a new query.")
else:
    for _, row in filtered_df.iterrows():
        with st.container():
            cols = st.columns([2, 1])
            with cols[0]:
                st.subheader(row['NAME'])
                st.write(f"**State**: {row['STATE']}")
                st.write(f"**Best Months**: {row['BEST_VISIT_MONTHS']}")
                st.write(f"**Timings**: {row['OPENING_TIME']} - {row['CLOSING_TIME']}")
                st.write(row['DESCRIPTION'])
                st.markdown(f"[Open in Google Maps]({row['GOOGLE_MAPS_LINK']})")
            with cols[1]:
                try:
                    st.image(row['IMAGE_URL'], use_container_width=True)
                except Exception:
                    st.warning(f"Image not available for {row['NAME']}")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input at bottom (native Streamlit)
prompt = st.chat_input("Ask about destinations, e.g., 'temples in Tamil Nadu'")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    if not filtered_df.empty:
        # Semantic search
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(filtered_df['DESCRIPTION'].fillna(""))
        query_vec = tfidf.transform([prompt])
        similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
        top_indices = similarity.argsort()[-5:][::-1]
        refined_df = filtered_df.iloc[top_indices]

        # Display bot response
        with st.chat_message("assistant"):
            if refined_df.empty:
                st.markdown("No destinations matched your query. Try being more specific.")
            else:
                for _, row in refined_df.iterrows():
                    st.markdown(f"**{row['NAME']}** in *{row['STATE']}* — {row['CATEGORY']} category")
                    st.write(f"{row['DESCRIPTION']}")
                    st.markdown(f"[🗺️ View Map]({row['GOOGLE_MAPS_LINK']})")

        # Save assistant response to history (optional)
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Top results for: '{prompt}'"
        })
