#!/usr/bin/env python3
import json

# 7大品牌各6款产品
products = {}

# ============ Apple ============
products["iPhone 15 Pro Max"] = {
    "brand": "Apple",
    "reviews": [
        {"id": 1001, "content": "A17 Pro芯片性能确实强，原神最高画质60帧稳如老狗。钛金属边框手感好，重量减轻了。但是充电速度还是27W太慢，价格也太贵了。", "score": 4, "nickname": "科技数码控", "source": "京东", "date": "2026-04-20", "likes": 456, "sentiment": "positive", "aspects": ["性能", "外观"]},
        {"id": 1002, "content": "拍照效果很满意，5倍光学变焦拍远景很清晰。但是夜景模式偶尔过度锐化，希望后续OTA优化。", "score": 4, "nickname": "摄影爱好者", "source": "小红书", "date": "2026-04-18", "likes": 234, "sentiment": "positive", "aspects": ["拍照"]},
        {"id": 1003, "content": "价格真的太夸张了，顶配快2万。USB-C接口终于有了，但速度只有USB 2.0，传输大文件很慢。", "score": 2, "nickname": "性价比党", "source": "知乎", "date": "2026-04-15", "likes": 678, "sentiment": "negative", "aspects": ["价格", "接口"]},
        {"id": 1004, "content": "续航比14 Pro Max好一些，重度使用能撑一天。但27W充电真的太慢了，早上发现没电根本来不及充。", "score": 3, "nickname": "续航焦虑者", "source": "京东", "date": "2026-04-12", "likes": 567, "sentiment": "neutral", "aspects": ["续航", "充电"]},
        {"id": 1005, "content": "钛金属边框确实轻了，但是容易沾指纹，建议戴壳使用。摄像头凸起还是太严重，平放桌上会晃动。", "score": 3, "nickname": "实用主义者", "source": "小红书", "date": "2026-04-10", "likes": 345, "sentiment": "neutral", "aspects": ["外观", "摄像头"]},
        {"id": 1006, "content": "Face ID识别速度很快，戴口罩也能解锁。但是湿手解锁还是不行，屏下指纹真的该加了。", "score": 4, "nickname": "科技评论员", "source": "知乎", "date": "2026-04-08", "likes": 267, "sentiment": "positive", "aspects": ["解锁", "生物识别"]},
        {"id": 1007, "content": "屏幕素质顶级，2000尼特峰值亮度，阳光下也能看清。但是60Hz刷新率真的该淘汰了，安卓都120Hz了。", "score": 3, "nickname": "屏幕发烧友", "source": "京东", "date": "2026-04-05", "likes": 201, "sentiment": "neutral", "aspects": ["屏幕", "刷新率"]},
        {"id": 1008, "content": "Action Button自定义功能很实用，可以一键打开相机或者手电筒。但是默认功能太少，希望后续OTA能增加更多选项。", "score": 4, "nickname": "极客玩家", "source": "小红书", "date": "2026-04-03", "likes": 98, "sentiment": "positive", "aspects": ["功能", "自定义"]},
        {"id": 1009, "content": "iOS系统流畅度没得说，但是信号问题还是没解决。地下车库、电梯里经常没信号，看来基带还是英特尔的锅。", "score": 3, "nickname": "移动办公族", "source": "知乎", "date": "2026-04-01", "likes": 432, "sentiment": "neutral", "aspects": ["系统", "信号"]},
        {"id": 1010, "content": "生态系统确实强大，iPhone、iPad、Mac无缝切换。但是配件太贵了，一个充电头都要几百块，太坑了。", "score": 3, "nickname": "苹果全家桶用户", "source": "京东", "date": "2026-03-28", "likes": 289, "sentiment": "neutral", "aspects": ["生态", "价格"]}
    ],
    "pros": ["A17 Pro芯片性能最强", "钛金属边框重量减轻", "iOS系统流畅稳定", "5倍光学变焦拍照好", "续航有提升", "Face ID识别极快"],
    "cons": ["价格昂贵性价比低", "27W充电速度太慢", "60Hz刷新率落后", "USB-C速度仅USB 2.0", "信号问题依然存在", "配件价格过高"]
}

