import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import re

# 配置参数
url = "https://tulane.edu/about"
save_dir = "tulane_images"
chrome_driver_path = "D:\\chenlin\\Documents\\downloda path\\chromedriver-win64\\chromedriver.exe"  # 修改为你的实际路径

# 高级浏览器配置
def configure_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    return chrome_options

# 智能滚动加载
def smart_scroll(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    while scroll_attempts < 5:  # 增加滚动次数
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # 增加等待时间
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_attempts += 1

# 检查是否为图片资源
def is_image_url(url):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
    parsed = urlparse(url)
    path = parsed.path.lower()
    return any(path.endswith(ext) for ext in image_extensions)

# 检查 Content-Type 是否为图片
def is_image_content_type(content_type):
    return content_type and content_type.startswith('image/')

# 高级下载函数
def advanced_download(url, save_path, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": url,
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    # 检查 URL 是否为图片
    if not is_image_url(url):
        print(f"跳过非图片资源: {url}")
        return False
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if not is_image_content_type(content_type):
                    print(f"跳过非图片内容: {url} (Content-Type: {content_type})")
                    return False
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return True
            else:
                print(f"尝试 {attempt + 1}/{retries}: 状态码 {response.status_code}")
        except Exception as e:
            print(f"尝试 {attempt + 1}/{retries}: 错误 {str(e)[:50]}")
        time.sleep(2)  # 重试前等待2秒
    return False

# 下载 SVG 文件
def download_svg(url, save_path, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": url,
        "Accept": "image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if content_type != 'image/svg+xml':
                    print(f"跳过非 SVG 内容: {url} (Content-Type: {content_type})")
                    return False
                
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"尝试 {attempt + 1}/{retries}: 状态码 {response.status_code}")
        except Exception as e:
            print(f"尝试 {attempt + 1}/{retries}: 错误 {str(e)[:50]}")
        time.sleep(2)  # 重试前等待2秒
    return False

# 主程序
try:
    # 初始化浏览器
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=configure_browser())
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """
    })
    
    print("智能加载页面中...")
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    smart_scroll(driver)
    
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//img[@src or @data-src or @data-srcset]')))
    except:
        print("未检测到图片容器，继续执行...")
    
    page_source = driver.page_source
    driver.quit()
    
    # 提取图片地址
    def extract_img_sources(html):
        img_pattern = re.compile(r'<img.*?src=["\'](.*?)["\']', re.IGNORECASE)
        data_src_pattern = re.compile(r'<img.*?data-src=["\'](.*?)["\']', re.IGNORECASE)
        data_srcset_pattern = re.compile(r'<img.*?data-srcset=["\'](.*?)["\']', re.IGNORECASE)
        srcset_pattern = re.compile(r'<img.*?srcset=["\'](.*?)["\']', re.IGNORECASE)
        
        sources = []
        sources += data_src_pattern.findall(html)
        sources += img_pattern.findall(html)
        sources += data_srcset_pattern.findall(html)
        for srcset in srcset_pattern.findall(html):
            sources += [url.split()[0] for url in srcset.split(',')]
        return list(set(sources))
    
    os.makedirs(save_dir, exist_ok=True)
    img_urls = extract_img_sources(page_source)
    print(f"找到 {len(img_urls)} 个图片资源")
    
    # 执行下载
    success_count = 0
    for idx, img_url in enumerate(img_urls, 1):
        full_url = urljoin(url, img_url)
        parsed = urlparse(full_url)
        
        # 生成安全文件名
        filename = os.path.basename(parsed.path)
        filename = re.sub(r'[^a-zA-Z0-9\-_.]', '', filename)[:100]
        if not filename:
            filename = f"image_{hash(full_url)}.jpg"
        elif not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
            filename += ".jpg"
            
        save_path = os.path.join(save_dir, filename)
        
        # 避免重复下载
        if os.path.exists(save_path):
            continue
            
        print(f"[{idx}/{len(img_urls)}] 正在下载: {filename}")
        if filename.lower().endswith('.svg'):
            if download_svg(full_url, save_path):
                success_count += 1
        else:
            if advanced_download(full_url, save_path):
                success_count += 1
            
    print(f"\n✅ 下载完成！成功下载 {success_count}/{len(img_urls)} 张图片")
    print(f"保存位置: {os.path.abspath(save_dir)}")

except Exception as e:
    print(f"❌ 程序运行出错: {str(e)}")
    if 'driver' in locals():
        driver.quit()