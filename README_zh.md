# JobsDB 职位爬虫

这是一个基于 Python 的异步爬虫，用于从 [JobsDB 香港站](https://hk.jobsdb.com) 抓取职位数据，使用官方 API 接口，支持并发控制和灵活配置。

📖 English version: [README.md](README.md)

## 🚀 项目特点

- 基于 `aiohttp` 实现异步高性能抓取
- 支持关键词、多工作类型、多页并发抓取
- 自动获取总页数，无需提前设置
- 日志支持文件和控制台输出，兼容 tqdm
- 结构化提取职位分类、地点、薪资等字段
- 支持 UTF-8 带 BOM 输出（Excel 友好）

## 🛠️ 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 启动爬虫
python main.py
```

## ⚙️ 配置说明（config.yaml）

```yaml
site_key: HK-Main
locale: en-HK
keywords: Operation # 可多选，例如：Operation,Marketing
work_type: 242 # 可多选，例如：242,243
page_size: 32
max_page: -1 # -1 表示抓取所有页面

concurrent_limit: 10
output_dir: output/
log_dir: logs/
log_level: INFO
enable_console: true
skip_existing: true
```

## 📁 项目结构

```
.
├── config.yaml          # 爬虫配置文件
├── main.py              # 入口函数
├── fetcher.py           # 发起请求
├── parser.py            # 解析字段
├── saver.py             # 保存为 CSV
├── logger.py            # 日志记录
├── requirements.txt
├── output/              # 输出目录
├── logs/                # 日志目录
```

## 📦 依赖组件

- `aiohttp`
- `pyyaml`
- `tqdm`

## 📌 注意事项

- 程序会先抓取第一页以获取职位总数 (`totalCount`)，再决定总抓取页数。
- 当 `max_page: -1` 时，表示不设抓取页数上限，全部抓取。
