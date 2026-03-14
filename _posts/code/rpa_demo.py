import json, os, tempfile, logging
from typing import Callable, Optional
from DrissionPage import ChromiumPage, ChromiumOptions
from openpyxl import Workbook

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

DATA_FILE = "datacache.json"
OUTPUT_FILE = "帖子数据.xlsx"
EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

def safe_modify_file(
    target_path: str,
    processor: Callable[[str, str], None]
) -> None:
    """
    原子操作文件
    Args:
        target_path: 要修改的目标文件路径
        processor: 业务逻辑函数 (源文件路径, 临时输出路径)
                   注意：源文件可能不存在，需自行处理 FileNotFoundError
    """
    target_dir = os.path.dirname(os.path.abspath(target_path))
    os.makedirs(target_dir, exist_ok=True) # 确保目标目录存在
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=target_dir, delete=False) as f:
            tmp_path = f.name
        processor(target_path, tmp_path) # 调用业务逻辑
        os.replace(tmp_path, target_path)
    except Exception as e:
        if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)
        raise e

def load_saved(file): 
    data = []
    if os.path.exists(file):
        for line in open(file, 'r', encoding='utf-8'):
            if line.strip():
                data.append(json.loads(line))
    return data

''' 
演示在线非商业网页自动化: https://quotes.toscrape.com/
进行登录;
获取Top Ten tags,并获取每个标签第一个帖子的内容,保存至xlsx文件。
'''
def main():

    co = ChromiumOptions().set_browser_path(EDGE_PATH).ignore_certificate_errors()
    
    tab = ChromiumPage(addr_or_opts=co, timeout = 5).get_tab()
    tab.get('https://quotes.toscrape.com/')

    if tab.s_ele('Logout', timeout = 1) is None: # 如果没有找到Logout元素，说明未登录
        tab('Login').click()
        tab('#username').input('admin')
        tab('#password').input('passwd')
        tab('@class:btn btn-primary').click()

    eles = tab('@class:col-md-4 tags-box').eles('@class:tag-item')
    logging.info("获取标签列表")
    tags = [ele.text for ele in eles]
    logging.info(f"获取到{len(tags)}个标签")

    saved = load_saved(DATA_FILE)
    saved_tags = {item['标签'] for item in saved} if saved else set()
    tags = [tag for tag in tags if tag not in saved_tags]
    logging.info(f"已保存可跳过: {len(saved_tags)}。待处理: {len(tags)}")

    data_buffer: List[Dict]  = []
    try:
        for tag in tags:
            tab.get(f"https://quotes.toscrape.com/tag/{tag}/")
            text = tab.s_ele('@class:quote').text
            data_buffer.append({'标签': tag, '内容': text})
    except Exception as e:
        logging.error(f"操作标签时发生错误: {e}")
        raise e
    finally:
        if data_buffer:
            def writer(src, tmp):
                combined = saved.copy()         # 读旧
                combined.extend(data_buffer)    # 加新
                with open(tmp, 'w', encoding='utf-8') as f:
                    for d in combined:
                        print(json.dumps(d, ensure_ascii=False), file=f)

            safe_modify_file(DATA_FILE, writer)
            logging.info(f"追加 {len(data_buffer)} 条数据到 {DATA_FILE}")

    logging.info("所有标签操作完成，正在保存数据...")
    
    # 将数据保存至xlsx文件
    data = load_saved(DATA_FILE)
    wb = Workbook()
    ws = wb.active
    headers = data[0].keys() if data else []
    ws.append(list(headers))
    # 3. 写入数据行
    for row in data:
        ws.append(list(row.values()))
    wb.save(OUTPUT_FILE)
    logging.info(f"数据已成功保存至{os.path.abspath(OUTPUT_FILE)}")
    logging.info(f"全部操作完成")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"程序发生错误: {e}")
        import traceback
        traceback.print_exc()
    