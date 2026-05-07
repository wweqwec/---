import json

# 7大品牌各6款产品
b = {
    "Apple": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14"],
    "Huawei": ["Mate 60 Pro", "Mate 60", "Mate 50 Pro", "Mate 50", "P60 Pro", "P60"],
    "Xiaomi": ["小米14 Pro", "小米14", "小米13 Pro", "小米13", "小米12S Pro", "小米12S"],
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
            r.append({"id": 1000 + len(p) * 100 + i, "content": product + "评价" + str(i), "score": s, "nickname": "User" + str(i), "source": "JD", "date": "2026-04-01", "likes": 100, "sentiment": t, "aspects": ["性能"]})
        p[product] = {"brand": brand, "reviews": r, "pros": ["优点1"], "cons": ["缺点1"]}

with open('../frontend-simple/data/reviews.json', 'w', encoding='utf-8') as f:
    json.dump({"products": p}, f, ensure_ascii=False, indent=2)
