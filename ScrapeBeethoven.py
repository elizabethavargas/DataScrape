from bs4 import BeautifulSoup
import urllib.request
import gzip
import io


# just in case the html needs to be decoded
def gunzip_bytes_obj(bytes_obj):
    in_ = io.BytesIO()
    in_.write(bytes_obj)
    in_.seek(0)
    with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
        gunzipped_bytes_obj = fo.read()

    return gunzipped_bytes_obj.decode()


browse_url = 'https://www.gutenberg.org/files/13065/13065-h/13065-h.htm'

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

# Now let's get the headers for all the letters
html_tags = soup.findAll('h3', attrs={'class': 'letter'})

file_path = "./BeethovenData.txt"
text = ''
for tag in html_tags:
    # Now lets get all the <p> tags until the next letter
    next_tag = tag.find_next_sibling('p')
    while next_tag.name == 'p':
        # don't add the dates
        if next_tag.class_ != 'date':
            text += next_tag.text + '\n'
            next_tag = next_tag.find_next_sibling()

with open(file_path, 'w') as out_file:
    print(text.encode("utf-8"), file=out_file)
