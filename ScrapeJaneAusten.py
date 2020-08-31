from bs4 import BeautifulSoup
import urllib.request
import os.path
import gzip
import io
import re


# just in case the html needs to be decoded
def gunzip_bytes_obj(bytes_obj):
    in_ = io.BytesIO()
    in_.write(bytes_obj)
    in_.seek(0)
    with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
        gunzipped_bytes_obj = fo.read()

    return gunzipped_bytes_obj.decode()


browse_url = 'https://www.gutenberg.org/files/42078/42078-h/42078-h.htm'

# I have been told that it's polite to add headers with a 'User-Agent' so if
# the company doesn't want you scraping they can email you and ask you to stop.
# Also, a few websites assume you're not a bot if you
# have a User-Agent, so it's an easy way to scrape some sites that you wouldn't
# otherwise be able to.
req = urllib.request.Request(browse_url, headers={'User-Agent': 'Elizabeth Greer elizabethgreer@byu.edu'})

# This is the line that actually downloads the html from the internet
html_doc = urllib.request.urlopen(req).read()

# I usually don't have to do this
"""
try:
    html_doc.decode('utf-8')
except UnicodeDecodeError:
    print('** Unzipping **')
    html_doc = gunzip_bytes_obj(html_doc)
    """

# This creates a parsed representation of the HTML
soup = BeautifulSoup(html_doc, 'html.parser')

# Now let's get the body
html_tags = soup.body.contents

file_path = "./JaneAustenData.txt"
text = ''
for tag in html_tags:
    # If the tag is <h2> and it contains roman numeral followed by a period, get all the <p>'s following
    if tag.name == "h2" and bool(re.match('^[MDCLXVI]+\.$', tag.text)):
        next_tag = tag.find_next_sibling('p')
        while next_tag.name == 'p':
            # remove page numbers in the format [##] from <p>
            text += re.sub('\[[0-9]+\]','', next_tag.text) + '\n'
            next_tag = next_tag.find_next_sibling()

with open(file_path, 'w') as out_file:
    print(text.encode("utf-8"), file=out_file)
