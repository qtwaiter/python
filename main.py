import pandas as pd
import random

def random_select_names(input_file, output_file, num_select):
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file)
        
        # 确保必要的列存在
        required_columns = ['姓名', '床位号', '护理等级']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f'Excel文件中缺少必要的列：{col}')
        
        # 如果要抽取的数量大于总行数，则调整为总行数
        num_select = min(num_select, len(df))
        
        # 随机抽取指定数量的行
        selected_rows = df.sample(n=num_select)
        
        # 只保留需要的列
        result_df = selected_rows[required_columns]
        
        # 导出到新的Excel文件
        result_df.to_excel(output_file, index=False)
        print(f'成功随机抽取{num_select}个名单并保存到{output_file}')
        
    except Exception as e:
        print(f'发生错误：{str(e)}')

def main():
    input_file = 'name.xlsx'
    output_file = 'random_selected_names.xlsx'
    
    while True:
        try:
            num_select = int(input('请输入需要随机抽取的人数：'))
            if num_select <= 0:
                print('请输入大于0的数字')
                continue
            break
        except ValueError:
            print('请输入有效的数字')
    
    random_select_names(input_file, output_file, num_select)

if __name__ == '__main__':
    main()