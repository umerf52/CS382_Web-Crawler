import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import os

# User agent is needed to imitate behavior of web browsers
user_agent = {'User-agent': 'Mozilla/5.0'}
# List of extensions that would be ignored while crawling
extensions = ['3g2', '3gp', 'asf', 'asx', 'avi', 'flv', 'm2ts', 'mkv', 'mov', 'mp4',
              'mpg', 'mpeg', 'rm', 'swf', 'vob', 'wmv', 'mp3', 'pdf', 'jpg', 'jpeg', 'png', 'gif']
# List of characters that cannot be a part of Windows 10 file name / path
inv_char = [':', '*', '>', '<', '?', '|', '"', '/', '\n', '\t', '\r']
# List of white space characters
white_space = ['\n', '\t', '\r']
# List of prefixes to ignore
prefix = ['mailto:', 'itms:appss://']


def main():
    url = input('Enter a website to that will act as the base URL: ')
    if url.startswith('https://'):
        url = url.replace('https://', '')
    if url.startswith('http://'):
        url = url.replace('http://', '')

    counter = 1								# Used to keep track of unnamed files
    unvisited = set()
    visited = set()

    protocol_url = 'https://{}'.format(url)
    parsed_uri = urlparse(protocol_url)

    check_domain = '{uri.netloc}'.format(uri=parsed_uri)
    directory_path = '{uri.netloc}'.format(uri=parsed_uri)

    # Make a folder to store the HTML files
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    try:
        r = requests.get(protocol_url, headers=user_agent)
    except:
        protocol_url = 'http://{}'.format(url)
        parsed_uri = urlparse(protocol_url)
        r = requests.get(protocol_url, headers=user_agent)

    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if 'www.' in domain:
        domain = domain.replace('www.', '')

    unvisited.add(protocol_url)

    data = r.text
    soup = BeautifulSoup(data, features='html.parser')
    for link in soup.find_all('a'):
        temp_link = link.get('href')
        if temp_link is None:
            continue
        for ch in white_space:
            temp_link = temp_link.replace(ch, '')
        temp_link = urllib.parse.urljoin(protocol_url, temp_link)
        temp_link = temp_link.strip()
        if '#' in temp_link:
            continue
        if temp_link.startswith(tuple(prefix)) or temp_link.endswith(tuple(extensions)):
            continue
        if check_domain in temp_link:
            unvisited.add(temp_link)

    while len(unvisited) != 0:
        link = unvisited.pop()
        print('Processing {}'.format(link))
        r = requests.get(link, headers=user_agent)
        data = r.text
        soup = BeautifulSoup(data, features='html.parser')
        if soup.title is None or soup.title.string is None:
            filename = 'unnamed({}).html'.format(str(counter))
            counter = counter + 1
        else:
            filename = soup.title.string + '.html'
        full_filename = os.path.join(directory_path, filename)
        full_filename = full_filename.replace('\'\'', '\'')
        for ch in inv_char:
            full_filename = full_filename.replace(ch, '')
        if full_filename.startswith(' ') or full_filename.startswith('\t') or full_filename.startswith('\n') or full_filename.startswith('\r'):
            full_filename = full_filename.lstrip()
        if not os.path.exists(full_filename):
            with open(full_filename, 'w', encoding='utf-8') as f:
                f.write(data)
        if link not in visited:
            visited.add(link)

        for new_links in soup.find_all('a'):
            if new_links.get('href') is None:
                continue
            temp_link = new_links.get('href')
            for ch in white_space:
                temp_link = temp_link.replace(ch, '')
            temp_link = urllib.parse.urljoin(protocol_url, temp_link)
            temp_link = temp_link.strip()
            if '#' in temp_link:
                continue
            if temp_link.startswith(tuple(prefix)) or temp_link.endswith(tuple(extensions)):
                continue
            if check_domain in temp_link:
                if temp_link not in visited:
                    unvisited.add(temp_link)

    print('Finished downloading.')


if __name__ == '__main__':
    main()
