"""
豆瓣电影Top250爬虫
主执行文件 - 启动爬虫程序
"""
import os
import sys
import subprocess

def main():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建爬虫文件的路径
    crawler_path = os.path.join(current_dir, "douban_crawler.py")
    
    # 检查文件是否存在
    if not os.path.exists(crawler_path):
        print(f"错误：找不到爬虫文件 '{crawler_path}'")
        return 1
    
    print("开始执行豆瓣电影Top250爬虫...")
    try:
        # 执行爬虫脚本
        result = subprocess.run([sys.executable, crawler_path], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"爬虫执行失败: {e}")
        return e.returncode
    except Exception as e:
        print(f"发生错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())