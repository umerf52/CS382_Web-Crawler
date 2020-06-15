# Web Crawler

- This is a general-purpose web crawler which takes a base URL, and downloads all pages that are on that website.
- The downloaded files are stored in a directory which is named after the base URL.
- It tries to avoid downloadable objects, such as media files, PDFs, etc.
- This crawler is not guarenteed to work on all websites. Tweaks may be needed to adapt it to specific websites.

### TODO:

- Convert the single-threaded implementation to multi-threaded implementation to reduce crawling time.
