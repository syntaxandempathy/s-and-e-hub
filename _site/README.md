# Website Files

_This directory contains the static HTML files for the website, ready for deployment._

**Overview**

This directory (`site`) holds the compiled HTML, CSS, and JavaScript files for the website.  It's the output of the website build process and contains all the necessary files to serve the site. The `listings.json` file provides a structured index of articles.  `search.json` contains data for website search functionality. The sitemap assists search engines in indexing the site's content.  To deploy, simply copy the contents of this directory to your web server.

**Contents**

* `about.html`: About page content (27.1 KB).
* `index.html`: Homepage content (21.8 KB).
* `listings.json`: JSON file listing website articles (8.8 KB, ~67 lines).  Sample: `["/articles/index.html", ...]`
* `robots.txt`:  Instructions for web robots (70 bytes, ~2 lines). Sample: `Sitemap: ...`
* `search.json`: JSON file containing data for website search (5.6 MB, ~21 lines). Sample: `[{"objectID": "...", ...}]`
* `sitemap.xml`: XML sitemap for search engines (24.0 KB).


**Structure**

The directory contains static HTML files organized for easy deployment.  The `listings.json` and `search.json` files provide metadata for navigation and search.

Last updated: 2025-09-20
