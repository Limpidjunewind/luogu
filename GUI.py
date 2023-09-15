import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import os

# 创建GUI窗口
window = tk.Tk()
window.title("洛谷题目爬取工具")

# 定义GUI界面元素和函数
def crawl_luogu():
    # 获取用户输入的筛选条件
    difficulty = difficulty_var.get()
    keywords = keywords_var.get()

    # 发送HTTP请求，爬取洛谷页面
    url = f"https://www.luogu.org/problem/list?difficulty={difficulty}&keyword={keywords}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 解析页面，获取题目信息
    problems = soup.find_all("div", class_="problem-set")

    for problem in problems:
        # 提取题目信息
        title = problem.find("span", class_="title").text
        problem_id = problem.find("span", class_="problem-id").text

        # 创建题目文件夹
        folder_name = f"{difficulty}-{keywords}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # 创建题目markdown文件
        with open(f"{folder_name}/{problem_id}-{title}.md", "w") as f:
            f.write(f"# {problem_id} - {title}\n\n")
            # 爬取题目内容并写入文件

        # 创建题解markdown文件
        with open(f"{folder_name}/{problem_id}-{title}-题解.md", "w") as f:
            f.write(f"# {problem_id} - {title} 题解\n\n")
            # 爬取题解内容并写入文件

# 创建GUI界面元素
difficulty_label = tk.Label(window, text="题目难度：")
difficulty_var = tk.StringVar()
difficulty_combobox = ttk.Combobox(window, textvariable=difficulty_var, values=[
    "暂无评定入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"
])

keywords_label = tk.Label(window, text="关键词：")
keywords_var = tk.StringVar()
keywords_entry = tk.Entry(window, textvariable=keywords_var)

crawl_button = tk.Button(window, text="开始爬取", command=crawl_luogu)

# 布局GUI界面元素
difficulty_label.grid(row=0, column=0)
difficulty_combobox.grid(row=0, column=1)
keywords_label.grid(row=1, column=0)
keywords_entry.grid(row=1, column=1)
crawl_button.grid(row=2, columnspan=2)

# 启动GUI
window.mainloop()
