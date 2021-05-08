# GPU Scraper

Personal GPU Scraper I'm working on which will also have purchasing abilities most likely near future

## How-To
1. Download the zip files from release
2. Copy GPUScraper into the file you want
3. Unzip the driver executables
   - Or just the one you need
4. Place into GPUScraper/mccaffertyp/driver_executables
5. Open a terminal in the folder (or cd into folder)
6. Run with `python run_scraper.py`
7. Follow on-screen prompts

Note: Packages should be downloaded with script, but may fail. In such case, either run again or
manually install selenium and pynput for Python3

## Extra Information
### Browsers
Currently, there are only three supported web browsers:
- Chrome (v90 only)
- Firefox (v47 above (according to Google))
- Opera (v90 only (based on chromedriver))

### Carriers
Similarly to Browsers, there are only four supported carriers currently:
- AT&T
- Sprint
- T-Mobile
- Verizon

(For a complete list to be added in, look under GPUScraper/mccaffertyp/number_domains.txt)