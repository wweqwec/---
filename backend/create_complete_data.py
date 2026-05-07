#!/usr/bin/env python3
import json
import random

# 模板：用于生成真实用户评价
review_templates = {
    "positive": [
        "性能很强，日常使用很流畅。",
        "拍照效果很好，色彩还原准确。",
        "续航表现不错，重度使用能撑一天。",
        "系统流畅度很好，操作跟手。",
        "充电速度很快，半小时就能充满。",
        "屏幕素质很好，显示效果细腻。",
        "信号表现很好，地下室也有信号。",
        "做工精致，质感很好。",
        "性价比很高，配置对得起价格。",
        "外观设计好看，手感很好。"
    ],
    "neutral": [
        "性能足够日常使用，但是充电速度慢。",
        "拍照效果不错，但是续航一般。",
        "续航表现一般，充电速度还行。",
        "系统流畅度还行，但是信号一般。",
        "充电速度还行，但是续航一般。",
        "屏幕素质不错，但是充电慢。",
        "信号表现一般，续航也不行。",
        "做工还行，但是性价比一般。",
        "性价比一般，做工也一般。",
        "外观中规中矩，性能还行。"
    ],
    "negative": [
        "性能还行，但是充电速度太慢了。",
        "拍照效果一般，续航也差。",
        "续航太差了，一天要充两次电。",
        "系统卡顿，广告太多。",
        "充电速度太慢了，充满要2小时。",
        "屏幕素质一般，亮度不够。",
        "信号太差了，地下室经常没信号。",
        "做工粗糙，边框缝隙大。",
        "性价比太低了，价格虚高。",
        "外观设计丑，辨识度低。"
    ]
}

# 各品牌产品定义
brands_products = {
    "Apple": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14"],
    "Huawei": ["Mate 60 Pro", "Mate 60", "Mate 50 Pro", "Mate 50", "P60 Pro", "P60"],
    "Xiaomi": ["小米14 Pro", "小米14", "小米13 Pro", "小米13", "小米12S Pro", "小米12S"],
    "Samsung": ["Galaxy S24 Ultra", "Galaxy S24", "Galaxy S23 Ultra", "Galaxy S23", "Galaxy S22 Ultra", "Galaxy S22"],
    "Oppo": ["Find X7 Ultra", "Find X7", "Find X6 Pro", "Find X6", "Find X5 Pro", "Find X5"],
    "Vivo": ["X100 Pro", "X100", "X90 Pro+", "X90 Pro", "X80 Pro", "X80"],
    "Honor": ["Magic 6 Pro", "Magic 6", "Magic 5 Pro", "Magic 5", "Magic 4 Pro", "Magic 4"]
}

# 各品牌优缺点模板
pros_cons_templates = {
    "Apple": {
        "pros": ["A系列芯片性能最强", "iOS系统流畅稳定", "生态完善协同强大", "做工精致质感好", "系统更新支持久"],
        "cons": ["价格昂贵性价比低", "充电速度慢", "信号问题依然存在", "刷新率落后", "配件价格过高"]
    },
    "Huawei": {
        "pros": ["麒麟芯片回归", "鸿蒙系统流畅", "信号表现优秀", "拍照效果好", "快充速度快"],
        "cons": ["没有GMS国外APP受限", "应用生态需完善", "充电时发热明显", "屏幕支架较宽", "品牌溢价不如苹果"]
    },
    "Xiaomi": {
        "pros": ["性价比极高", "骁龙旗舰芯片性能强", "快充速度快", "配置拉满", "MIUI功能丰富"],
        "cons": ["MIUI广告多", "做工材质不如苹果", "系统稳定性需提升", "信号表现一般", "保值率低"]
    },
    "Samsung": {
        "pros": ["屏幕素质顶级", "拍照效果好", "S Pen提升效率", "One UI功能丰富", "做工精致"],
        "cons": ["充电速度慢", "续航不如iPhone", "价格偏贵", "发热控制需优化", "系统有些复杂"]
    },
    "Oppo": {
        "pros": ["哈苏影像拍照好", "快充速度快", "外观时尚", "做工不错", "屏幕素质好"],
        "cons": ["ColorOS广告多", "系统稳定性需提升", "续航一般", "信号表现一般", "性价比不高"]
    },
    "Vivo": {
        "pros": ["蔡司光学拍照好", "人像模式优秀", "快充速度快", "屏幕护眼", "外观好看"],
        "cons": ["OriginOS学习成本高", "系统广告多", "续航一般", "充电时发热", "价格偏高"]
    },
    "Honor": {
        "pros": ["骁龙旗舰芯片性能强", "MagicOS流畅", "鹰眼相机抓拍快", "屏幕护眼", "信号表现好"],
        "cons": ["系统广告多", "快充速度不算快", "续航不如预期", "价格偏高", "保值率低"]
    }
}

# 生成评价
def generate_reviews(product_name, brand, count=10):
    reviews = []
    sources = ["京东", "小红书", "知乎"]
    nicknames = ["科技数码控", "摄影爱好者", "性价比党", "果粉一枚", "国产支持者", 
                "续航焦虑者", "快充依赖者", "小屏爱好者", "屏幕发烧友", "数码工坊",
                "极客玩家", "视频博主", "参数党", "理性消费者", "护眼党"]
    
    for i in range(1, count + 1):
        sentiment = random.choice(["positive"] * 4 + ["neutral"] * 3 + ["negative"] * 3)
        
        if sentiment == "positive":
            score = random.randint(4, 5)
        elif sentiment == "neutral":
            score = 3
        else:
            score = random.randint(1, 2)
        
        template = random.choice(review_templates[sentiment])
        aspect1 = random.choice(["性能", "拍照", "续航", "充电", "外观", "系统", "屏幕", "信号"])
        aspect2 = random.choice(["性能", "拍照", "续航", "充电", "外观", "系统", "屏幕", "信号"])
        
        content = template.format(product_name, f"{aspect1}表现不错" if sentiment == "positive" else f"{aspect1}有待提升")
        
        reviews.append({
            "id": random.randint(1000, 9999),
            "content": content,
            "score": score,
            "nickname": random.choice(nicknames),
            "source": random.choice(sources),
            "date": f"2026-{random.randint(1,4):02d}-{random.randint(1,28):02d}",
            "likes": random.randint(50, 800),
            "sentiment": sentiment,
            "aspects": list(set([aspect1, aspect2]))
        })
    
    return reviews

# 生成所有产品数据
products = {}
for brand, product_list in brands_products.items():
    for product in product_list:
        products[product] = {
            "brand": brand,
            "reviews": generate_reviews(product, brand, count=10),
            "pros": random.sample(pros_cons_templates[brand]["pros"], 5),
            "cons": random.sample(pros_cons_templates[brand]["cons"], 5)
        }

# 保存为JSON文件
output_file = '../frontend-simple/data/reviews.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({"products": products}, f, ensure_ascii=False, indent=2)

print(f"数据已保存到: {output_file}")
print(f"共生成 {len(products)} 款产品")
print("\n各品牌产品数量:")
brand_counts = {}
for product, data in products.items():
    brand = data["brand"]
    brand_counts[brand] = brand_counts.get(brand, 0) + 1
for brand, count in brand_counts.items():
    print(f"  {brand}: {count}款")

# 验证JSON格式
try:
    with open(output_file, 'r', encoding='utf-8') as f:
        json.load(f)
    print("\n✅ JSON格式验证通过")
except Exception as e:
    print(f"\n❌ JSON格式错误: {e}")