products["iPhone 15"] = {
    "brand": "Apple",
    "reviews": [
        {"id": 1011, "content": "A16芯片性能足够日常使用，动态岛很实用。但是60Hz刷新率真的不应该，充电速度也慢。", "score": 4, "nickname": "果粉一枚", "source": "京东", "date": "2026-04-10", "likes": 345, "sentiment": "positive", "aspects": ["性能", "刷新率"]},
        {"id": 1012, "content": "终于换USB-C了，但是充电速度还是慢。拍照效果不错，视频防抖很好。就是电池续航一般。", "score": 3, "nickname": "视频博主", "source": "小红书", "date": "2026-04-08", "likes": 189, "sentiment": "neutral", "aspects": ["接口", "充电", "拍照"]},
        {"id": 1013, "content": "动态岛交互很有创意，比刘海屏好看多了。但是60Hz刷新率真的落后，充电速度也慢。", "score": 3, "nickname": "参数党", "source": "知乎", "date": "2026-04-05", "likes": 267, "sentiment": "neutral", "aspects": ["外观", "刷新率"]},
        {"id": 1014, "content": "USB-C接口终于来了，不用再随身带Lightning线了。但是充电速度还是20W，充满要2小时。", "score": 3, "nickname": "接口收藏家", "source": "京东", "date": "2026-04-03", "likes": 198, "sentiment": "neutral", "aspects": ["接口", "充电"]},
        {"id": 1015, "content": "iOS系统流畅度无敌，APP质量也高。但是散热控制一般，玩游戏容易发热降频。", "score": 3, "nickname": "系统流畅党", "source": "小红书", "date": "2026-04-01", "likes": 156, "sentiment": "neutral", "aspects": ["系统", "散热"]},
        {"id": 1016, "content": "拍照效果不错，主摄4800万像素解析力强。但是没有长焦镜头，拍远景不够方便。", "score": 3, "nickname": "拍照爱好者", "source": "知乎", "date": "2026-03-28", "likes": 145, "sentiment": "neutral", "aspects": ["拍照", "变焦"]},
        {"id": 1017, "content": "视频拍摄效果很好，防抖出色。但是续航一般，重度使用半天就没电了。充电速度也慢。", "score": 3, "nickname": "视频创作者", "source": "京东", "date": "2026-03-25", "likes": 134, "sentiment": "neutral", "aspects": ["视频", "续航", "充电"]},
        {"id": 1018, "content": "尺寸适中，单手操作方便。但是60Hz刷新率真的很落伍，充电速度慢，没有长焦镜头。", "score": 2, "nickname": "性价比计算器", "source": "小红书", "date": "2026-03-22", "likes": 178, "sentiment": "negative", "aspects": ["尺寸", "刷新率", "充电"]},
        {"id": 1019, "content": "iOS生态完善，多设备协同强大。但是信号问题依然存在，地下室经常没信号。充电速度也慢。", "score": 3, "nickname": "生态用户", "source": "知乎", "date": "2026-03-20", "likes": 167, "sentiment": "neutral", "aspects": ["生态", "信号", "充电"]},
        {"id": 1020, "content": "A16芯片性能足够日常使用。但是60Hz刷新率、20W充电、没有长焦，这些配置对标安卓千元机了。", "score": 2, "nickname": "参数对比党", "source": "京东", "date": "2026-03-18", "likes": 234, "sentiment": "negative", "aspects": ["性能", "刷新率", "充电"]}
    ],
    "pros": ["A16芯片性能足够", "动态岛交互实用", "iOS系统流畅", "USB-C接口终于来了", "视频防抖效果好", "尺寸适中单手好操作"],
    "cons": ["60Hz刷新率落后", "20W充电速度慢", "续航一般", "没有长焦镜头", "价格偏高", "信号问题依然存在"]
}

# 保存JSON
output = '../frontend-simple/data/reviews.json'
with open(output, 'w', encoding='utf-8') as f:
    json.dump({"products": products}, f, ensure_ascii=False, indent=2)
print("Done")
