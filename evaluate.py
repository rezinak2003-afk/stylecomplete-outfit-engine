"""Small demo smoke check; not a model-quality evaluation."""
from recommender import OutfitCompletionEngine, demo_catalog
engine = OutfitCompletionEngine(demo_catalog())
seed = demo_catalog().iloc[0]["article_id"]
print(engine.recommend(seed, top_k=5)[["name", "category", "score"]].to_string(index=False))
