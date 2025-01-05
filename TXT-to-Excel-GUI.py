import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def extract_number(text):
    if isinstance(text, str):
        text = text.replace(',', '')
        numbers = re.findall(r'\d+\.?\d*', text)
        return float(numbers[0]) if numbers else 0
    return text

def is_product_name(line):
    if any(keyword in line for keyword in ['¥', '下单数:', '出库数:']):
        return False
    if re.match(r'^[\d.,]+\s*(斤|箱)$', line.strip()):
        return False
    return True

def process_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        data = []
        current_item = None
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
                
            if is_product_name(line):
                if current_item is not None:
                    data.append(current_item.copy())
                
                current_item = {
                    '商品名称': line,
                    '单价（元/斤）': 0,
                    '总价（元）': 0,
                    '下单数（斤）': 0,
                    '出库数（斤）': 0
                }
            
            elif '¥' in line and '/' in line:
                if current_item is not None:
                    current_item['单价（元/斤）'] = extract_number(line)
            
            elif '¥' in line and '/' not in line:
                if current_item is not None:
                    current_item['总价（元）'] = extract_number(line)
            
            elif '下单数:' in line:
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if ('斤' in next_line or '箱' in next_line) and current_item is not None:
                        current_item['下单数（斤）'] = extract_number(next_line)
                        i += 1
            
            elif '出库数:' in line:
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if ('斤' in next_line or '箱' in next_line) and current_item is not None:
                        current_item['出库数（斤）'] = extract_number(next_line)
                        i += 1
            
            i += 1

        if current_item is not None:
            data.append(current_item.copy())

        df = pd.DataFrame(data)
        
        numeric_columns = ['单价（元/斤）', '总价（元）', '下单数（斤）', '出库数（斤）']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # 生成输出文件名
        output_path = os.path.splitext(file_path)[0] + '_转换结果.xlsx'
        df.to_excel(output_path, index=False)
        
        return True, f"成功处理 {len(data)} 条数据\n保存至：{output_path}"
    
    except Exception as e:
        return False, f"处理失败：{str(e)}"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TXT转Excel工具")
        self.root.geometry("500x300")
        
        # 设置窗口图标
        try:
            self.root.iconbitmap("icon.ico")  # 如果有图标文件的话
        except:
            pass
        
        # 创建主框架
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # 标题标签
        title_label = tk.Label(main_frame, text="菜篮子数据转换工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 说明文本
        instruction_text = "使用说明：\n1. 点击\"选择文件\"按钮选择要转换的TXT文件\n2. 程序会自动生成Excel文件在相同目录下"
        instruction_label = tk.Label(main_frame, text=instruction_text, justify='left')
        instruction_label.pack(pady=(0, 20))
        
        # 按钮
        self.select_button = tk.Button(main_frame, text="选择文件", command=self.select_file, width=20)
        self.select_button.pack(pady=(0, 10))
        
        # 状态显示
        self.status_text = tk.Text(main_frame, height=5, width=50)
        self.status_text.pack(pady=(10, 0))
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择TXT文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"正在处理文件：{file_path}\n")
            self.root.update()
            
            success, message = process_text_file(file_path)
            
            self.status_text.insert(tk.END, message)
            if success:
                messagebox.showinfo("成功", message)
            else:
                messagebox.showerror("错误", message)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main() 