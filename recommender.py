import pandas as pd

_DEMO = [
(1001,"Relaxed cotton shirt","Tops","white","minimal","cotton","A versatile clean base layer."),
(1002,"Floral midi skirt","Skirts","floral","expressive","viscose","A statement skirt for a balanced outfit."),
(1003,"Straight denim jeans","Trousers","blue","casual","denim","An everyday wardrobe foundation."),
(1004,"Lightweight sheer overshirt","Layers","cream","layered","polyester","An airy layer for styling contrast."),
(1005,"Beaded shoulder bag","Accessories","cobalt","craft","beads","A small colour accent with texture."),
(1006,"Linen blend trousers","Trousers","sage","minimal","linen","Relaxed tailored trousers."),
(1007,"Crochet vest","Layers","ecru","craft","cotton","A tactile openwork layer."),
(1008,"Citrus printed top","Tops","yellow","expressive","cotton","A bright focal point for neutral bottoms."),
(1009,"Black midi skirt","Skirts","black","minimal","cotton","A versatile base for statement tops."),
(1010,"Fringe crossbody bag","Accessories","tan","craft","synthetic","Movement and texture in a compact accessory."),
(1011,"Soft satin slip dress","Dresses","blush","occasion","satin","A fluid one-piece for evening styling."),
(1012,"Wide sash belt","Accessories","ink","minimal","fabric","Defines the waist and changes proportions."),
(1013,"Striped knit top","Tops","navy","casual","cotton","A patterned staple for easy styling."),
(1014,"Lightweight cotton shorts","Shorts","chalk","casual","cotton","A warm-weather essential."),
(1015,"Lace-trim camisole","Tops","cream","occasion","lace","A delicate layer under shirts or jackets."),
(1016,"Sage overshirt","Layers","sage","casual","cotton","A practical third piece."),
]
COLUMNS = ["article_id","name","category","colour","style","material","description"]
def demo_catalog():
    return pd.DataFrame(_DEMO, columns=COLUMNS)

class OutfitCompletionEngine:
    def __init__(self, catalog):
        self.catalog = catalog.copy()
        for c in COLUMNS:
            if c not in self.catalog.columns:
                self.catalog[c] = ""
        self.catalog["article_id"] = self.catalog["article_id"].astype(str)
    def recommend(self, article_id, top_k=5):
        seed = self.catalog[self.catalog["article_id"] == str(article_id)]
        if seed.empty:
            seed = self.catalog[self.catalog["article_id"] == article_id]
        if seed.empty:
            return self.catalog.head(0).assign(score=[])
        seed = seed.iloc[0]
        df = self.catalog[self.catalog["article_id"].astype(str) != str(article_id)].copy()
        # Complementary category weights are simple transparent demo heuristics.
        complements = {
            "Tops": ["Skirts","Trousers","Shorts","Layers","Accessories"],
            "Skirts": ["Tops","Layers","Accessories"], "Trousers": ["Tops","Layers","Accessories"],
            "Dresses": ["Layers","Accessories"], "Layers": ["Tops","Trousers","Skirts","Dresses"],
            "Shorts": ["Tops","Layers","Accessories"], "Accessories": ["Tops","Skirts","Trousers","Dresses","Layers","Shorts"]
        }
        target = complements.get(seed["category"], [])
        def score(row):
            s = 0.35 if row["category"] in target else 0.05
            if row["colour"] != seed["colour"]: s += 0.12
            if row["style"] == seed["style"]: s += 0.15
            if row["material"] != seed["material"]: s += 0.08
            if row["category"] == seed["category"]: s -= 0.2
            return max(0, min(s, 0.95))
        df["score"] = df.apply(score, axis=1)
        return df.sort_values(["score","name"], ascending=[False, True]).head(int(top_k))
