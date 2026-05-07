#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI助手后端服务 - 使用阿里云百炼API（完整版）
支持离线模拟模式，无需联网即可运行

⚙️ 切换在线/离线模式：
   修改下方 USE_OFFLINE_MODE 的值
   - True  = 离线模拟模式（无需联网，使用本地回复）
   - False = 在线API模式（需要联网，调用阿里云百炼API）
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests
import time
import re
import random


# ================================
# ⚙️ 配置开关：切换在线/离线模式
# ================================
USE_OFFLINE_MODE = True  # True = 离线模拟模式，False = 在线API模式
# ================================


def generate_offline_response(user_message, products, selected_product=None, budget=None, history=None, all_products=None):
    """
    离线模拟AI回复（无需联网）
    根据用户输入生成预设的智能回复
    支持对话历史，能理解上下文
    """
    user_message_lower = user_message.lower()
    
    # 如果没有传入所有产品数据，使用products作为所有产品
    if all_products is None:
        all_products = products
    
    # 判断问题类型
    is_comparison = any(word in user_message_lower for word in ['对比', '比较', '区别', 'vs', '和', '哪个好', '哪个强', '哪个差'])
    is_pros_cons = any(word in user_message_lower for word in ['优点', '缺点', '好处', '不足', '槽点', '评价', '怎么样', '如何'])
    
    # 判断是否是延续性问题（用户想继续之前的对话）
    continuation_keywords = ['继续', '还有', '其他的', '那款', '这个', '这款', '呢', '吗', '推荐']
    is_continuation = any(word in user_message for word in continuation_keywords)
    
    # 只有是延续性问题时，才从历史恢复预算
    # 对比问题和优缺点问题不使用历史预算
    if history and not budget and is_continuation and not is_comparison and not is_pros_cons:
        for h in reversed(history):
            if h.get('budget'):
                budget = h.get('budget')
                # 如果有历史预算，重新过滤产品
                products = filter_products_by_budget(all_products, budget)
                print(f"[AI-离线] 从历史恢复预算：{budget}元，过滤后剩余：{len(products)} 款")
                break
    
    # 也检查历史中提到的产品选择（只在查询优缺点时）
    if history and not selected_product:
        # 如果用户询问优缺点，尝试从历史中找到选中的产品
        if any(word in user_message_lower for word in ['优点', '缺点', '好处', '不足', '槽点', '评价']):
            for h in reversed(history):
                if h.get('selected_product'):
                    # 检查该产品是否还在当前产品列表中
                    if h.get('selected_product') in all_products:
                        selected_product = h.get('selected_product')
                        print(f"[AI-离线] 从历史恢复选中产品：{selected_product}")
                        break
    
    # 1. 问候语
    if any(word in user_message for word in ['你好', 'hi', 'hello', '嗨', '您好']):
        return random.choice([
            "您好！我是手机推荐助手，可以帮您推荐手机、对比机型、分析评价。请问有什么可以帮您？",
            "嗨！我是AI手机顾问。告诉我您的预算和需求，我帮您选最合适的手机！"
        ])
    
    # 2. 推荐手机（有预算）- 优先级提高，放在对比之前
    if budget:
        if products:
            # 判断用户是否有特定需求（游戏、拍照、续航等）
            has_specific_need = False
            need_type = None
            
            if any(word in user_message_lower for word in ['游戏', '性能', '最强', '最快', '帧率', '骁龙']):
                has_specific_need = True
                need_type = '游戏性能'
            elif any(word in user_message_lower for word in ['拍照', '摄影', '相机', '像素', '摄像头']):
                has_specific_need = True
                need_type = '拍照'
            elif any(word in user_message_lower for word in ['续航', '电池', '充电', '电量']):
                has_specific_need = True
                need_type = '续航'
            
            # 如果有特定需求，进行筛选和排序
            if has_specific_need:
                # 根据需求筛选和评分产品
                scored_products = []
                for name, data in products.items():
                    pros_list = data.get('pros', [])
                    cons_list = data.get('cons', [])
                    pros_text = ' '.join(pros_list)
                    cons_text = ' '.join(cons_list)
                    all_text = pros_text + ' ' + cons_text
                    
                    # 根据需求类型评分
                    score = 0
                    if need_type == '游戏性能':
                        # 优点中包含性能相关关键词，加分
                        if any(word in pros_text for word in ['性能', '游戏', '帧率', '骁龙', '芯片', '流畅']):
                            score += 3
                        # 缺点中包含性能相关负面词，减分
                        if any(word in cons_text for word in ['发热', '卡顿', '掉帧']):
                            score -= 2
                    elif need_type == '拍照':
                        if any(word in pros_text for word in ['拍照', '摄影', '相机', '像素', '徕卡', '影像', '样张']):
                            score += 3
                        if any(word in cons_text for word in ['拍照差', '拍照一般', '相机垃圾']):
                            score -= 2
                    elif need_type == '续航':
                        if any(word in pros_text for word in ['续航', '电池', '充电', '耐用']):
                            score += 3
                        if any(word in cons_text for word in ['续航差', '电池小', '充电慢']):
                            score -= 2
                    
                    # 只添加有得分的产品（说明优缺点中提到过该需求）
                    if score > 0:
                        scored_products.append((name, data, score))
                
                # 按得分排序（从高到低）
                scored_products.sort(key=lambda x: x[2], reverse=True)
                
                # 如果筛选后有结果，使用筛选结果；否则使用所有产品
                if scored_products:
                    products_to_show = [(name, data) for name, data, score in scored_products]
                    print(f"[AI-离线] 根据{need_type}需求筛选并排序，剩余：{len(products_to_show)} 款")
                else:
                    # 如果没有产品提到该需求，使用所有产品但不排序
                    products_to_show = list(products.items())
                    print(f"[AI-离线] 根据{need_type}需求筛选无结果，使用所有产品")
            else:
                products_to_show = list(products.items())
            
            # 生成推荐列表
            product_list = []
            for idx, (name, data) in enumerate(products_to_show[:5], 1):
                brand = data['brand']
                price_info = data.get('price', {})
                if isinstance(price_info, dict):
                    price = price_info.get('current_price', price_info.get('price', '暂无价格'))
                else:
                    price = str(price_info)
                
                # 根据需求类型，只显示相关的优缺点
                if has_specific_need and need_type == '游戏性能':
                    pros = '、'.join([p for p in data.get('pros', []) if any(w in p for w in ['性能', '游戏', '帧率', '芯片', '流畅'])][:2])
                    cons = '、'.join([c for c in data.get('cons', []) if any(w in c for w in ['发热', '卡顿'])][:2])
                elif has_specific_need and need_type == '拍照':
                    pros = '、'.join([p for p in data.get('pros', []) if any(w in p for w in ['拍照', '摄影', '相机', '像素', '影像'])][:2])
                    cons = '、'.join([c for c in data.get('cons', []) if any(w in c for w in ['拍照', '相机'])][:2])
                elif has_specific_need and need_type == '续航':
                    pros = '、'.join([p for p in data.get('pros', []) if any(w in p for w in ['续航', '电池', '充电'])][:2])
                    cons = '、'.join([c for c in data.get('cons', []) if any(w in c for w in ['续航', '电池', '充电'])][:2])
                else:
                    pros = '、'.join(data.get('pros', [])[:2])
                    cons = '、'.join(data.get('cons', [])[:2])
                
                product_list.append(f"{idx}. {brand} {name}（{price}元）\n   优点：{pros}\n   缺点：{cons}")
            
            # 根据是否有特定需求生成回复
            if has_specific_need:
                reply = f"根据您的{budget}元预算，为您推荐以下{need_type}强的手机：\n\n"
            else:
                reply = f"根据您的{budget}元预算，为您推荐以下手机：\n\n"
            
            reply += "\n\n".join(product_list)
            reply += f"\n\n[提示] 以上共{len(products_to_show)}款手机符合您的需求，您可以选择感兴趣的机型查看详细评价分析。"
            return reply
        else:
            return f"抱歉，当前数据集中暂不支持{budget}元预算范围内的手机。建议：\n1. 扩大预算范围\n2. 查看热门机型（不限定预算）"
    
    # 3. 对比请求 - 改进版：支持直接识别用户提到的两款手机
    if any(word in user_message_lower for word in ['对比', '比较', '区别', 'vs', '和', '哪个好', '哪个强', '哪个差']):
        # 尝试从用户消息中提取产品名称（使用所有产品数据，不受预算过滤影响）
        mentioned_products = []
        
        # 预处理用户消息（去掉多余空格，便于匹配）
        user_message_normalized = ''.join(user_message_lower.split())  # 去掉所有空格
        
        print(f"[AI-离线-对比] 用户消息（去空格）: {user_message_normalized}")
        
        for name, data in all_products.items():  # 使用all_products而不是products
            # 检查产品名称是否在用户消息中（支持模糊匹配）
            name_lower = name.lower()
            name_normalized = ''.join(name_lower.split())  # 去掉所有空格
            brand = data.get('brand', '').lower()
            brand_normalized = ''.join(brand.split()) if brand else ''  # 去掉所有空格
            
            # 精确匹配产品名（去掉空格后比较）
            if name_normalized in user_message_normalized:
                mentioned_products.append((name, data))
                print(f"[AI-离线-对比] 匹配到产品（精确）: {name} (normalized: {name_normalized})")
            # 模糊匹配：品牌+关键词（去掉空格后比较）
            elif brand and brand_normalized in user_message_normalized:
                # 提取产品名中的关键词（去掉品牌名后，再去掉空格）
                keywords = name_lower.replace(brand, '').strip()
                keywords_normalized = ''.join(keywords.split())  # 去掉所有空格
                if keywords_normalized and keywords_normalized in user_message_normalized:
                    mentioned_products.append((name, data))
                    print(f"[AI-离线-对比] 匹配到产品（模糊）: {name} (brand: {brand}, keywords: {keywords_normalized})")
        
        # 修复：去除子字符串匹配的产品（保留最长的产品名）
        if len(mentioned_products) > 2:
            # 按产品名称长度排序（从长到短）
            mentioned_products.sort(key=lambda x: len(x[0]), reverse=True)
            
            # 去除子字符串匹配的产品
            filtered_products = []
            for i, (name1, data1) in enumerate(mentioned_products):
                is_substring = False
                name1_normalized = ''.join(name1.lower().split())
                for j, (name2, data2) in enumerate(mentioned_products):
                    if i != j:
                        name2_normalized = ''.join(name2.lower().split())
                        # 如果name1是name2的子字符串，且name1比name2短
                        if name1_normalized in name2_normalized and len(name1_normalized) < len(name2_normalized):
                            is_substring = True
                            print(f"[AI-离线-对比] 去除子字符串匹配: {name1} (被 {name2} 包含)")
                            break
                if not is_substring:
                    filtered_products.append((name1, data1))
            
            mentioned_products = filtered_products
            print(f"[AI-离线-对比] 去重后产品数量: {len(mentioned_products)}")
        
        # 如果找到至少两个产品，进行对比
        if len(mentioned_products) >= 2:
            product1_name, product1_data = mentioned_products[0]
            product2_name, product2_data = mentioned_products[1]
            
            # 判断对比维度（拍照、游戏、续航等）
            compare_aspect = "综合"
            if any(word in user_message_lower for word in ['拍照', '摄影', '相机', '像素', '摄像头']):
                compare_aspect = "拍照"
            elif any(word in user_message_lower for word in ['游戏', '性能', '帧率', '骁龙']):
                compare_aspect = "游戏性能"
            elif any(word in user_message_lower for word in ['续航', '电池', '充电']):
                compare_aspect = "续航"
            
            # 构建对比结果
            result = f"【{compare_aspect}对比】：{product1_name} vs {product2_name}\n\n"
            
            result += f"【{product1_name}】：\n"
            result += f"  优点：{'、'.join(product1_data.get('pros', [])[:3])}\n"
            result += f"  缺点：{'、'.join(product1_data.get('cons', [])[:2])}\n\n"
            
            result += f"【{product2_name}】：\n"
            result += f"  优点：{'、'.join(product2_data.get('pros', [])[:3])}\n"
            result += f"  缺点：{'、'.join(product2_data.get('cons', [])[:2])}\n\n"
            
            # 根据对比维度给出建议
            if compare_aspect == "拍照":
                result += "[建议] 拍照建议：关注摄像头参数、影像算法、样片效果\n"
            elif compare_aspect == "游戏性能":
                result += "[建议] 游戏建议：关注处理器、散热、帧率稳定性\n"
            elif compare_aspect == "续航":
                result += "[建议] 续航建议：关注电池容量、充电速度、实际续航测试\n"
            
            result += "\n您可以根据上述对比，结合自己的使用习惯做决定。"
            return result
        
        # 如果只有一个产品或没有找到产品，但有选中的产品
        elif selected_product and selected_product in products:
            selected_data = products[selected_product]
            
            # 尝试找到另一个产品（同品牌或第一个其他产品）
            other_product = None
            for name, data in products.items():
                if name != selected_product:
                    other_product = (name, data)
                    break
            
            if other_product:
                result = f"【对比】：{selected_product} vs {other_product[0]}\n\n"
                result += f"{selected_product}：\n"
                result += f"  优点：{'、'.join(selected_data.get('pros', [])[:3])}\n"
                result += f"  缺点：{'、'.join(selected_data.get('cons', [])[:2])}\n\n"
                result += f"{other_product[0]}：\n"
                result += f"  优点：{'、'.join(other_product[1].get('pros', [])[:3])}\n"
                result += f"  缺点：{'、'.join(other_product[1].get('cons', [])[:2])}\n"
                return result + "\n您可以根据上述对比，结合自己的使用习惯做决定。"
        
        # 如果无法识别两个产品，提示用户
        return "我检测到您想对比两款手机，但无法识别具体型号。请明确告诉我您想对比的手机名称，例如：'iPhone 15 Pro Max和小米14 Ultra哪个拍照好'"
    
    # 4. 询问优点/缺点
    if selected_product and products:
        if selected_product in products:
            data = products[selected_product]
            if any(word in user_message_lower for word in ['优点', '好处', '优势', '好']):
                pros = '、'.join(data.get('pros', []))
                return f"【{selected_product}】的主要优点：\n{pros}\n\n您可以在左侧查看详细用户评价。"
            if any(word in user_message_lower for word in ['缺点', '不足', '槽点', '差']):
                cons = '、'.join(data.get('cons', []))
                return f"【{selected_product}】的主要缺点：\n{cons}\n\n建议结合您的实际使用需求判断是否可接受。"
    
    # 5. 按用途推荐（游戏、拍照等）
    if any(word in user_message_lower for word in ['游戏', '性能', '最强', '最快', '帧率', '骁龙']):
        # 筛选游戏性能强的手机（根据优点中包含"性能"、"游戏"、"帧率"等）
        game_phones = []
        for name, data in products.items():
            pros_text = ' '.join(data.get('pros', []))
            if any(word in pros_text for word in ['性能', '游戏', '帧率', '骁龙']):
                game_phones.append((name, data))
        
        if game_phones:
            product_list = []
            for idx, (name, data) in enumerate(game_phones[:3], 1):
                brand = data['brand']
                price_info = data.get('price', {})
                if isinstance(price_info, dict):
                    price = price_info.get('current_price', price_info.get('price', '暂无价格'))
                else:
                    price = str(price_info)
                pros = '、'.join(data.get('pros', [])[:2])
                product_list.append(f"{idx}. {brand} {name}（{price}元）\n   性能特点：{pros}")
            
            return "根据数据分析，以下手机游戏性能较强：\n\n" + "\n\n".join(product_list)
        else:
            return "根据现有数据，推荐关注搭载骁龙8 Gen系列芯片的机型，如：\n1. 小米14 Pro\n2. Redmi K70\n3. 一加 Ace 2\n\n具体性能表现可查看各机型的详细评价。"
    
    # 6. 拍照推荐
    if any(word in user_message_lower for word in ['拍照', '摄影', '相机', '像素', '摄像头']):
        camera_phones = []
        for name, data in products.items():
            pros_text = ' '.join(data.get('pros', []))
            if any(word in pros_text for word in ['拍照', '摄影', '相机', '像素', '徕卡', '影像']):
                camera_phones.append((name, data))
        
        if camera_phones:
            product_list = []
            for idx, (name, data) in enumerate(camera_phones[:3], 1):
                brand = data['brand']
                price_info = data.get('price', {})
                if isinstance(price_info, dict):
                    price = price_info.get('current_price', price_info.get('price', '暂无价格'))
                else:
                    price = str(price_info)
                pros = '、'.join(data.get('pros', [])[:2])
                product_list.append(f"{idx}. {brand} {name}（{price}元）\n   拍照特点：{pros}")
            
            return "根据数据分析，以下手机拍照表现较好：\n\n" + "\n\n".join(product_list)
        else:
            return "根据现有数据，拍照较好的机型通常集中在高端旗舰，如iPhone系列、华为Mate/P系列、小米Ultra系列等。"
    
    # 7. 续航推荐
    if any(word in user_message_lower for word in ['续航', '电池', '充电', '电量']):
        battery_phones = []
        for name, data in products.items():
            pros_text = ' '.join(data.get('pros', []))
            if any(word in pros_text for word in ['续航', '电池', '充电']):
                battery_phones.append((name, data))
        
        if battery_phones:
            product_list = []
            for idx, (name, data) in enumerate(battery_phones[:3], 1):
                brand = data['brand']
                price_info = data.get('price', {})
                if isinstance(price_info, dict):
                    price = price_info.get('current_price', price_info.get('price', '暂无价格'))
                else:
                    price = str(price_info)
                pros = '、'.join(data.get('pros', [])[:2])
                product_list.append(f"{idx}. {brand} {name}（{price}元）\n   续航特点：{pros}")
            
            return "根据数据分析，以下手机续航表现较好：\n\n" + "\n\n".join(product_list)
    
    # 8. 推荐但不限定预算
    if any(word in user_message_lower for word in ['推荐', '建议', '买哪款', '选哪款']):
        if products:
            # 推荐前3款
            product_list = []
            for idx, (name, data) in enumerate(list(products.items())[:3], 1):
                brand = data['brand']
                price_info = data.get('price', {})
                if isinstance(price_info, dict):
                    price = price_info.get('current_price', price_info.get('price', '暂无价格'))
                else:
                    price = str(price_info)
                product_list.append(f"{idx}. {brand} {name}（{price}元）")
            
            return "以下是一些热门推荐：\n" + "\n".join(product_list) + "\n\n💡 您可以告诉我您的预算，我会为您筛选更精准的推荐！"
        else:
            return "请告诉我您的预算范围，例如：'3000元以下'、'5000元左右'，我会为您推荐合适的手机。"
    
    # 9. 默认回复
    default_replies = [
        "好的，我正在分析您的需求。请告诉我您的预算范围，我会为您推荐合适的手机。",
        "了解您的需求了。为了给您更精准的推荐，请告诉我：\n1. 您的预算范围\n2. 主要用途（游戏、拍照、办公等）\n3. 品牌偏好（如果有的话）",
        "我帮您分析一下。您可以：\n- 直接说预算，我推荐手机\n- 选择一个产品，我分析优缺点\n- 询问两款手机的对比"
    ]
    
    return random.choice(default_replies)


