# 豆瓣电影Top250爬虫

这是一个用于爬取豆瓣电影Top250信息及其评论的Python爬虫项目。爬虫会收集电影详细信息和用户评论，并将数据存储到MySQL数据库中。

## 功能特性

- 爬取豆瓣电影Top250列表
- 抓取每部电影的详细信息（导演、演员、评分等）
- 收集每部电影的用户评论（每部电影默认收集3页评论）
- 数据存储至MySQL数据库
- 防反爬机制（使用随机Cookie）

## 项目结构

```
Web Crawler on Douban/
│
├── run.py                  # 主执行文件
├── douban_crawler.py       # 爬虫核心代码
├── requirements.txt        # 项目依赖
├── movies.sql              # 数据库导出文件
├── README.md               # 项目说明
└── LICENSE                 # MIT许可证
```

## 环境要求

- Python 3.6+
- MySQL数据库服务器
- 以下Python库：
  - requests>=2.25.0
  - beautifulsoup4>=4.9.3
  - pymysql>=1.0.2

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

### 数据表设计

程序将创建两个数据表:

1. **movies_list** - 存储电影基本信息
   - `id`: INT (主键，自增)
   - `top25No`: VARCHAR(20) - Top250中的排名
   - `title`: VARCHAR(100) - 电影标题
   - `year`: VARCHAR(20) - 上映年份
   - `director`: VARCHAR(1000) - 导演
   - `scriptwriter`: VARCHAR(1000) - 编剧
   - `lead_performer`: VARCHAR(1000) - 主演
   - `genre`: VARCHAR(100) - 电影类型
   - `produced_country_or_region`: VARCHAR(100) - 制片国家/地区
   - `language`: VARCHAR(50) - 语言
   - `initial_release_date`: VARCHAR(200) - 上映日期
   - `runtime`: VARCHAR(50) - 片长
   - `also_known_as`: VARCHAR(200) - 别名
   - `IMDb`: VARCHAR(30) - IMDb编号
   - `official_site`: VARCHAR(100) - 官方网站
   - `summary`: VARCHAR(2000) - 电影简介
   - `rating`: VARCHAR(20) - 评分
   - `nums_of_rating_people`: VARCHAR(20) - 评分人数
   - `ratings_on_weight`: VARCHAR(100) - 评分分布
   - `rating_betterthan`: VARCHAR(100) - 好于同类电影比例
   - `comments_site`: VARCHAR(100) - 评论页面链接

2. **comments_list** - 存储电影评论
   - `id`: INT (主键，自增)
   - `movie_id`: INT - 关联电影ID（外键）
   - `user`: VARCHAR(50) - 评论用户
   - `star`: VARCHAR(20) - 用户评分
   - `time`: VARCHAR(50) - 评论时间
   - `useful`: VARCHAR(40) - 有用数量
   - `content`: VARCHAR(2000) - 评论内容

## 实现细节

- 使用BeautifulSoup解析HTML内容
- 通过递归查找和CSS选择器提取页面信息
- 采用随机Cookie策略减少被封风险
- 通过关系数据库存储结构化数据
- 对不同类型电影信息使用不同的解析策略

## 注意事项

- 爬虫使用随机Cookie来避免被反爬虫机制阻止
- 默认每部电影爬取3页评论
- 网络请求过于频繁可能导致IP被暂时封禁，请合理控制爬取频率
- 请遵守豆瓣网站的使用条款，合理使用爬虫

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。
```
