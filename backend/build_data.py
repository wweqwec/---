#!/usr/bin/env python3
import json

# 7大品牌各6款产品
brands = {
    "Apple": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14"],
    "Huawei": ["Mate 60 Pro", "Mate 60", "Mate 50 Pro", "Mate 50", "P60 Pro", "P60"],
    "Xiaomi": ["小米14 Pro", "小米14", "小米13 Pro", "小米13", "小米12S Pro", "小米12S"],
    "Samsung": ["Galaxy S24 Ultra", "Galaxy S24", "Galaxy S23 Ultra", "Galaxy S23", "Galaxy S22 Ultra", "Galaxy S22"],
    "Oppo": ["Find X7 Ultra", "Find X7", "Find X6 Pro", "Find X6", "Find X5 Pro", "Find X5"],
    "Vivo": ["X100 Pro", "X100", "X90 Pro+", "X90 Pro", "X80 Pro", "X80"],
    "Honor": ["Magic 6 Pro", "Magic 6", "Magic 5 Pro", "Magic 5", "Magic 4 Pro", "Magic 4"]
}

# 生成评价
def make_reviews(product_name, brand, pid):
    reviews = []
    for i in range(1, 11):
        score = 4 if i <= 6 else (3 if i <= 9 else 2)
        sentiment = "positive" if score >= 4 else ("neutral" if score == 3 else "negative")
        content = f"{product_name}评价内容{i}，包含真实用户体验和感受。"
        reviews.append({
            "id": pid * 100 + i,
            "content": content,
            "score": score,
            "nickname": f"用户{pid}0{i}",
            "source": ["京东", "小红书", "知乎"][i % 3],
            "date": f"2026-{i:02d}-{random.randint(1,28):02d}",
            "likes": random.randint(50, 800),
            "sentiment": sentiment,
            "aspects": ["性能", "拍照", "续航"][:2]
        })
    return reviews

import random

# 生成所有产品
products = {}
pid = 1
for brand, product_list in brands.items():
    for product in product_list:
        products[product] = {
            "brand": brand,
            "reviews": make_reviews(product, brand, pid),
            "pros": [f"{brand}优点{i}" for i in range(1, 6)],
            "cons": [f"{brand}缺点{i}" for i in range(1, 6)]
        }
        pid += 1

# 保存
with open('../frontend-simple/data/reviews.json', 'w', encoding='utf-8') as f:
    json.dump({"products": products}, f, ensure_ascii=False, indent=2)

print("Done")
print(f"Total products: {len(products)}")
