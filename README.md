# arixiv-agent/README.md
---
# 中文

# 1. 使用说明

- 运行前先按照`requiments.txt`配置本地`python`环境
- 然后运行`setup.sh`，该脚本检查`python`版本、配置必需的文件夹、为`agent/custom_tools/`下的自定义工具进行注册
- 在`~/.metagpt/config2.yaml`中为`MetaGPT`配置LLM服务的API，参考：[配置大模型API | MetaGPT (deepwisdom.ai)](https://docs.deepwisdom.ai/main/zh/guide/get_started/configuration/llm_api_configuration.html)
- 运行`main.py`，即可运行`MetGPT`框架下的`team`， 包括一个`SimpleCrawler`和一个`Summarizer`。前者爬取当日`arxiv.com`某一搜索结果页面的一定量文章，后者对所有的文章进行分类-归类操作。全部完成后，主进程推送`summary@{today}.md`和`paper@{today}.md` 给指定的微信群机器人
    
    ```bash
    python ./main.py
    ```
    
- 当然也可以使用`crontab -e` 设定定时运行计划（使用绝对路径），比如设定每天9点30分，通过`task.sh`运行一次，shell输出到指定的`task.log`文件
    
    ```bash
    38 9 * * * /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/task.sh > /home/int.orion.que/dev/task.log 2>&1
    ```
    

# 2. 输入配置和输出说明

- 需要配置的主要参数：
    - `main.py`中的路径
    - `main.py`中的机器人key
    - `main.py`中的自定义消息
    - `agent/custom_actions/DataActoins.py`中的爬取目标URL（可以修改URL进行高级搜索的设定）和爬取规模`TaskSize`
    - `agent/custom_actions/DataActoins.py`中的日期范围`inDatedThreshold`*，*是距离当前日期的最大范围，只有在该范围内的文章会被发送给`Summarizer`
    - `agent/custom_actions/TextActoins.py`中的各个prompt
- 每次运行可以得到的输出:
    - `SimpleCrawler`的日志`logs/crawler_{today}.log`
    - `Summarizer`的日志`logs/{today}.txt`
    - 爬虫爬取的未经日期判别分类的所有文章条目`output/raw/crawler_{today}.json`
    - 符合`inDatedThreshold`要求的所有文章`output/paper@{today}.md`
    - 不符合`inDatedThreshold`要求的各日期的文章`output/oudated/paper@{date}.md`
    - 符合`inDatedThreshold`要求的所有文章的分类&归类结果`output/summary@{today}.md`
    - 7日内爬取过的所有文章的网址的缓存`output/paperdone.pkl`，（由主进程自动维护，不要轻易删除，会导致重复爬取）。
    - 如果是`crontab`定时任务，还会在指定的输出位置得到`shell`的输出`log` 文件。

# 3. 项目结构

项目结构如下面描述。

- `agent/`中有三个module，`custom_actions`，`custom_roles`，和`custom_tools`。这些分别是对`MetaGPT`框架下的Action，Role，和Tool元素的定义。具体请看：[智能体入门 | MetaGPT (deepwisdom.ai)](https://docs.deepwisdom.ai/main/zh/guide/tutorials/agent_101.html)。其中`custom_tools`暂时没有用处，如果在其中定义了新的tool，需要通过`setup.sh`为其创建到`MetaGPT`要求目录的硬链接（根据`MetaGPT`文档要求）。
- `output/`保存所有的非日志输出，包括`json`，`md`，和`pkl`文件。新的总结和文章保存在根目录，其他将保存在对应的文件夹下。
- `tools/`是一个module，包含项目的其他模块代码，如爬虫、数据处理、文件存取、日志、机器人通信等，是最核心的目录。
- `logs/`是日志保存的文件夹。
- `main.py` 是主程序
- `test.py`是测试用的程序
- `task.sh`是定时执行主程序所用的脚本
- `clear.sh`是定时进行缓存清理所用的脚本
- `setup.sh`是配置环境的脚本（功能见1）
- `LICENSE`是GPLv3.0，这表明本项目是开源的
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

# 4. 有关缓存

## 4.1 `paperdone.pkl`

- 7日内爬取过的所有文章的网址的缓存`output/paperdone.pkl，`是由主进程自动维护的一个字典的二进制存档，包含过去7天内爬到的每个日期（key）的文章链接（value）。
- 这个字典在`tools/DataProcessor.py`中被使用，用于确定这篇文章是否在过去一周内见过，如果没见过将会加入新条目并保存。
- 这个字典作为过去文章的记录，由主程序`main.py`每次运行时维护，会检查是否有超过7天范围的日期key，有的话删除。
- 因此不要轻易手动删除该文件，否则下一次运行可能会导致重复总结已经总结过的文章。

## 4.2 其他缓存

- 其他缓存包括上述的每天产生的各种输出。这些缓存将由`./clear.sh`通过同样的`crontab`自动任务进行定时清除。比如下述设置每周一零点进行一次缓存清空。
    
    ```bash
    0 0 * * 1 /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/clear.sh > /home/int.orion.que/dev/clear.log 2>&1
    ```


---
# English Version

# 1. **Usage Instructions**

   Before running, configure the local Python environment according to `requirements.txt`.

   Then, execute `setup.sh`. This script checks the Python version, sets up necessary directories, and registers custom tools under `agent/custom_tools/`.

   In `~/.metagpt/config2.yaml`, configure the API for the LLM service of MetaGPT. Reference: "Configure Large Model API | MetaGPT (deepwisdom.ai)"

   Run `main.py` to operate the team under the MetGPT framework, which includes a SimpleCrawler and a Summarizer. The former crawls a certain number of articles from a search result page on arxiv.com for the current day, and the latter classifies and categorizes all articles. After completion, the main process pushes `summary@{today}.md` and `paper@{today}.md` to a specified WeChat bot.

   ```bash
   python ./main.py
   ```

   You can also set up a scheduled run using `crontab -e` (using absolute paths), for example, to run once through `task.sh` at 9:30 AM every day, with shell output directed to a specified `task.log` file.

   ```bash
   38 9 * * * /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/task.sh > /home/int.orion.que/dev/task.log 2>&1
   ```

# 2. **Input Configuration and Output Description**

   Key configurations needed:

   - Paths in `main.py`
   - Bot key in `main.py`
   - Custom messages in `main.py`
   - Target URL for crawling in `agent/custom_actions/DataActions.py` (you can modify the URL for advanced search settings) and the scale of the crawl TaskSize
   - Date range in `agent/custom_actions/DataActions.py` for inDatedThreshold, which is the maximum range from the current date. Only articles within this range will be sent to the Summarizer
   - Various prompts in `agent/custom_actions/TextActions.py`

   Output obtained each time:

   - Logs for SimpleCrawler: `logs/crawler_{today}.log`
   - Logs for Summarizer: `logs/{today}.txt`
   - All articles crawled by the crawler without date discrimination and classification: `output/raw/crawler_{today}.json`
   - All articles that meet the inDatedThreshold requirements: `output/paper@{today}.md`
   - Articles from each date that do not meet the inDatedThreshold requirements: `output/outdated/paper@{date}.md`
   - Classification & categorization results for all articles that meet the inDatedThreshold requirements: `output/summary@{today}.md`
   - Cache of URLs for all articles crawled within the past 7 days: `output/paperdone.pkl` (automatically maintained by the main process, do not delete carelessly to avoid re-crawling).
   - If it's a crontab scheduled task, you will also get the shell output log file at the specified output location.

# 3. **Project Structure**

   The project structure is described as follows.

   * Inside the `agent/` directory, there are three modules: `custom_actions`, `custom_roles`, and `custom_tools`. These correspond to the definitions of the Action, Role, and Tool elements under the MetaGPT framework, respectively. For more details, see: "Agent Introduction | MetaGPT (deepwisdom.ai)". The `custom_tools` are currently not in use. If you define a new tool within it, you need to create a hard link to the MetaGPT required directory through `setup.sh` according to the MetaGPT documentation.

   * `output/` saves all non-log outputs, including JSON, MD, and PKL files. New summaries and articles are saved in the root directory, and others are saved in the corresponding folders.

   * `tools/` is a module that contains other module codes of the project, such as crawler, data processing, file storage, logs, bot communication, etc. It is the most core directory.

   * `logs/` is the folder where logs are saved.

   * `main.py` is the main program.

   * `test.py` is the test program.

   * `task.sh` is the script used for timed execution of the main program.

   * `clear.sh` is the script used for timed cache cleaning.

   * `setup.sh` is the script for environment configuration (functions as seen in 1).

   * `LICENSE` is GPLv3.0, indicating that this project is open source.

   * `README.md` is this documentation.

   * `requirements.txt` lists the Python environment requirements.

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

# 4. **About Caching**

   ## 4.1 `paperdone.pkl`

   The cache of URLs for all articles crawled within the past 7 days, `output/paperdone.pkl`, is a binary archive of a dictionary automatically maintained by the main process. It contains links to articles crawled each day (value) for the past 7 days (key).

   This dictionary is used in `tools/DataProcessor.py` to determine if an article has been seen in the past week. If not, a new entry will be added and saved.

   As a record of past articles, this dictionary is maintained by the main program `main.py` during each run, checking for and removing any date keys that exceed the 7-day range.

   Therefore, do not manually delete this file carelessly, as the next run may result in the re-summation of articles that have already been summarized.

   ## 4.2 Other Caches

   Other caches include the various outputs generated each day. These caches will be automatically cleared by `./clear.sh` through the same crontab scheduled task. For example, the following setting clears the cache once a week at midnight.

   ```bash
   0 0 * * 1 /bin/bash /home/int.orion.que/dev/my_programs/arxiv-agent/clear.sh > /home/int.orion.que/dev/clear.log 2>&1
   ```