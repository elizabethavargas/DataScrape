import bs4
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

# put all 1590 accounts into different files

# grab the last index read
with open('saintsIndex.txt') as f:
    startingIndex = int(next(f).strip())

for page in range(startingIndex, 1589):
    # file_path = "./SaintsByTheSeaData2/{}".format(page) + ".txt"
    print(f'Getting page {page + 1}')
    browse_url = f'https://saintsbysea.lib.byu.edu/mii/account/{page + 1}'

    # I have been told that it's polite to add headers with a 'User-Agent' so if
    # the company doesn't want you scraping they can email you and ask you to stop.
    # In my experience they will just block your IP instead of emailing you, but
    # I like doing it anyway. Also, a few websites assume you're not a bot if you
    # have a User-Agent, so it's an easy way to scrape some sites that you wouldn't
    # otherwise be able to.
    req = urllib.request.Request(browse_url, headers={'User-Agent': 'Elizabeth Greer elizabethgreer@byu.edu'})

    # This is the line that actually downloads the html from the internet
    html_doc = urllib.request.urlopen(req).read()

    # I usually don't have to do this
    try:
        html_doc.decode('utf-8')
    except UnicodeDecodeError:
        print('** Unzipping **')
        html_doc = gunzip_bytes_obj(html_doc)

    # This creates a parsed representation of the HTML
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')

    # Now let's find our entry tag
    account = soup.find('div', attrs={'class': 'entry'})

    # Lets get the title
    file_path = soup.find('section', attrs={'class': 'page account'}).find('h2').text
    if(file_path == "A Compilation of General Voyage Notes"):
        file_path += "_" + soup.find('div', attrs={'class': 'page'}).find('h1').text
    file_path = file_path.replace(" ", "_") + ".txt"
    print(file_path)

    text = ''
    # if the text is directly in the div, add the text
    # else add the text of all the nested <p>'s
    for p in account:
        if(type(p) == bs4.element.NavigableString):
            text += p + '\n'
            continue
        if p.name == 'p' and p.class_ == None:
            text += p.text + '\n'

    # if file is short, put it in short_entries subdirectory
    if(len(text) < 200):
        file_path = "./SaintsByTheSeaData2/short_entries/" + file_path
    else:
        file_path = "./SaintsByTheSeaData2/" + file_path

    with open(file_path, 'w') as out_file:
        print(text.encode("utf-8"), file=out_file)

    # Write last index read to file
    f = open("saintsIndex.txt", "w")
    f.write(str(page))
    f.close()

    # IMPORTANT: It is polite to pause between each request to a single server.
    # Some sites will block your IP address if you don't. You should always
    # sleep for at least 2 or 3 seconds between requests, and I like to do
    # longer if I am leaving the scraper running overnight.
    sleep(2)
