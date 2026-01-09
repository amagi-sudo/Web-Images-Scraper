# Web Image Scraper
一个高效健壮的网页图片抓取工具，支持动态加载内容和反爬虫策略。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-orange)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)


## 🌟 功能特性
- **动态内容支持**：通过 Selenium 模拟浏览器，抓取 JavaScript 渲染的图片。
- **智能滚动加载**：自动触发页面滚动，确保懒加载图片完全加载。
- **多格式兼容**：支持 JPG/PNG/GIF/WEBP/SVG 等常见图片格式。
- **反反爬策略**：伪装浏览器指纹，绕过简单反爬检测机制。
- **健壮性设计**：内置自动重试、内容类型校验、文件名自动清理逻辑。


## 🛠 技术栈
- **核心工具**：Selenium (ChromeDriver)、BeautifulSoup、Requests
- **反爬优化**：动态 User-Agent 切换、自动化特征隐藏
- **数据处理**：正则表达式解析、二进制文件流直接下载


## 🚀 快速开始

### 安装依赖
```bash
pip install selenium requests beautifulsoup4
