import requests
from bs4 import BeautifulSoup
import os
import time
import re

# 映射难度等级
difficulty_dict = {
    1: "入门",
    2: "普及-",
    3: "普及/提高-",
    4: "提高+/省选-",
    5: "省选/NOI-",
    6: "NOI/NOI+/CTSC-",
    7: "CTSC/NOI+/NOI++"
}

def navigateToLuoguDifficultyPage(difficulty, keyword, a):
    base_url = "https://www.luogu.com.cn/problem/list?difficulty="
    
    # 检查用户输入的难度等级是否有效
    if difficulty < 1 or difficulty > 7:
        print("无效的难度等级。")
        return
    
    # 构建对应难度等级的网页链接
    url = base_url + str(difficulty)
    
    # 发送请求跳转到网页
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # 检查是否成功跳转
    if response.status_code == 200:
        print(f"成功跳转到难度等级 {difficulty} 的网页。")
        
        # 使用Beautiful Soup解析页面内容
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # 使用选择器定位所有的<li>标签
        problem_elements = soup.select('li')
        
        # 初始化保存的题目计数器
        saved_count = 0
        
        for problem_element in problem_elements:
            # 如果已保存的题目数量达到a，则退出循环
            if saved_count >= a:
                break

            # 使用正则表达式提取题目编号和标题
            text = problem_element.get_text()
            match = re.match(r'P(\d+)\s+(.*)', text)
            if match:
                problem_id = match.group(1)
                problem_title = match.group(2)
                problem_link = "https://www.luogu.com.cn/problem/P" + problem_id
                # 如果用户输入了关键词并且匹配成功，爬取题目内容并保存为Markdown文件
                if keyword and keyword.lower() in problem_title.lower():
                    print(f"正在保存编号为 {problem_id}，题目为 {problem_title} 的问题（问题链接: {problem_link})")
                    problem_info = {
                        "id": problem_id,
                        "title": problem_title,
                        "link": problem_link,
                        "markdown": getProblemMarkdown(problem_link)
                    }
                    saveProblemMarkdown(problem_info)
                    saved_count += 1
                elif not keyword:  # 如果用户未输入关键词，直接保存题目内容
                    print(f"正在保存编号为 {problem_id}，题目为 {problem_title} 的问题（问题链接: {problem_link})")
                    problem_info = {
                        "id": problem_id,
                        "title": problem_title,
                        "link": problem_link,
                        "markdown": getProblemMarkdown(problem_link)
                    }
                    saveProblemMarkdown(problem_info)
                    saved_count += 1

            time.sleep(2)

    else:
        print(f"无法跳转到难度等级 {difficulty} 的网页。状态码：{response.status_code}")

def getProblemMarkdown(url):
    # 发送请求跳转到题目页面
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # 检查是否成功跳转
    if response.status_code == 200:
        # 使用Beautiful Soup解析页面内容
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        # 获取题目的Markdown内容
        problem_md = soup.find("article").prettify()
        return problem_md
    
    else:
        print(f"无法跳转到题目页面。状态码：{response.status_code}")
        return ""

def saveProblemMarkdown(problem_info):
    folder_name = f"P{problem_info['id']}-{problem_info['title']}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # 构建Markdown文件名
    filename = f"P{problem_info['id']}-{problem_info['title']}.md"
    # 构建Markdown文件路径
    file_path = os.path.join(folder_name, filename)
    # 保存Markdown内容到文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(problem_info["markdown"])
        print(f"已保存为 {filename}")

if __name__ == '__main__':
    difficulty = int(input("请输入难度等级（1-7）："))
    keyword = input("请输入关键词（如果需要匹配题目，请输入关键词；否则，直接按回车）：")
    a = int(input("请输入需要保存的题目数量 a："))
    navigateToLuoguDifficultyPage(difficulty, keyword, a)
