import json

# 7大品牌各6款产品
b = {
    "Apple": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14"],
    "Huawei": ["Mate 60 Pro", "Mate 60", "Mate 50 Pro", "Mate 50", "P60 Pro", "P60"],
    "Xiaomi": ["Xiaomi 14 Pro", "Xiaomi 14", "Xiaomi 13 Pro", "Xiaomi 13", "Xiaomi 12S Pro", "Xiaomi 12S"],
    "Samsung": ["Galaxy S24 Ultra", "Galaxy S24", "Galaxy S23 Ultra", "Galaxy S23", "Galaxy S22 Ultra", "Galaxy S22"],
    "Oppo": ["Find X7 Ultra", "Find X7", "Find X6 Pro", "Find X6", "Find X5 Pro", "Find X5"],
    "Vivo": ["X100 Pro", "X100", "X90 Pro+", "X90 Pro", "X80 Pro", "X80"],
    "Honor": ["Magic 6 Pro", "Magic 6", "Magic 5 Pro", "Magic 5", "Magic 4 Pro", "Magic 4"]
}

p = {}
for brand, products in b.items():
    for product in products:
        r = []
        for i in range(1, 11):
            s = 4 if i <= 6 else (3 if i <= 9 else 2)
            t = "positive" if s >= 4 else ("neutral" if s == 3 else "negative")
            r.append({"id": 1000 + len(p) * 100 + i, "content": f"{product}评价{i}，包含真实用户体验。", "score": s, "nickname": f"User{i}", "source": ["京东", "小红书", "知乎"][i % 3], "date": "2026-04-{:02d}".format(i * 2), "likes": i * 50, "sentiment": t, "aspects": ["性能", "拍照"]})
        p[product] = {"brand": brand, "reviews": r, "pros": [f"{brand}优点{i}" for i in range(1, 6)], "cons": [f"{brand}缺点{i}" for i in range(1, 6)]}

with open('../frontend-simple/data/reviews.json', 'w', encoding='utf-8') as f:
    json.dump({"products": p}, f, ensure_ascii=False, indent=2)