def extract_budget(user_message):
    """
    从用户消息中提取预算
    支持多种格式：3000元预算、预算3000、3000以内、3000预算等
    返回：预算金额（整数），如果没有则返回None
    """
    # 匹配各种预算表达方式（按顺序匹配，更宽松的模式放前面）
    patterns = [
        r'(\d+)\s*元预算',           # 3000元预算
        r'(\d+)\s*预算',             # 3000预算（新增）
        r'预算\s*[为是:：]\s*(\d+)',  # 预算为3000、预算：3000
        r'(\d+)\s*元以下',           # 3000元以下
        r'(\d+)\s*以内',             # 3000以内
        r'(\d+)\s*块以下',           # 3000块以下
        r'(\d+)\s*左右',             # 3000左右
        r'(\d+)\s*到\s*(\d+)',      # 3000到5000，返回上限
        r'(\d+)\s*元',               # 3000元（通用匹配，放最后）
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_message)
        if match:
            if len(match.groups()) == 2:  # 区间
                return int(match.group(2))
            return int(match.group(1))
    
    return None


def filter_products_by_budget(products, budget):
    """
    根据预算过滤产品
    价格可能是字符串（如"4500-5200"）或数字，或字典
    只要价格区间的任意部分在预算内，就包含
    """
    filtered = {}
    for name, data in products.items():
        price_info = data.get('price', {})
        
        # 提取价格（正确处理字典格式）
        price_value = 0
        if isinstance(price_info, dict):
            # 如果是字典，取current_price或price
            if 'current_price' in price_info:
                price_value = int(price_info['current_price'])
            elif 'price' in price_info:
                price_value = int(price_info['price'])
        elif isinstance(price_info, (int, float)):
            price_value = int(price_info)
        else:
            # 尝试从字符串中提取数字
            price_str = str(price_info)
            numbers = re.findall(r'\d+', price_str)
            if numbers:
                price_value = int(numbers[0])
        
        # 如果价格超过预算，跳过
        if price_value > budget:
            continue
        
        filtered[name] = data
    
    return filtered


