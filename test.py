import os
from markitdown import MarkItDown

# 获取用户输入的文件路径
input_file = input("请输入要转换的Excel文件路径: ")

# 检查文件是否存在
if not os.path.exists(input_file):
    print(f"文件 {input_file} 不存在")
    exit()

markitdown = MarkItDown()
result = markitdown.convert(input_file)
print(result.text_content)

# 生成输出文件名
output_file = os.path.splitext(input_file)[0] + ".md"

# 将转换结果导出到 Markdown 文件
with open(output_file, "w", encoding="utf-8") as md_file:
    md_file.write(result.text_content)

print(f"转换完成，结果已保存到 {output_file}")
