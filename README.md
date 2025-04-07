# 豆瓣电影Top250爬虫

这是一个用于爬取豆瓣电影Top250信息及其评论的Python爬虫项目。爬虫会收集电影详细信息和用户评论，并将数据存储到MySQL数据库中。

## 功能特性

- 爬取豆瓣电影Top250列表
- 抓取每部电影的详细信息（导演、演员、评分等）
- 收集每部电影的用户评论
- 数据存储至MySQL数据库

## 环境要求

- Python 3.6+
- MySQL数据库服务器

## 安装指南

1. 克隆或下载此项目到本地

2. 安装依赖库:
   ```
   pip install -r requirements.txt
   ```

3. 配置MySQL数据库:
   - 确保MySQL服务正在运行
   - 修改数据库连接信息（如需要）:
     - 默认连接信息: 
       - 主机: localhost
       - 用户名: root
       - 密码: password
       - 数据库名: movies (将自动创建)

## 一键执行

运行以下命令启动爬虫:

```
python run.py
```

## 数据库结构

程序将创建两个数据表:

1. **movies_list** - 存储电影基本信息
   - id, top25No, title, year, director, scriptwriter, lead_performer, genre等字段

2. **comments_list** - 存储电影评论
   - id, movie_id, user, star, time, useful, content等字段

## 注意事项

- 爬虫使用随机Cookie来避免被反爬虫机制阻止
- 默认每部电影爬取3页评论
- 网络请求过于频繁可能导致IP被暂时封禁，请合理控制爬取频率
