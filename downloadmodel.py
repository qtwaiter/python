from huggingface_hub import hf_hub_download, login, list_repo_files
import os
from tqdm import tqdm
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

def setup_http_session():
    """设置 HTTP 会话，添加重试机制"""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def extract_repo_id(url):
    """从 Hugging Face URL 中提取 repo_id"""
    # 匹配格式：https://huggingface.co/username/modelname
    match = re.match(r'https?://huggingface\.co/([^/]+/[^/]+)/?.*', url)
    if match:
        return match.group(1)
    raise ValueError("无效的 Hugging Face URL 格式")

def download_model(url):
    # 从 URL 提取 repo_id
    try:
        repo_id = extract_repo_id(url)
    except ValueError as e:
        print(f"错误: {e}")
        return
    
    # 首先尝试从环境变量获取 token
    token = os.getenv("HF_TOKEN")
    
    # 如果环境变量中没有 token，则提示用户输入
    if not token:
        print("未找到环境变量 HF_TOKEN")
        print("请访问 https://huggingface.co/settings/tokens 获取你的 token")
        token = input("请输入你的 Hugging Face token: ").strip()
        if not token:
            raise ValueError("Token 不能为空")
    
    # 登录（带重试机制）
    max_retries = 3
    for attempt in range(max_retries):
        try:
            login(token, add_to_git_credential=True)
            print("登录成功！")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"登录失败，{wait_time} 秒后重试... ({str(e)})")
                time.sleep(wait_time)
            else:
                print(f"登录失败: {str(e)}")
                print("请检查：")
                print("1. 网络连接是否正常")
                print("2. Token 是否正确")
                print("3. 是否可以访问 huggingface.co")
                return

    try:
        # 获取仓库中的所有文件
        print(f"\n正在获取 {repo_id} 的文件列表...")
        files = list_repo_files(repo_id, token=token)
        
        # 创建保存目录（使用 repo_id 的最后一部分作为目录名）
        model_name = repo_id.split('/')[-1]
        save_dir = f"{model_name}_model"
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"\n找到 {len(files)} 个文件需要下载")
        print(f"文件将保存在: {save_dir}")
        
        # 下载每个文件
        for filename in files:
            success = False
            for attempt in range(max_retries):
                try:
                    print(f"\n正在下载 {filename}...")
                    print(f"尝试 {attempt + 1}/{max_retries}")
                    
                    local_file = hf_hub_download(
                        repo_id=repo_id,
                        filename=filename,
                        local_dir=save_dir,
                        local_dir_use_symlinks=False,
                        token=token,
                        force_download=True,
                        resume_download=True
                    )
                    print(f"成功下载 {filename} 到 {local_file}")
                    success = True
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5
                        print(f"下载失败，{wait_time} 秒后重试... ({str(e)})")
                        time.sleep(wait_time)
                    else:
                        print(f"下载 {filename} 失败: {str(e)}")
                        print("请确保：")
                        print("1. Token 是正确的")
                        print("2. 已经在网站上接受了模型的使用条款")
                        print("3. 网络连接正常")
                        return
            
            if not success:
                return
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return

if __name__ == "__main__":
    print("欢迎使用 Hugging Face 模型下载器")
    url = input("请输入 Hugging Face 模型网址 (例如: https://huggingface.co/HKUST-Audio/xcodec2): ").strip()
    
    try:
        download_model(url)
        print("\n下载完成！")
    except KeyboardInterrupt:
        print("\n下载已取消")
    except Exception as e:
        print(f"\n下载出错: {str(e)}")
