from bs4 import BeautifulSoup
import urllib.request
from time import sleep
import os.path
import gzip
import io


# this function is just in case the html needs to be decoded
def gunzip_bytes_obj(bytes_obj):
    in_ = io.BytesIO()
    in_.write(bytes_obj)
    in_.seek(0)
    with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
        gunzipped_bytes_obj = fo.read()

    return gunzipped_bytes_obj.decode()


for page in range(7000):

    file_path = "./WashingtonData/{}".format(page) + ".txt"
    nxt_path = "./WashingtonData/{}".format(page + 1) + ".txt"
    if os.path.exists(file_path) or os.path.exists(nxt_path):
        print('** Skipping **')
        continue

    print(f'Getting page {page + 1}')


    browse_url = f'https://founders.archives.gov/?q=Series%3AWashington-03%20Author%3A%22Washington%2C%20George%22&s=1511311112&r={page + 1}'

    # I have been told that it's polite to add headers with a 'User-Agent' so if
    # the company doesn't want you scraping they can email you and ask you to stop.
    # In my experience they will just block your IP instead of emailing you, but
    # I like doing it anyway. Also, a few websites assume you're not a bot if you
    # have a User-Agent, so it's an easy way to scrape some sites that you wouldn't
    # otherwise be able to.
    req = urllib.request.Request(browse_url, headers={'User-Agent': 'Chaz Gundry cagbyu@byu.edu'})

    # This is the line that actually downloads the html from the internet
    html_doc = urllib.request.urlopen(req).read()

    # I usually don't have to do this
    try:
        html_doc.decode('utf-8')
    except UnicodeDecodeError:
        print('** Unzipping **')
        html_doc = gunzip_bytes_obj(html_doc)

    # This creates a parsed representation of the HTML
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Now let's find our p tags

    innerdiv = soup.find_all(class_="innerdiv docbody")

    if not innerdiv:
        continue

    p_tags = innerdiv[0].find_all('p')



    text = ''
    for p in p_tags:
        # Most of the time the web element you extract using .find() or .findAll()
        # will have more information than you want. Calling .text on an element
        # gets the text that a human reader would see, which is usually what you
        # want (unless you're getting links or images or something)
        text += p.text + '\n'
    with open(file_path, 'w') as out_file:
        print(text.encode("utf-8"), file=out_file)

    # IMPORTANT: It is polite to pause between each request to a single server.
    # Some sites will block your IP address if you don't. You should always
    # sleep for at least 2 or 3 seconds between requests, and I like to do
    # longer if I am leaving the scraper running overnight.
    sleep(2)