def validate_and_fix_response(response, products):
    """
    验证AI响应，检查是否推荐了列表中不存在的手机
    """
    product_names = list(products.keys())
    
    # 常见的错误推荐模式
    error_patterns = [
        (r'一加\s*11', '一加 Ace 2'),
        (r'iPhone\s*15\s*Pro(?!\s*Max)', 'iPhone 15 Pro Max'),
    ]
    
    corrected = response
    for pattern, replacement in error_patterns:
        if re.search(pattern, corrected, re.IGNORECASE):
            print(f"[AI] 检测到可能的错误推荐：{pattern}，建议替换为：{replacement}")
            corrected = re.sub(pattern, f'{replacement}（注意：数据集中的完整型号是{replacement}）', corrected, flags=re.IGNORECASE)
    
    return corrected


app = Flask(__name__)
CORS(app)

# 阿里云百炼API配置（在线模式使用）
API_KEY = "sk-ac5a29627d7d46b39703dffcd28b4a01"
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# 读取产品数据（缓存）
_products_cache = None
# 存储前端发送的完整产品数据
_full_products_data = None
# 存储对话历史（简单实现，实际部署应使用session或数据库）
_conversation_history = {}
MAX_HISTORY_LENGTH = 10  # 最多保留10轮对话

def load_products_data():
    """加载产品数据（带缓存）"""
    global _products_cache
    if _products_cache is not None:
        return _products_cache
    
    try:
        with open('data/reviews.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        _products_cache = data['products']
        return _products_cache
    except Exception as e:
        print(f"[错误] 加载产品数据失败: {e}")
        return {}


@app.route('/api/ai/load-products', methods=['POST'])
def load_products():
    """接收前端发送的完整产品数据"""
    global _full_products_data
    
    try:
        data = request.get_json()
        products = data.get('products', {})
        
        if not products:
            return jsonify({
                'success': False,
                'error': '没有收到产品数据'
            }), 400
        
        _full_products_data = products
        
        print(f"[AI] 收到完整产品数据：{len(products)} 款产品")
        
        return jsonify({
            'success': True,
            'message': f'已加载 {len(products)} 款产品的数据',
            'product_count': len(products)
        })
        
    except Exception as e:
        print(f"[AI] 加载产品数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI对话接口（支持在线/离线模式）"""
    try:
        # 获取用户问题
        data = request.get_json()
        user_message = data.get('message', '')
        selected_product = data.get('product', None)
        session_id = data.get('session_id', 'default')  # 简单的session管理
        
        if not user_message:
            return jsonify({'error': '请输入您的问题'}), 400
        
        # 加载产品数据（优先使用前端发送的完整数据）
        if _full_products_data is not None:
            all_products = _full_products_data
            print(f"[AI] 使用完整产品数据：{len(all_products)} 款")
        else:
            all_products = load_products_data()
            print(f"[AI] 使用本地产品数据：{len(all_products)} 款")
        
        # 尝试从用户消息中提取预算
        budget = extract_budget(user_message)
        
        # 如果用户提到预算，先过滤产品
        if budget:
            products = filter_products_by_budget(all_products, budget)
            print(f"[AI] 检测到预算：{budget}元，过滤后剩余：{len(products)} 款")
        else:
            products = all_products
        
        # 获取对话历史
        history = _conversation_history.get(session_id, [])
        
        # 保存当前用户消息到历史
        history.append({
            'role': 'user',
            'message': user_message,
            'budget': budget,
            'selected_product': selected_product,
            'timestamp': time.time()
        })
        
        # 限制历史长度
        if len(history) > MAX_HISTORY_LENGTH:
            history = history[-MAX_HISTORY_LENGTH:]
        
        # ================================
        # 离线模式：使用本地模拟回复
        # ================================
        # 离线模式：使用本地模拟回复
        # ================================
        if USE_OFFLINE_MODE:
            print(f"[AI-离线] 用户问题: {user_message}")
            print(f"[AI-离线] 选中产品: {selected_product}")
            print(f"[AI-离线] 预算: {budget}")
            print(f"[AI-离线] 对话历史: {len(history)} 条")
            
            ai_response = generate_offline_response(
                user_message=user_message,
                products=products,
                selected_product=selected_product,
                budget=budget,
                history=history,
                all_products=all_products  # 传递所有产品数据
            )
            
            print(f"[AI-离线] 回复: {ai_response[:100]}...")
            
            # 保存AI回复到历史
            history.append({
                'role': 'assistant',
                'message': ai_response,
                'timestamp': time.time()
            })
            _conversation_history[session_id] = history
            
            return jsonify({
                'success': True,
                'response': ai_response,
                'timestamp': time.time(),
                'mode': 'offline'
            })
        
        # ================================
        # 在线模式：调用阿里云百炼API
        # ================================
        else:
            # 构建系统提示词
            system_prompt = """你是专业的手机推荐顾问，只能基于提供的产品数据进行推荐。

【严格约束】：
1. 只能从下面提供的产品列表中选择手机进行推荐，绝对不能推荐列表中不存在的手机型号
2. 如果列表中没有符合用户需求的手机，必须明确告知："当前数据集暂不支持您需求的手机"
3. 推荐手机时，必须使用列表中完全相同的产品名称，不能自行修改或简化
4. 推荐手机时，必须说明完整的品牌名称

回答要求：
1. 根据用户需求从列表中选择合适的手机（预算、用途、品牌偏好等）
2. 当用户问"XXX元以下有哪些手机"时，必须列出所有符合预算的手机，不要只列1-2款
3. 对比不同手机的优缺点（只能对比列表中的手机）
4. 回答简洁专业，控制在400字以内
5. 如果没有足够信息，可以询问用户更多需求

【重要】回答格式要求：
- 列出多款手机时，使用数字编号，每款手机单独一行
- 必须基于实际价格数据回答，不要编造价格
"""
            
            # 添加产品信息到提示词
            if selected_product and selected_product in all_products:
                # 如果用户选中了某个产品，发送该产品的详细信息
                product_data = all_products[selected_product]
                brand = product_data['brand']
                # 正确处理价格字段（可能是字符串或数字）
                price_info = product_data.get('price', {})
                if isinstance(price_info, dict):
                    price = price_info.get('current_price', price_info.get('price', '暂无价格'))
                else:
                    price = str(price_info)
                pros = '、'.join(product_data.get('pros', [])[:3])
                cons = '、'.join(product_data.get('cons', [])[:3])
                
                system_prompt += f"\n用户当前查看：{brand} {selected_product}\n价格：{price}元\n优点：{pros}\n缺点：{cons}\n"
            else:
                # 发送过滤后的产品列表（用于推荐）
                system_prompt += "\n【可推荐的手机列表（必须从中选择，不能推荐列表外的手机）】：\n"
                
                if not products:
                    system_prompt += f"\n（没有找到符合您预算的产品）\n"
                else:
                    # 简化的产品列表格式
                    for idx, (product_name, product_data) in enumerate(products.items(), 1):
                        brand = product_data['brand']
                        # 正确处理价格字段
                        price_info = product_data.get('price', {})
                        if isinstance(price_info, dict):
                            price = price_info.get('current_price', price_info.get('price', '暂无价格'))
                        else:
                            price = str(price_info)
                        
                        system_prompt += f"{idx}. {brand} {product_name} - {price}元\n"
                
                system_prompt += "\n【重要】：\n"
                system_prompt += "1. 只能从上述列表中选择手机进行推荐，绝对不能推荐列表中不存在的手机\n"
                system_prompt += "2. 必须使用列表中完全相同的产品名称\n"
                system_prompt += "3. 如果列表中没有符合用户需求的手机，请明确告知'当前数据集暂不支持您需求的手机'\n"
                system_prompt += "4. 推荐时要说明完整的品牌名称\n"
                system_prompt += "5. 当用户问'XXX元以下有哪些手机'时，必须列出上述列表中的所有手机\n"
            
            # 构建消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # 调用阿里云百炼API
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "qwen-max",  # 使用通义千问Max模型
                "input": {
                    "messages": messages
                },
                "parameters": {
                    "temperature": 0.1,  # 降低温度，让AI回答更快速
                    "top_p": 0.9,
                    "max_tokens": 500  # 限制输出长度，加快响应速度
                }
            }
            
            print(f"[AI-在线] 用户问题: {user_message}")
            print(f"[AI-在线] 选中产品: {selected_product}")
            print(f"[AI-在线] 预算: {budget}")
            print(f"[AI-在线] 发送给AI的产品数量: {len(products)}")
            
            # 调用API（120秒超时）
            response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                
                # 检查响应格式
                if 'output' in result and 'text' in result['output']:
                    ai_response = result['output']['text']
                elif 'choices' in result:
                    # 兼容不同的响应格式
                    ai_response = result['choices'][0]['message']['content']
                else:
                    print(f"[AI] 响应格式异常: {result}")
                    ai_response = "抱歉，AI服务响应格式异常，请稍后重试。"
                
                # 验证AI响应：检查是否推荐了列表中不存在的手机
                ai_response = validate_and_fix_response(ai_response, products)
                
                print(f"[AI-在线] 回复成功: {ai_response[:100]}...")
                
                return jsonify({
                    'success': True,
                    'response': ai_response,
                    'timestamp': time.time(),
                    'mode': 'online'
                })
            else:
                print(f"[AI] API调用失败: {response.status_code} - {response.text}")
                # 提供更详细的错误信息
                error_msg = f'AI服务暂时不可用（错误码：{response.status_code}）'
                if response.status_code == 401:
                    error_msg = 'AI服务认证失败，请检查API Key是否正确'
                elif response.status_code == 429:
                    error_msg = 'AI服务请求过于频繁，请稍后再试'
                elif response.status_code >= 500:
                    error_msg = 'AI服务端错误，请稍后重试'
                
                return jsonify({
                    'success': False,
                    'error': error_msg
                }), 500
        
    except requests.exceptions.Timeout:
        print(f"[AI] 请求超时")
        return jsonify({
            'success': False,
            'error': 'AI服务响应超时，请稍后重试或简化您的问题'
        }), 504
    
    except Exception as e:
        print(f"[AI] 服务器错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@app.route('/api/products', methods=['GET'])
def get_products():
    """获取所有产品列表"""
    try:
        products = load_products_data()
        product_list = []
        
        for name, data in products.items():
            product_list.append({
                'name': name,
                'brand': data['brand'],
                'price': data['price']['current_price']
            })
        
        return jsonify({
            'success': True,
            'products': product_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    mode = "离线模拟模式" if USE_OFFLINE_MODE else "在线API模式"
    return jsonify({
        'status': 'ok',
        'mode': mode,
        'api': '本地模拟' if USE_OFFLINE_MODE else '阿里云百炼',
        'model': '本地规则引擎' if USE_OFFLINE_MODE else 'qwen-max',
        'full_data_loaded': _full_products_data is not None
    })


if __name__ == '__main__':
    print("=" * 70)
    print("  AI助手服务启动")
    print("=" * 70)
    print()
    if USE_OFFLINE_MODE:
        print("  [离线] 当前模式：离线模拟模式（无需联网）")
        print("  [提示] 切换在线模式：修改 USE_OFFLINE_MODE = False")
    else:
        print("  [在线] 当前模式：在线API模式（需要联网）")
        print("  [提示] 切换离线模式：修改 USE_OFFLINE_MODE = True")
    print("=" * 70)
    print()
    print("  接口列表：")
    print("  - POST /api/ai/load-products  # 加载完整产品数据")
    print("  - POST /api/ai/chat         # AI对话")
    print("  - GET  /api/products       # 获取产品列表")
    print("  - GET  /api/health         # 健康检查")
    print()
    print("  访问地址: <http://localhost:5000>")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
