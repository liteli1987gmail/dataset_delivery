import os
import sys

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# 获取脚本所在的目录
script_dir = os.path.dirname(script_path)

# 获取项目的根目录
root_dir = os.path.dirname(script_dir)

# 获取 src 目录的路径
src_dir = os.path.join(root_dir, 'src')
print(src_dir)
# 将 src 目录添加到 sys.path
sys.path.append(src_dir)

import replace_pronouns as pronouns_agent

if __name__ == "__main__":
    country = "China"

    relative_path = "sample-texts/sample-short1.txt"
    script_dir = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(script_dir, relative_path)

    with open(full_path, encoding="utf-8") as file:
        source_text = file.read()

    print(f"Source text:\n\n{source_text}\n------------\n")

    replacement = pronouns_agent.replace_pronouns_names(
        source_text=source_text,
        country=country,
    )
    print(f"Replacement:\n\n{replacement}")

    # 将结果写入一个新的text文件中，文件名为replacement_result.txt
    with open("replacement_result.txt", "w", encoding="utf-8") as file:
        file.write(replacement)
