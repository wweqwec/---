#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
京东用户评价爬虫 - 使用Python标准库（无需额外依赖）
"""

import urllib.request
import urllib.parse
import json
import time
import random

def crawl_jd_reviews(product_id, page=1, page_size=10):
    """
    爬取京东商品评价
    
    Args:
        product_id: 京东商品ID
        page: 页码
        page_size: 每页数量
    
    Returns:
        评价列表
    """
    # 京东评价API
    url = f"https://club.jd.com/comment/productPageComments.action"
    
    # 构造请求参数
    params = {
        'productId': product_id,
        'score': '0',  # 0=全部, 1=差评, 2=中评, 3=好评
        'sortType': '5',  # 5=推荐排序
        'page': str(page),
        'pageSize': str(page_size),
        'isShadowSku': '0',
        'fold': '1'
    }
    
    # 构造请求URL
    full_url = url + '?' + urllib.parse.urlencode(params)
    
    # 设置请求头（模拟浏览器）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': f'https://item.jd.com/{product_id}.html',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    try:
        # 发送请求
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if 'comments' in data:
                reviews = []
                for comment in data['comments']:
                    review = {
                        'id': comment.get('id', ''),
                        'content': comment.get('content', ''),
                        'score': comment.get('score', 5),  # 1-5分
                        'nickname': comment.get('nickname', '匿名用户'),
                        'productColor': comment.get('productColor', ''),
                        'productSize': comment.get('productSize', ''),
                        'referenceTime': comment.get('referenceTime', ''),
                        'usefulVoteCount': comment.get('usefulVoteCount', 0),
                        'replyCount': comment.get('replyCount', 0),
                        'source': '京东',
                        'productId': product_id
                    }
                    
                    # 判断情感（根据评分）
                    if review['score'] >= 4:
                        review['sentiment'] = 'positive'
                    elif review['score'] == 3:
                        review['sentiment'] = 'neutral'
                    else:
                        review['sentiment'] = 'negative'
                    
                    reviews.append(review)
                
                return reviews
            else:
                print(f"未找到评价数据: {data}")
                return []
    
    except Exception as e:
        print(f"爬取失败: {e}")
        return []

def search_jd_product(keyword):
    """
    搜索京东商品，获取商品ID
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        商品ID列表
    """
    # 简化版：直接返回已知的热门商品ID
    known_products = {
        'iPhone 15 Pro Max': '10074947411370',
        'iPhone 15': '10072967348168',
        'Mate 60 Pro': '10077048153511',
        'Mate 60': '10077048153507',
        '小米14 Pro': '10077048153522',
        '小米14': '10077048153518',
        'Galaxy S24 Ultra': '10077048153533',
        'Galaxy S24': '10077048153529'
    }
    
    return known_products.get(keyword, None)

def main():
    """主函数 - 爬取示例"""
    print("=" * 60)
    print("京东用户评价爬虫（Python标准库版）")
    print("=" * 60)
    
    # 测试爬取 iPhone 15 Pro Max 的评价
    product_name = "iPhone 15 Pro Max"
    product_id = search_jd_product(product_name)
    
    if not product_id:
        print(f"未找到商品: {product_name}")
        return
    
    print(f"\n正在爬取: {product_name}")
    print(f"商品ID: {product_id}")
    print("-" * 60)
    
    # 爬取前3页评价
    all_reviews = []
    for page in range(1, 4):
        print(f"正在爬取第 {page} 页...")
        reviews = crawl_jd_reviews(product_id, page=page, page_size=10)
        
        if reviews:
            all_reviews.extend(reviews)
            print(f"  成功爬取 {len(reviews)} 条评价")
        else:
            print(f"  未获取到评价")
        
        # 随机延迟，避免被封
        time.sleep(random.uniform(1, 3))
    
    # 保存为JSON文件
    output_file = '../frontend-simple/data/jd_reviews.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"爬取完成！共获取 {len(all_reviews)} 条评价")
    print(f"数据已保存到: {output_file}")
    print("=" * 60)
    
    # 统计情感分布
    positive = sum(1 for r in all_reviews if r['sentiment'] == 'positive')
    neutral = sum(1 for r in all_reviews if r['sentiment'] == 'neutral')
    negative = sum(1 for r in all_reviews if r['sentiment'] == 'negative')
    
    print(f"\n情感分布:")
    print(f"  正面评价: {positive} 条 ({positive/len(all_reviews)*100:.1f}%)")
    print(f"  中性评价: {neutral} 条 ({neutral/len(all_reviews)*100:.1f}%)")
    print(f"  负面评价: {negative} 条 ({negative/len(all_reviews)*100:.1f}%)")

if __name__ == '__main__':
    main()
