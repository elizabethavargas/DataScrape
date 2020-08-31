from bs4 import BeautifulSoup
import urllib.request
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


browse_url = 'https://www.gutenberg.org/files/5307/5307-h/5307-h.htm'

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

# Now let's get the paragraphs
html_tags = soup.findAll('p')

file_path = "./MozartData.txt"
text = ''
for tag in html_tags:
    # If the tag text is a number followed by a period,
    # remove the <p> following it which contains the date and location
    if(bool(re.match('[0-9]+\.', tag.text.strip()))):
        # get the next tag for while
        next_tag = tag.find_next_sibling('p')
        # get all the tags for the letter
        while next_tag.name == 'p' and not bool(re.match('[0-9]+\.', next_tag.text.strip())):
            text += next_tag.text + '\n'
            next_tag = next_tag.find_next_sibling()

# remove footnotes, aka anything in square brackets
text = re.sub('\[[\s\S]+?\]','', text)

with open(file_path, 'w') as out_file:
    print(text.encode("utf-8"), file=out_file)
