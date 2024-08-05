# arixiv-agent/README.md
---
# 中文

# 1. 使用说明

- 运行前先确保python版本大于等于3.9，然后按照`requiments.txt`配置本地`python`环境，并修改`setup.sh`内的python路径
- 为了实现pdf输出，需要手动安装`wkhtmltopdf`软件，并在`main.py`中的`path_wk`配置其路径
- 为了进行企业微信的推送，需要在`main.py`中为`msger`配置正确的key
- 运行`setup.sh`，该脚本检查`python`版本、配置必需的文件夹、为`agent/custom_tools/`下的自定义工具进行注册(如果有的话)
- 在`~/.metagpt/config2.yaml`中为`MetaGPT`配置LLM服务的API，参考：[配置大模型API | MetaGPT (deepwisdom.ai)](https://docs.deepwisdom.ai/main/zh/guide/get_started/configuration/llm_api_configuration.html)
- 使用正确的python环境运行`main.py`，即可运行`MetGPT`框架下的`team`， 包括一个`SimpleCrawler`和一个`Summarizer`。前者爬取当日`arxiv.com`某一搜索结果页面的一定量文章，后者对所有的文章进行分类-归类-总结操作
    
    ```bash
    python ./main.py
    ```
- 当然也可以使用`crontab -e` 设定定时运行计划（使用绝对路径），比如设定每天9点30分，通过`task.sh`运行一次，shell输出到指定的`task.log`文件。为此需要对`task.sh`里的python路径和一些必要的PATH进行设置。
    
    ```bash
    38 9 * * * /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/task.sh > /home/int.orion.que/dev/task.log 2>&1
    ```
- 爬取和总结全部完成后，主进程得到`summary@{today}.md`和`paper@{today}.md`，并将其转换为pdf格式，推送给指定的机器人，要发送的消息可以在`main.py`中配置。
- 每天爬取的记录保存在`output/paperdone.pkl`中，每天爬虫根据这个记录避免重复爬取，详情见后文
- 每天的输出都在`output`下，可以通过在`crontab -e`设定`clear.sh`的定时运行计划清除这些历史数据
    

# 2. 输入配置和输出说明

- 需要配置的主要参数：
    - `main.py`中的路径
    - `main.py`中的机器人key
    - `main.py`中的自定义消息
    - `agent/custom_actions/DataActoins.py`中的爬取目标URL（可以修改URL进行高级搜索的设定）和爬取规模`TaskSize`
    - `agent/custom_actions/TextActoins.py`中的各个prompt
- 每次运行可以得到的输出:
    - `SimpleCrawler`的日志`logs/crawler_{today}.log`
    - `MetaGPT`的日志`logs/{today}.txt`
    - 爬虫爬取的所有文章条目`output/raw/crawler_{today}.json`
    - 通过筛选，保证是新的文章`output/paper@{today}.md`和`output/summary@{today}.pdf`
    - 分类&归类结果`output/summary@{today}.md`和`output/summary@{today}.pdf`
    - 7日内爬取过的所有文章的网址的缓存`output/paperdone.pkl`，是一个字典，key为日期，value是连接的List（由主进程`main.py`自动维护，不要轻易删除，会导致重复爬取）。
    - 如果是`crontab`定时任务，还会在指定的输出位置得到shell的输出`log`文件。

# 3. 项目结构

项目结构如下面描述。

- `agent/`中有三个module，`custom_actions`，`custom_roles`，和`custom_tools`。这些分别是对`MetaGPT`框架下的Action，Role，和Tool元素的定义。具体请看：[智能体入门 | MetaGPT (deepwisdom.ai)](https://docs.deepwisdom.ai/main/zh/guide/tutorials/agent_101.html)。其中`custom_tools`暂时没有用处，如果在其中定义了新的tool，需要通过`setup.sh`为其创建到`MetaGPT`要求目录的链接（根据`MetaGPT`文档要求）。
- `output/`保存所有的非日志输出，包括`json`，`md`，和`pkl`文件。新的总结和文章保存在根目录，其他将保存在对应的文件夹下。
- `tools/`是一个module，包含项目的其他模块代码，如爬虫、数据处理、文件存取、日志、机器人通信等，是最核心的目录。
- `logs/`是日志保存的文件夹。
- `main.py` 是主程序
- `test.py`是测试用的程序
- `task.sh`是定时执行主程序所用的脚本
- `clear.sh`是定时进行缓存清理所用的脚本
- `setup.sh`是配置环境的脚本（功能见1）
- `LICENSE`是项目的开源许可证
- `README.md`即本说明文档
- `requirements.txt`是python环境需求

```bash
arxiv-agent
|agent/
    |——custom_actions/
        |——__init__.py
        |——DataActions.py
        |——TextActions.py
    |——custom_roles/
        |——__init__.py
        |——SimpleCrawler.py
        |——Summarizer.py
    |——custom_tools/
        |——__init__.py
        |——CustomStructedCrawler.py
|output/
    |——paperdone.pkl
    |——outdated/
    |——pdf/
    |——raw/
|tools/
    |——__init__.py
    |——AccessFile.py
    |——Crawler.py
    |——DataProcessor.py
    |——Logger.py
    |——Messenger.py
    |——OutputMD.py
|logs/
|main.py
|test.py
|task.sh
|clear.sh
|setup.sh
|README.md
|LICENSE
|requirements.txt
```

# 4. 有关临时数据

## 4.1 `paperdone.pkl`

- 7日内爬取过的所有文章的网址的缓存`output/paperdone.pkl，`是由主进程自动维护的一个字典的二进制存档，包含过去7天内爬到的每个日期（key）的文章链接（value）。
- 这个字典在`tools/DataProcessor.py`中被使用和维护，用于确定这篇文章是否在过去一周内见过，如果没见过将会加入新条目并保存。
- 这个字典作为过去文章的记录，由主程序`main.py`每次运行时定期清除历史缓存，会检查并删除超过7天范围的条目。
- 因此不要轻易手动删除该文件，否则下一次运行可能会导致重复总结已经总结过的文章。

## 4.2 其他数据

- 其他数据包括上述的每天产生的各种输出。这些缓存将由`./clear.sh`通过同样的`crontab`自动任务进行定时清除。比如下述设置每周一零点进行一次缓存清空。
    
    ```bash
    0 0 * * 1 /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/clear.sh > /home/int.orion.que/dev/clear.log 2>&1
    ```


---
# English Version

Here is the translation of the provided document into English:

# 1. Usage Instructions

- Before running, ensure that your Python version is at least 3.9, then configure your local Python environment according to `requirements.txt`, and modify the Python path in `setup.sh`.
- To enable PDF output, manually install the `wkhtmltopdf` software and configure its path in `path_wk` within `main.py`.
- For enterprise WeChat notifications, configure the correct key for `msger` in `main.py`.
- Run `setup.sh`. This script checks the Python version, sets up necessary folders, and registers custom tools under `agent/custom_tools/` (if any).
- Configure the LLM service API for `MetaGPT` in `~/.metagpt/config2.yaml`. Reference: [Configure Large Model API | MetaGPT (deepwisdom.ai)](https://docs.deepwisdom.ai/main/zh/guide/get_started/configuration/llm_api_configuration.html)
- Run `main.py` using the correct Python environment to launch the `team` under the `MetaGPT` framework, which includes a `SimpleCrawler` and a `Summarizer`. The former scrapes a certain number of articles from a search results page on `arxiv.com` for the day, while the latter categorizes, groups, and summarizes all the articles.
  
  ```bash
  python ./main.py
  ```

- You can also use `crontab -e` to set up a scheduled task (using absolute paths), for example, to run `task.sh` once daily at 9:30 AM, with shell output directed to a specific `task.log` file. You need to configure the Python path and some necessary PATHs in `task.sh`.

  ```bash
  38 9 * * * /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/task.sh > /home/int.orion.que/dev/task.log 2>&1
  ```

- After scraping and summarizing, the main process generates `summary@{today}.md` and `paper@{today}.md`, converts them to PDF format, and sends them to a designated bot. The message to be sent can be configured in `main.py`.
- Daily scraping records are saved in `output/paperdone.pkl`, and each day's crawler uses this record to avoid duplicate scraping. Details are provided later.
- All daily outputs are stored in `output/`, and you can clear these historical data through a scheduled `clear.sh` task set up in `crontab -e`.

# 2. Input Configuration and Output Description

- Main parameters to configure:
    - Paths in `main.py`
    - Bot key in `main.py`
    - Custom messages in `main.py`
    - Scraping target URL and scale (`TaskSize`) in `agent/custom_actions/DataActions.py`
    - Prompts in `agent/custom_actions/TextActions.py`
- Outputs obtained each run:
    - `SimpleCrawler` log: `logs/crawler_{today}.log`
    - `MetaGPT` log: `logs/{today}.txt`
    - All article entries scraped by the crawler: `output/raw/crawler_{today}.json`
    - New articles after filtering: `output/paper@{today}.md` and `output/summary@{today}.pdf`
    - Categorization & grouping results: `output/summary@{today}.md` and `output/summary@{today}.pdf`
    - Cache of all URLs of articles scraped within the last 7 days: `output/paperdone.pkl` (a dictionary where keys are dates and values are lists of links; maintained automatically by the main process `main.py`; do not delete it easily as it may cause duplicate scraping).
    - If using a `crontab` scheduled task, you will also get the shell output `log` file at the specified location.

# 3. Project Structure

The project structure is described as follows:

- `agent/` contains three modules: `custom_actions`, `custom_roles`, and `custom_tools`. These define the Action, Role, and Tool elements under the `MetaGPT` framework. For more details, see: [Agent 101 | MetaGPT (deepwisdom.ai)](https://docs.deepwisdom.ai/main/zh/guide/tutorials/agent_101.html). The `custom_tools` module is currently unused. If new tools are defined here, you need to create links to the required directory via `setup.sh` (as per `MetaGPT` documentation requirements).
- `output/` stores all non-log outputs, including `json`, `md`, and `pkl` files. New summaries and articles are saved in the root directory, while others are saved in corresponding subfolders.
- `tools/` is a module containing other code modules such as crawlers, data processing, file access, logging, and bot communication – the core directory of the project.
- `logs/` is the folder for log files.
- `main.py` is the main program.
- `test.py` is a test program.
- `task.sh` is the script used for scheduling the main program.
- `clear.sh` is the script used for scheduled cache cleaning.
- `setup.sh` is the script for configuring the environment (see section 1 for details).
- `LICENSE` is the open-source license for the project.
- `README.md` is this documentation.
- `requirements.txt` lists the Python environment dependencies.


```bash
arxiv-agent
|-agent/
    |——custom_actions/
        |——__init__.py
        |——DataActions.py
        |——TextActions.py
    |——custom_roles/
        |——__init__.py
        |——SimpleCrawler.py
        |——Summarizer.py
    |——custom_tools/
        |——__init__.py
        |——CustomStructedCrawler.py
|-output/
    |——paperdone.pkl
    |——outdated/
    |——pdf/
    |——raw/
|-tools/
    |——__init__.py
    |——AccessFile.py
    |——Crawler.py
    |——DataProcessor.py
    |——Logger.py
    |——Messenger.py
    |——OutputMD.py
|-logs/
|-main.py
|-test.py
|-task.sh
|-clear.sh
|-setup.sh
|-README.md
|-LICENSE
|-requirements.txt
```

Here is the translation for the additional section:

# 4. Temporary Data

## 4.1 `paperdone.pkl`

- The cache of all URLs of articles scraped within the last 7 days is stored in `output/paperdone.pkl`. This is a binary archive of a dictionary automatically maintained by the main process, containing the links (values) of articles for each date (keys) within the past 7 days.
- This dictionary is used and maintained in `tools/DataProcessor.py` to determine whether an article has been seen within the past week. If not, it adds a new entry and saves it.
- As a record of past articles, this dictionary is periodically cleared by the main program `main.py` when it runs, checking and removing entries that exceed the 7-day range.
- Therefore, do not delete this file manually, as doing so might result in re-summarizing articles that have already been summarized during the next run.

## 4.2 Other Data

- Other data includes various outputs generated daily, as mentioned above. These caches are automatically cleared by `./clear.sh` through the same `crontab` scheduled task. For example, the following setting clears the cache every Monday at midnight.
  
  ```bash
  0 0 * * 1 /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/clear.sh > /home/int.orion.que/dev/clear.log 2>&1
  ```