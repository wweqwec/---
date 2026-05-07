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
        "iPhone 15 Pro": {
            "brand": "Apple",
            "reviews": [
                {"id": 4, "content": "A17 Pro芯片性能强，尺寸比Max版更适合单手操作。但是充电速度慢，价格还是偏贵。灵动岛交互很实用。", "score": 4, "nickname": "果粉一枚", "source": "京东", "date": "2026-04-12", "likes": 345, "sentiment": "positive", "aspects": ["性能", "尺寸", "充电", "价格"]},
                {"id": 5, "content": "钛金属边框手感好，重量减轻了。但是60Hz刷新率真的不应该，安卓千元机都120Hz了。拍照效果不错。", "score": 3, "nickname": "参数党", "source": "知乎", "date": "2026-04-10", "likes": 267, "sentiment": "neutral", "aspects": ["外观", "刷新率", "拍照"]}
            ],
            "pros": ["A17 Pro芯片性能强", "钛金属边框重量轻", "尺寸适中单手好操作", "灵动岛交互实用", "iOS系统流畅"],
            "cons": ["60Hz刷新率落后", "充电速度慢", "价格偏贵", "USB-C速度慢", "信号问题依然存在"]}
    }
}

# 保存为JSON文件
output_file = '../frontend-simple/data/reviews.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"数据已保存到: {output_file}")
print(f"共生成 {len(data['products'])} 款产品")
