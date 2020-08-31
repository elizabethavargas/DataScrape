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


browse_url = 'https://www.historynet.com/famous-letters-and-speeches-of-martin-luther-king-jr'

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

# Now let's get the content
html_tags = soup.find('div', attrs={'id': 'content'})

file_path = "./MartinLutherKingData.txt"
text = ''
# get all p and h2 in the nested class 'entry'
for tag in html_tags.find('div', attrs={'class': 'post-13750043 page type-page status-publish has-post-thumbnail hentry magazines-mag-ahi times-1900s times-1900s-civilrights regions-americas topics-blackhist topics-figures'}).find('div', attrs = {'class':'entry'}).findAll(['h2', 'p']):
    # add text that is not bolded or italicized to the doc
    for test in tag:
        if test.name is None:
            text += tag.text + '\n'

with open(file_path, 'w') as out_file:
    print(text.encode("utf-8"), file=out_file)
