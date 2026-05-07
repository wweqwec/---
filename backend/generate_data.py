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
                {"id": 1, "content": "A17 Pro芯片性能确实强，原神最高画质60帧稳如老狗。钛金属边框手感好，重量减轻了。但是充电速度还是27W太慢，价格也太贵了。", "score": 4, "nickname": "科技数码控", "source": "京东", "date": "2026-04-20", "likes": 456, "sentiment": "positive", "aspects": ["性能", "外观", "充电", "价格"]},
                {"id": 2, "content": "拍照效果很满意，5倍光学变焦拍远景很清晰。但是夜景模式偶尔过度锐化，希望后续优化。iOS系统流畅，但信号问题依然存在。", "score": 4, "nickname": "摄影爱好者", "source": "小红书", "date": "2026-04-18", "likes": 234, "sentiment": "positive", "aspects": ["拍照", "系统", "信号"]},
                {"id": 3, "content": "价格真的太夸张了，顶配快2万。USB-C接口终于有了，但速度只有USB 2.0，传输大文件很慢。60Hz刷新率也该淘汰了。", "score": 2, "nickname": "性价比党", "source": "知乎", "date": "2026-04-15", "likes": 678, "sentiment": "negative", "aspects": ["价格", "接口", "刷新率"]}
            ],
            "pros": ["A17 Pro芯片性能最强", "钛金属边框重量减轻", "iOS系统流畅稳定", "5倍光学变焦拍照好", "续航有提升"],
            "cons": ["价格昂贵性价比低", "27W充电速度太慢", "60Hz刷新率落后", "USB-C速度仅USB 2.0", "信号问题依然存在"]
        },
        "iPhone 15": {
            "brand": "Apple",
            "reviews": [
                {"id": 4, "content": "A16芯片性能足够日常使用，动态岛很实用。但是60Hz刷新率真的不应该，充电速度也慢。不过iOS系统流畅，生态完善。", "score": 4, "nickname": "果粉一枚", "source": "京东", "date": "2026-04-10", "likes": 345, "sentiment": "positive", "aspects": ["性能", "刷新率", "系统"]},
                {"id": 5, "content": "终于换USB-C了，但是充电速度还是慢。拍照效果不错，视频防抖很好。就是电池续航一般，重度使用需要一天两充。", "score": 3, "nickname": "视频博主", "source": "小红书", "date": "2026-04-08", "likes": 189, "sentiment": "neutral", "aspects": ["接口", "充电", "拍照", "续航"]}
            ],
            "pros": ["A16芯片性能足够", "动态岛交互实用", "iOS系统流畅", "USB-C接口终于来了", "视频防抖效果好"],
            "cons": ["60Hz刷新率落后", "充电速度慢", "续航一般", "没有长焦镜头", "价格偏高"]
        },
        "iPhone 14 Pro": {
            "brand": "Apple",
            "reviews": [
                {"id": 6, "content": "A16芯片性能强，4800万主摄拍照效果好。但是充电速度慢，信号问题依然存在。灵动岛交互很有创意。", "score": 4, "nickname": "苹果用户", "source": "京东", "date": "2026-04-05", "likes": 267, "sentiment": "positive", "aspects": ["性能", "拍照", "充电", "信号"]},
                {"id": 7, "content": "屏幕素质很好，Promotion自适应刷新率流畅。但是60Hz在安卓旗舰面前确实落后，充电速度也慢。价格偏贵。", "score": 3, "nickname": "屏幕党", "source": "知乎", "date": "2026-04-03", "likes": 198, "sentiment": "neutral", "aspects": ["屏幕", "刷新率", "充电", "价格"]}
            ],
            "pros": ["A16芯片性能强", "4800万主摄拍照好", "灵动岛交互创新", "Promotion自适应刷新率", "iOS系统流畅"],
            "cons": ["充电速度慢", "信号问题依然存在", "价格偏贵", "重量偏重", "60Hz刷新率落后"]}
    }
}

# 保存为JSON文件
output_file = '../frontend-simple/data/reviews.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"数据已保存到: {output_file}")
print(f"共生成 {len(data['products'])} 款产品")
