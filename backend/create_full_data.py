#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成7大品牌多代产品的用户评价数据
"""

import json

data = {
    "products": {
        # ============ Apple ============
        "iPhone 15 Pro Max": {
            "brand": "Apple",
            "reviews": [
                {"id": 1, "content": "A17 Pro芯片性能确实强，原神最高画质60帧稳如老狗。钛金属边框手感好，重量减轻了。但是充电速度还是27W太慢，价格也太贵了。", "score": 4, "nickname": "科技数码控", "source": "京东", "date": "2026-04-20", "likes": 456, "sentiment": "positive", "aspects": ["性能", "外观"]},
                {"id": 2, "content": "拍照效果很满意，5倍光学变焦拍远景很清晰。但是夜景模式偶尔过度锐化，希望后续优化。", "score": 4, "nickname": "摄影爱好者", "source": "小红书", "date": "2026-04-18", "likes": 234, "sentiment": "positive", "aspects": ["拍照"]}
            ],
            "pros": ["A17 Pro芯片性能最强", "钛金属边框重量减轻"],
            "cons": ["价格昂贵性价比低", "27W充电速度太慢"]
        },
        "iPhone 15": {
            "brand": "Apple",
            "reviews": [
                {"id": 3, "content": "A16芯片性能足够日常使用，动态岛很实用。但是60Hz刷新率真的不应该，充电速度也慢。", "score": 4, "nickname": "果粉一枚", "source": "京东", "date": "2026-04-10", "likes": 345, "sentiment": "positive", "aspects": ["性能", "刷新率"]}
            ],
            "pros": ["A16芯片性能足够", "动态岛交互实用"],
            "cons": ["60Hz刷新率落后", "充电速度慢"]
        },
        "iPhone 14 Pro": {
            "brand": "Apple",
            "reviews": [
                {"id": 4, "content": "A16芯片性能强，4800万主摄拍照效果好。但是充电速度慢，信号问题依然存在。", "score": 4, "nickname": "苹果用户", "source": "京东", "date": "2026-04-05", "likes": 267, "sentiment": "positive", "aspects": ["性能", "拍照"]}
            ],
            "pros": ["A16芯片性能强", "4800万主摄拍照好"],
            "cons": ["充电速度慢", "信号问题依然存在"]
        },
        # ============ Huawei ============
        "Mate 60 Pro": {
            "brand": "Huawei",
            "reviews": [
                {"id": 5, "content": "麒麟9000S回归真的感动，虽然性能不算顶级但日常够用。支持国产！鸿蒙系统流畅，多设备协同强大。", "score": 5, "nickname": "国产支持者", "source": "京东", "date": "2026-04-18", "likes": 789, "sentiment": "positive", "aspects": ["芯片", "系统"]}
            ],
            "pros": ["麒麟芯片回归支持国产", "鸿蒙系统流畅协同强"],
            "cons": ["没有GMS国外APP受限", "充电时发热明显"]
        },
        "Mate 50 Pro": {
            "brand": "Huawei",
            "reviews": [
                {"id": 6, "content": "XMAGE影像系统调教不错，拍照效果好。但是骁龙8+ Gen1性能虽然够用，发热还是有点明显。", "score": 4, "nickname": "摄影达人", "source": "京东", "date": "2026-04-12", "likes": 267, "sentiment": "positive", "aspects": ["拍照", "性能"]}
            ],
            "pros": ["XMAGE影像拍照好", "昆仑玻璃耐摔"],
            "cons": ["屏幕支架较宽", "部分APP适配不好"]
        },
        # ============ Xiaomi ============
        "小米14 Pro": {
            "brand": "Xiaomi",
            "reviews": [
                {"id": 7, "content": "性价比真的高，骁龙8 Gen3性能强。120W快充19分钟充满。但是MIUI广告多，需要手动关闭。", "score": 5, "nickname": "性价比之王", "source": "京东", "date": "2026-04-15", "likes": 678, "sentiment": "positive", "aspects": ["性价比", "性能"]}
            ],
            "pros": ["性价比极高配置拉满", "骁龙8 Gen3性能强"],
            "cons": ["MIUI广告多需手动关", "做工材质不如苹果"]
        },
        "小米13": {
            "brand": "Xiaomi",
            "reviews": [
                {"id": 8, "content": "小屏旗舰很适合单手操作，骁龙8 Gen2性能强。MIUI 14流畅度提升明显。但是续航一般。", "score": 4, "nickname": "小屏爱好者", "source": "京东", "date": "2026-04-08", "likes": 389, "sentiment": "positive", "aspects": ["尺寸", "性能"]}
            ],
            "pros": ["小屏旗舰单手操作好", "骁龙8 Gen2性能强"],
            "cons": ["续航一般", "拍照不如Pro版"]
        },
        # ============ Samsung ============
        "Galaxy S24 Ultra": {
            "brand": "Samsung",
            "reviews": [
                {"id": 9, "content": "骁龙8 Gen3 for Galaxy性能强，2亿像素拍照效果很好。S Pen很实用，办公效率高。但是充电速度只有45W。", "score": 4, "nickname": "商务人士", "source": "京东", "date": "2026-04-18", "likes": 567, "sentiment": "positive", "aspects": ["性能", "拍照"]}
            ],
            "pros": ["骁龙8 Gen3性能强", "2亿像素拍照好"],
            "cons": ["45W充电速度慢", "续航不如iPhone"]
        },
        "Galaxy S23": {
            "brand": "Samsung",
            "reviews": [
                {"id": 10, "content": "骁龙8 Gen2性能强，散热控制比上一代好。One UI系统流畅，自定义程度高。但是充电速度只有25W太慢了。", "score": 4, "nickname": "三星老用户", "source": "京东", "date": "2026-04-10", "likes": 345, "sentiment": "positive", "aspects": ["性能", "散热"]}
            ],
            "pros": ["骁龙8 Gen2性能强", "散热控制有改善"],
            "cons": ["25W充电速度太慢", "续航一般"]
        },
        # ============ Oppo ============
        "Find X7 Ultra": {
            "brand": "Oppo",
            "reviews": [
                {"id": 11, "content": "哈苏影像系统拍照效果很好，1英寸大底主摄进光量大。100W快充速度快。但是ColorOS系统广告多。", "score": 4, "nickname": "拍照爱好者", "source": "京东", "date": "2026-04-15", "likes": 456, "sentiment": "positive", "aspects": ["拍照", "充电"]}
            ],
            "pros": ["哈苏影像拍照效果好", "100W快充速度快"],
            "cons": ["ColorOS广告多", "续航一般"]
        },
        "Find X6 Pro": {
            "brand": "Oppo",
            "reviews": [
                {"id": 12, "content": "拍照效果提升很大，马里亚纳X芯片加持。100W快充速度快。但是ColorOS系统广告还是多。", "score": 4, "nickname": "OPPO用户", "source": "京东", "date": "2026-04-10", "likes": 289, "sentiment": "positive", "aspects": ["拍照", "充电"]}
            ],
            "pros": ["哈苏影像系统优秀", "100W快充速度快"],
            "cons": ["ColorOS广告多", "系统稳定性需提升"]
        },
        # ============ Vivo ============
        "X100 Pro": {
            "brand": "Vivo",
            "reviews": [
                {"id": 13, "content": "蔡司光学拍照效果很好，人像模式特别赞。天玑9300性能强，功耗控制不错。120W快充速度快。", "score": 5, "nickname": "人像摄影师", "source": "京东", "date": "2026-04-18", "likes": 567, "sentiment": "positive", "aspects": ["拍照", "性能"]}
            ],
            "pros": ["蔡司光学拍照优秀", "天玑9300性能强"],
            "cons": ["OriginOS学习成本高", "系统广告多"]
        },
        "X90 Pro+": {
            "brand": "Vivo",
            "reviews": [
                {"id": 14, "content": "蔡司影像系统拍照效果好，特别是人像模式。骁龙8 Gen2性能强。但是OriginOS系统不好上手。", "score": 4, "nickname": "Vivo老用户", "source": "京东", "date": "2026-04-12", "likes": 345, "sentiment": "positive", "aspects": ["拍照", "性能"]}
            ],
            "pros": ["蔡司影像拍照好", "骁龙8 Gen2性能强"],
            "cons": ["OriginOS不好上手", "系统广告多"]
        },
        # ============ Honor ============
        "Magic 6 Pro": {
            "brand": "Honor",
            "reviews": [
                {"id": 15, "content": "骁龙8 Gen3性能强，MagicOS系统流畅度提升明显。拍照效果不错，鹰眼相机抓拍快。但是续航一般。", "score": 4, "nickname": "荣耀用户", "source": "京东", "date": "2026-04-15", "likes": 423, "sentiment": "positive", "aspects": ["性能", "系统"]}
            ],
            "pros": ["骁龙8 Gen3性能强", "MagicOS流畅度提升"],
            "cons": ["系统广告多", "66W充电不算快"]
        },
        "Magic 5 Pro": {
            "brand": "Honor",
            "reviews": [
                {"id": 16, "content": "骁龙8 Gen2性能强，MagicOS系统流畅。拍照效果不错，特别是夜景模式。但是续航一般。", "score": 4, "nickname": "荣耀粉丝", "source": "京东", "date": "2026-04-10", "likes": 356, "sentiment": "positive", "aspects": ["性能", "系统"]}
            ],
            "pros": ["骁龙8 Gen2性能强", "MagicOS系统流畅"],
            "cons": ["系统广告多", "66W充电不算快"]
        }
    }
}

# 保存为JSON文件
output_file = '../frontend-simple/data/reviews.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"数据已保存到: {output_file}")
print(f"共生成 {len(data['products'])} 款产品")
print("\n各品牌产品数量:")
brands = {}
for product in data['products'].values():
    brand = product['brand']
    brands[brand] = brands.get(brand, 0) + 1
for brand, count in brands.items():
    print(f"  {brand}: {count}款")
