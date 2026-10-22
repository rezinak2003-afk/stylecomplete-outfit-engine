# StyleComplete — Outfit Completion Engine

A Streamlit portfolio prototype that recommends complementary fashion items for a selected article.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Demo data
The app includes a small illustrative demo catalogue in `recommender.py`, so it can run without external datasets. `data/demo_articles.csv` is also included. This is demo-only data, not the H&M competition dataset.

## Full dataset / evaluation
Use only data you are authorised to access. Do not commit restricted Kaggle competition data to a public repository unless its terms explicitly permit redistribution. The current demo scores are heuristic and must not be presented as validated model performance.
