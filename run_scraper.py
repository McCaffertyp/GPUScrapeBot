from mccaffertyp.gpu_scraper import GpuScraper
from selenium import webdriver

gpu_scraper = GpuScraper(webdriver)
gpu_scraper.run()
