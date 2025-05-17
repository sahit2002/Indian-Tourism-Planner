
# Cultural Connect: Interactive Tourism Planner for India

## 📌 Project Overview
Cultural Connect is an interactive web-based tourism planner designed to promote India's diverse heritage destinations. The application is built using **Streamlit** for the frontend and **Snowflake** as the backend data warehouse. Users can explore top-rated destinations by applying filters such as travel month, state, and category. The app enhances the travel planning experience through visually rich cards powered by verified Wikipedia images and a natural language search interface.

---

## 💡 Features
- **Month, State & Category-based Filtering** for destinations.
- **Natural Language Search Interface** using TF-IDF and cosine similarity.
- **Interactive Cards** with:
  - Tourist place info
  - Google Maps links
  - High-quality Wikipedia-sourced images
- **Floating Chat-Style Input** for seamless user queries.

---

##  Tech Stack
- **Frontend**: Streamlit
- **Backend**: Snowflake Cloud Data Warehouse
- **Data Source**: Curated CSV + Wikipedia Commons (Images)
- **Search Engine**: Scikit-learn (TF-IDF + Cosine Similarity)

---

## 📊 Data Schema
Table: `TOURIST_DESTINATIONS`

| Column Name         | Type     | Description                               |
|---------------------|----------|-------------------------------------------|
| PLACE_ID            | NUMBER   | Unique place identifier                   |
| NAME                | TEXT     | Name of the destination                   |
| STATE               | TEXT     | Indian state                              |
| BEST_VISIT_MONTHS   | TEXT     | Ideal months to visit                     |
| CATEGORY            | TEXT     | Category like Monument, Temple, etc.      |
| OPENING_TIME        | TIME     | Opening time                              |
| CLOSING_TIME        | TIME     | Closing time                              |
| GOOGLE_MAPS_LINK    | TEXT     | Direct Google Maps URL                    |
| IMAGE_URL           | TEXT     | Wikipedia-hosted image URL                |
| DESCRIPTION         | TEXT     | Brief info about the location             |

---

## 🚀 How to Run

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your `secrets.toml` for Snowflake connection under `.streamlit/`:
   ```toml
   [snowflake]
   user = "your_username"
   password = "your_password"
   account = "your_account"
   warehouse = "your_warehouse"
   database = "your_database"
   schema = "your_schema"
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

---

## Future Enhancements
- Integration of live weather and cultural events data
- Multilingual user interface
- AI-based recommendation engine
- Mobile-first design improvements

---

## 👤 Author
Built by Sure Sai Venkata Krishna Sahit
