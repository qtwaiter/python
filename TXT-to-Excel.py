import pandas as pd
import re

def extract_number(text):
    # 从字符串中提取数字
    if isinstance(text, str):
        # 移除逗号
        text = text.replace(',', '')
        # 查找数字（包括小数点）
        numbers = re.findall(r'\d+\.?\d*', text)
        return float(numbers[0]) if numbers else 0
    return text

def is_product_name(line):
    # 排除明确不是商品名称的行
    if any(keyword in line for keyword in ['¥', '下单数:', '出库数:']):
        return False
    # 如果行中只包含数字和单位（斤/箱），则不是商品名称
    if re.match(r'^[\d.,]+\s*(斤|箱)$', line.strip()):
        return False
    return True

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    current_item = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:  # 跳过空行
            i += 1
            continue
            
        # 使用新的判断函数来确定是否为商品名称行
        if is_product_name(line):
            # 如果已有商品数据，保存它
            if current_item is not None:
                data.append(current_item.copy())
                print(f"添加商品: {current_item['商品名称']}")  # 调试信息
            
            # 创建新的商品数据
            current_item = {
                '商品名称': line,
                '单价（元/斤）': 0,
                '总价（元）': 0,
                '下单数（斤）': 0,
                '出库数（斤）': 0
            }
            print(f"发现新商品: {line}")  # 调试信息
        
        # 处理单价
        elif '¥' in line and '/' in line:
            if current_item is not None:
                current_item['单价（元/斤）'] = extract_number(line)
        
        # 处理总价
        elif '¥' in line and '/' not in line:
            if current_item is not None:
                current_item['总价（元）'] = extract_number(line)
        
        # 处理下单数量
        elif '下单数:' in line:
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if ('斤' in next_line or '箱' in next_line) and current_item is not None:
                    current_item['下单数（斤）'] = extract_number(next_line)
                    i += 1
        
        # 处理出库数量
        elif '出库数:' in line:
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if ('斤' in next_line or '箱' in next_line) and current_item is not None:
                    current_item['出库数（斤）'] = extract_number(next_line)
                    i += 1
        
        i += 1

    # 添加最后一个商品的数据
    if current_item is not None:
        data.append(current_item.copy())
        print(f"添加最后一个商品: {current_item['商品名称']}")  # 调试信息

    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 确保所有数值列都是float类型
    numeric_columns = ['单价（元/斤）', '总价（元）', '下单数（斤）', '出库数（斤）']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    print(f"\n总共处理了 {len(data)} 条商品数据")  # 调试信息
    
    # 保存到Excel
    df.to_excel('商品清单0101.xlsx', index=False)
    print("Excel文件已生成：商品清单.xlsx")

if __name__ == '__main__':
    process_text_file('0101.txt')