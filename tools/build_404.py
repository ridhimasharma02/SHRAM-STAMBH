# -*- coding: utf-8 -*-
"""Builds 404.html, shown for an address that doesn't exist.
Most web hosts use a file called 404.html automatically; tools/serve.py does too."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_common import page, hi, ICONS as I

body = f'''
    <div class="panel notfound t-help">
      <p class="bigcode">404</p>
      <h1>This page does not exist{hi("यह पन्ना नहीं मिला")}</h1>
      <p class="lead">The address may have a mistake in it. Go back to the home page, or call for help.{hi("पता गलत हो सकता है। मुख्य पन्ने पर जाएँ, या मदद के लिए फ़ोन करें।")}</p>
      <div class="step-actions">
        <a class="btn dark" href="index.html">{I["home"]}Home · मुख्य पन्ना</a>
        <a class="callbtn" href="tel:15100">{I["phone"]}<span>15100<small>Free legal help · मुफ़्त मदद</small></span></a>
      </div>
    </div>
'''
page("404.html", "Page not found", body, "This page does not exist. Go to the SHRAM STAMBH home page or call 15100 for free legal help.", topic="t-help", guard=False)

# The 404 page can be shown at any address, even inside a folder, so its links start from the site root.
import re
from build_common import OUT
path = OUT + "404.html"
html = open(path, encoding="utf-8").read()
html = re.sub(r'(href|src)="(?!https?:|tel:|mailto:|#|/|data:)', r'\1="/', html)
open(path, "w", encoding="utf-8").write(html)
print("404 links made absolute")
