import json

# 输入的数据
tags = [
    "Kruskal 重构树",
    "网络流",
    "图论建模",
    "图遍历",
    "拓扑排序",
    "最短路",
    "K 短路",
    "生成树",
    "平面图",
    "最小环",
    "负权环",
    "连通块",
    "2-SAT",
    "欧拉公式",
    "强连通分量",
    "Tarjan",
    "双连通分量",
    "欧拉回路",
    "差分约束",
    "仙人掌",
    "二分图",
    "一般图的最大匹配",
    "最大流",
    "上下界网络流",
    "最小割",
    "费用流",
    "圆方树",
    "Dilworth 定理"
]

category_ids = [
    6, 68, 79, 155, 158, 159, 160, 165, 166, 172, 173, 174, 175, 176, 177, 179, 180, 181, 182, 185, 186, 187, 189, 194, 197, 198, 204, 350, 364
]

# 创建标签和分类编号的字典
tag_to_category = dict(zip(tags, category_ids))

# 指定要保存的 JSON 文件路径
json_file_path = "tags_to_categories1.json"

# 将字典写入 JSON 文件
with open(json_file_path, "w") as json_file:
    json.dump(tag_to_category, json_file, indent=4)

print(f"已将标签和分类信息保存到 {json_file_path} 文件中。")
