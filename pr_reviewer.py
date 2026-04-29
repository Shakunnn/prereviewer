import os
import requests
from openai import OpenAI

def get_pr_diff(repo, pr_number, github_token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def analyze_code_with_ai(diff_text, api_key, base_url="https://api.openai.com/v1"):
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    system_prompt = """
    你是一个资深的研发架构师和严格的代码审查员 (Reviewer Agent)。
    请分析以下 GitHub PR 的代码变更 (Diff)。
    你需要关注：
    1. 代码逻辑是否存在潜在 Bug 或死循环？
    2. 是否存在安全漏洞（如 SQL 注入、XSS、越权）？
    3. 性能是否有优化空间？
    4. 代码规范性。
    请用 Markdown 格式输出审查报告，包含【总结】、【存在的问题】、【修改建议】。如果代码很好，请给予肯定。
    """
    
    max_diff_length = 20000 
    if len(diff_text) > max_diff_length:
        diff_text = diff_text[:max_diff_length] + "\n\n...[Diff too long, truncated]..."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # 如果使用其他模型，请替换模型名称，例如 "deepseek-chat" 或 "glm-4"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"以下是本次 PR 的代码变更：\n\n{diff_text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def post_comment_to_pr(repo, pr_number, github_token, comment_body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": f"🤖 **AI Agent Code Review Report** 🤖\n\n{comment_body}"}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("AI 审查评论已成功发布！")

if __name__ == "__main__":
    GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
    PR_NUMBER = os.environ.get("PR_NUMBER")
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    
    # 你的大模型 API 密钥
    AI_API_KEY = os.environ.get("AI_API_KEY")
    
    AI_BASE_URL = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1")

    print(f"开始审查 PR: {GITHUB_REPOSITORY} #{PR_NUMBER}")
    
    try:
        diff_text = get_pr_diff(GITHUB_REPOSITORY, PR_NUMBER, GITHUB_TOKEN)
        print("已获取代码变更...")
        
        print("Agent 正在深度分析代码...")
        review_result = analyze_code_with_ai(diff_text, AI_API_KEY, AI_BASE_URL)
        
        post_comment_to_pr(GITHUB_REPOSITORY, PR_NUMBER, GITHUB_TOKEN, review_result)
        
    except Exception as e:
        print(f"运行出错: {e}")
