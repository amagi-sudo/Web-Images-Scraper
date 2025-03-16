# Web-Images-Scraper

---

# Web Image Scraper

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-orange)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

一个高效、健壮的网页图片抓取工具，支持动态加载内容和反爬虫策略。

## 🌟 功能特性
- **动态内容支持**：通过 Selenium 模拟浏览器，抓取 JavaScript 渲染的图片。
- **智能滚动加载**：自动触发页面滚动，确保懒加载图片完全加载。
- **多格式兼容**：支持 JPG/PNG/GIF/WEBP/SVG 等常见格式。
- **反反爬策略**：伪装浏览器指纹，绕过简单反爬检测。
- **健壮性设计**：自动重试、内容类型检查、文件名清理。

## 🛠 技术栈
- **核心工具**：Selenium (ChromeDriver)、BeautifulSoup、Requests
- **反爬策略**：动态 User-Agent、自动化特征隐藏
- **数据处理**：正则表达式、文件流下载

## 🚀 快速开始

### 安装依赖
```bash
pip install selenium requests beautifulsoup4

PS:下载 ChromeDriver
访问 ChromeDriver 官网。

下载与本地 Chrome 版本匹配的驱动，解压后替换代码中的 chrome_driver_path。
