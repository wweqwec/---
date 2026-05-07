#!/usr/bin/env python3
import json
import random

# 7大品牌各6款产品
brands_products = {
    "Apple": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14"],
    "Huawei": ["Mate 60 Pro", "Mate 60", "Mate 50 Pro", "Mate 50", "P60 Pro", "P60"],
    "Xiaomi": ["小米14 Pro", "小米14", "小米13 Pro", "小米13", "小米12S Pro", "小米12S"],
    "Samsung": ["Galaxy S24 Ultra", "Galaxy S24", "Galaxy S23 Ultra", "Galaxy S23", "Galaxy S22 Ultra", "Galaxy S22"],
    "Oppo": ["Find X7 Ultra", "Find X7", "Find X6 Pro", "Find X6", "Find X5 Pro", "Find X5"],
    "Vivo": ["X100 Pro", "X100", "X90 Pro+", "X90 Pro", "X80 Pro", "X80"],
    "Honor": ["Magic 6 Pro", "Magic 6", "Magic 5 Pro", "Magic 5", "Magic 4 Pro", "Magic 4"]
}

products = {}

# 为每个产品生成10条评价
for brand, product_list in brands_products.items():
    for idx, product in enumerate(product_list):
        reviews = []
        for i in range(1, 11):
            # 随机生成评价
            score = random.choice([5, 5, 4, 4, 4, 3, 3, 2])
            sentiment = "positive" if score >= 4 else ("neutral" if score == 3 else "negative")
            
            content = f"{product}的评价内容{i}，包含真实用户体验。"
            if sentiment == "positive":
                content = f"{product}性能很好，使用体验满意。{content}"
            elif sentiment == "neutral":
                content = f"{product}性能还行，但是有些缺点。{content}"
            else:
                content = f"{product}有些问题，体验不够好。{content}"
            
            reviews.append({
                "id": random.randint(1000, 9999),
                "content": content,
                "score": score,
                "nickname": f"用户{i}",
                "source": random.choice(["京东", "小红书", "知乎"]),
                "date": "2026-04-{:02d}".format(random.randint(1, 28)),
                "likes": random.randint(50, 800),
                "sentiment": sentiment,
                "aspects": random.sample(["性能", "拍照", "续航", "充电", "外观"], 2)
            })
        
        products[product] = {
            "brand": brand,
            "reviews": reviews,
            "pros": [f"{brand}优点{i}" for i in range(1, 6)],
            "cons": [f"{brand}缺点{i}" for i in range(1, 6)]
        }

# 保存为JSON
with open('../frontend-simple/data/reviews.json', 'w', encoding='utf-8') as f:
    json.dump({"products": products}, f, ensure_ascii=False, indent=2)

print("Done")
print(f"Total: {len(products)} products")
