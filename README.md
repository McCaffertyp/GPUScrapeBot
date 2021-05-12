# GPU Scraper

Personal GPU Scraper I'm working on which will also have purchasing abilities most likely near future.

## How-To
1. Download the source code folder from release
2. Copy GPUScraper-<version> folder to desired location
3. Open a terminal in the folder (or cd into folder)
4. Run with `python run_scraper.py`
5. Follow on-screen prompts

If all goes perfect, that should work.
Possible issues mostly lie with Raspberry Pi, and potentially a personal Linux system.

### Troubleshooting
Should something go wrong, most likely will be with drivers.
A few possibilities will either be permissions or execution of file with bad system exec format.

#### Permissions
Try cd-ing to the file and running a `chmod -x <filename>`
If this does not work...
1. Go to one of following and just download manually.
   - [Chrome](https://chromedriver.chromium.org)
   - [Firefox](https://github.com/mozilla/geckodriver/releases)
   - [Opera](https://github.com/operasoftware/operachromiumdriver/releases)
2. Unzip and place the driver file in GPUScraper-<version>/mccaffertyp/driver_executables

#### Errno 8: exec format error
Only encountered this on my Raspberry pi 4
To fix, do the following:
1. Run `sudo apt-get install chromium-chromedriver`
   - To make sure it downloaded, you can run `chromedriver -v`
2. Run `whereis chromedriver`
   - Should be in one of two locations:
      1. `/usr/bin/chromedriver` - This is where it was for me.
      2. `/usr/lib/chromium-chromedriver/chromedriver` - This never happened for me

Note: Packages should be downloaded with script, but may fail. In such case, either run again or
manually install selenium for Python3

## Extra Information
### Websites
At this point in time, below are the websites being scraped:
1. Amazon (First page only)
2. Best Buy
3. NewEgg

### Items
Items being scraped for stock:
1. RTX 3080

### Browsers
Currently, there are only three supported web browsers:
- Chrome (v90 only - Windows, v88 only - Linux)
- Firefox (v47 above (according to Google), xxx - Linux needs manual installation)
- Opera (v90 only (based on chromedriver) - Windows, v90 only (based on chromedriver) - Linux)

Note: Versions may vary, these are just the versions I included already for your ease of use (hopefully)

### Carriers
Similarly to Browsers, there are only four supported carriers currently:
- AT&T
- Sprint
- T-Mobile
- Verizon

(For a complete list to be added in, look under GPUScraper/mccaffertyp/number_domains.txt)