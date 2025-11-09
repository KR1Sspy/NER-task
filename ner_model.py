from transformers import pipeline
from collections import Counter

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")


def extract_products(text: str):
    if not text or not text.strip():
        return []

    try:
        products = []

        furniture_keywords = [
            "chair", "table", "sofa", "bed", "desk", "lamp", "mirror", "cabinet", "shelf",
            "ottoman", "bench", "stool", "dresser", "nightstand", "bookcase", "wardrobe",
            "dining", "living", "bedroom", "office", "kitchen", "bathroom", "outdoor",
            "light", "lighting", "pendant", "ceiling", "wall", "floor", "spot",
            "mattress", "pillow", "cushion", "throw", "rug", "curtain", "blind",
            "furniture", "product", "item", "collection", "series", "стол",
            "стул", "диван", "кровать", "лампа", "зеркало", "шкаф", "полка"
        ]

        text_lower = text.lower()
        for keyword in furniture_keywords:
            if keyword in text_lower:
                import re
                matches = re.findall(r'\b\w+\b', text)
                for match in matches:
                    if keyword in match.lower() and len(match) > 2:
                        products.append(match)
                        break

        if not products:
            short_text = text[:1000]
            entities = ner(short_text)

            for entity in entities:
                word = entity.get('word', '').strip()
                score = entity.get('score', 0.0)

                if len(word) > 2 and score > 0.3:
                    products.append(word)

        if not products:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if (len(line) > 10 and len(line) < 100 and
                        any(word in line.lower() for word in ["light", "lamp", "chair", "table", "sofa", "bed", "mattress"])):
                    import re
                    clean_line = re.sub(r'[^\w\s\-]', '', line)
                    if len(clean_line) > 5:
                        products.append(clean_line)
                        break

        unique_products = list(set(products))
        filtered_products = []

        for product in unique_products:
            if (len(product) > 3 and
                not product.startswith('#') and
                not product.isupper() and
                    not product.isdigit()):
                filtered_products.append(product)

        return filtered_products[:10]

    except Exception as e:
        print(f"Ошибка при извлечении товаров: {e}")
        return []

def get_most_popular(products) -> str:
    if not products:
        return ""
    return Counter(products).most_common(1)[0][0]

