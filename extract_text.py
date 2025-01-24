import re
from bs4 import BeautifulSoup

def clean_html_content(html):
    # 移除所有HTML标签（加强版）
    soup = BeautifulSoup(html, 'lxml')
    
    # 新增：显式移除所有标签但保留内容
    for tag in soup.find_all(True):
        tag.unwrap()
    
    text = soup.get_text(separator='\n', strip=True)
    
    # 新增：二次过滤残留标签
    text = re.sub(r'<[^>]+>', '', text)  # 移除任何残留的HTML标签
    
    # 移除Twine脚本标记
    text = re.sub(r'<<.*?>>', '', text)
    
    # 处理转义字符
    text = text.replace('\\s', ' ').replace('\\n', '\n')
    
    # 移除残留的代码片段
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)  # 移除CSS注释
    text = re.sub(r'//.*', '', text)  # 移除JS单行注释
    
    # 保留角色对话格式
    dialogue_lines = []
    for line in text.split('\n'):
        line = line.strip()
        # 改进的角色对话检测（支持带空格的类名）
        if re.match(r'^([A-Z][a-z]+\s*)+(?::|：)', line):  
            dialogue_lines.append(line)
        elif line and not any(char in line for char in {'{', '}'}):
            dialogue_lines.append(line)
    
    # 合并空行并格式优化
    cleaned_text = '\n'.join([line for line in dialogue_lines if line])
    return re.sub(r'\n{3,}', '\n\n', cleaned_text)  # 合并多个空行

def process_html_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    cleaned_text = clean_html_content(html)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract English text from HTML')
    parser.add_argument('-i', '--input', required=True, help='Input HTML file path')
    parser.add_argument('-o', '--output', default='output.txt', help='Output text file path')
    
    args = parser.parse_args()
    process_html_file(args.input, args.output)
