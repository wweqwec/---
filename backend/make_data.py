#!/usr/bin/env python3
import json

data = {
    "products": {
        "iPhone 15 Pro Max": {
            "brand": "Apple",
            "reviews": [
                {"id": 1, "content": "A17 Pro芯片性能确实强，原神最高画质60帧稳如老狗。钛金属边框手感好，重量减轻了。", "score": 4, "nickname": "科技数码控", "source": "京东", "date": "2026-04-20", "likes": 456, "sentiment": "positive", "aspects": ["性能", "外观"]},
                {"id": 2, "content": "拍照效果很满意，5倍光学变焦拍远景很清晰。但是夜景模式偶尔过度锐化。", "score": 4, "nickname": "摄影爱好者", "source": "小红书", "date": "2026-04-18", "likes": 234, "sentiment": "positive", "aspects": ["拍照"]},
                {"id": 3, "content": "充电速度还是27W太慢，价格也太贵了。顶配快2万，性价比太低。", "score": 2, "nickname": "性价比党", "source": "知乎", "date": "2026-04-15", "likes": 678, "sentiment": "negative", "aspects": ["充电", "价格"]},
                {"id": 4, "content": "续航比14 Pro Max好一些，重度使用能撑一天。但是充电真的太慢了。", "score": 3, "nickname": "续航焦虑者", "source": "京东", "date": "2026-04-12", "likes": 567, "sentiment": "neutral", "aspects": ["续航", "充电"]},
                {"id": 5, "content": "钛金属边框确实轻了，但是容易刮花。摄像头凸起还是太严重。", "score": 3, "nickname": "实用主义者", "source": "小红书", "date": "2026-04-10", "likes": 345, "sentiment": "neutral", "aspects": ["外观", "摄像头"]},
                {"id": 6, "content": "Face ID识别速度很快，戴口罩也能解锁。但是湿手解锁还是不行。", "score": 4, "nickname": "科技评论员", "source": "知乎", "date": "2026-04-08", "likes": 267, "sentiment": "positive", "aspects": ["解锁"]},
                {"id": 7, "content": "屏幕素质顶级，2000尼特峰值亮度。但是60Hz刷新率真的该淘汰了。", "score": 3, "nickname": "屏幕发烧友", "source": "京东", "date": "2026-04-05", "likes": 201, "sentiment": "neutral", "aspects": ["屏幕", "刷新率"]},
                {"id": 8, "content": "Action Button自定义功能很实用。但是默认功能太少，希望增加更多选项。", "score": 4, "nickname": "极客玩家", "source": "小红书", "date": "2026-04-03", "likes": 98, "sentiment": "positive", "aspects": ["功能"]},
                {"id": 9, "content": "iOS系统流畅度没得说，但是信号还是老问题。地下室经常没信号。", "score": 3, "nickname": "移动办公族", "source": "知乎", "date": "2026-04-01", "likes": 432, "sentiment": "neutral", "aspects": ["系统", "信号"]},
                {"id": 10, "content": "生态系统确实强大，多设备无缝切换。但是配件太贵了，充电头都要几百。", "score": 3, "nickname": "苹果全家桶", "source": "京东", "date": "2026-03-28", "likes": 289, "sentiment": "neutral", "aspects": ["生态", "价格"]}
            ],
            "pros": ["A17 Pro芯片性能最强", "钛金属边框重量减轻", "iOS系统流畅稳定", "5倍光学变焦拍照好"],
            "cons": ["价格昂贵性价比低", "27W充电速度太慢", "60Hz刷新率落后", "信号问题依然存在"]
        },
        "iPhone 15": {
            "brand": "Apple",
            "reviews": [
                {"id": 11, "content": "A16芯片性能足够日常使用，动态岛很实用。但是60Hz刷新率不应该。", "score": 4, "nickname": "果粉一枚", "source": "京东", "date": "2026-04-10", "likes": 345, "sentiment": "positive", "aspects": ["性能", "刷新率"]},
                {"id": 12, "content": "终于换USB-C了，但是充电速度还是慢。拍照效果不错，视频防抖很好。", "score": 3, "nickname": "视频博主", "source": "小红书", "date": "2026-04-08", "likes": 189, "sentiment": "neutral", "aspects": ["接口", "拍照"]}
            ],
            "pros": ["A16芯片性能足够", "动态岛交互实用", "iOS系统流畅", "USB-C接口终于来了"],
            "cons": ["60Hz刷新率落后", "充电速度慢", "续航一般", "没有长焦镜头"]
        }
    }
}

with open('../frontend-simple/data/reviews.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Done")
