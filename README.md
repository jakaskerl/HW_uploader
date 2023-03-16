# HTML to PDF tool for Luxonis hardware page

## Scripts
Install [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) before first run.


Execute scripts using Python3.10+.
**Run retrieve_devices.py first!**

### main.py
Converts html data from Luxonis docs hardware page to PDF for use in datasheets

### retrieve_devices.py
Retrieves all possible current devices and stores them inside devices.json where main.py can see them

### uploader.py
TODO