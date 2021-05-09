# GPU Scraper

Personal GPU Scraper I'm working on which will also have purchasing abilities most likely near future

## How-To
1. Download the source code folder from release
2. Copy GPUScraper-<version> folder to desired location
3. Open a terminal in the folder (or cd into folder)
4. Run with `python run_scraper.py`
5. Follow on-screen prompts

Note: Packages should be downloaded with script, but may fail. In such case, either run again or
manually install selenium and pynput for Python3

## Extra Information
### Browsers
Currently, there are only three supported web browsers:
- Chrome (v90 only - Windows, v88 only - Linux)
- Firefox (v47 above (according to Google), xxx - Linux needs manual installation)
- Opera (v90 only (based on chromedriver) - Windows, v90 only (based on chromedriver) - Linux)

### Carriers
Similarly to Browsers, there are only four supported carriers currently:
- AT&T
- Sprint
- T-Mobile
- Verizon

(For a complete list to be added in, look under GPUScraper/mccaffertyp/number_domains.txt)