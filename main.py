import argparse
import eyed3
import re
import requests

from bs4 import BeautifulSoup
from pathlib import Path

eyed3.log.setLevel("ERROR")


exfat_illegal_chars = {
        # '"': "'",
        # '*': '',
        # '/': '.',
        # ':': '.',
        # '<': '_',
        # '>': '_',
        # '?': '¿',
        # '\\': '.',
        # '|': '.'
        } 


PATH = './Darknet Diaries'


def get_episode_page_contents(s, num):
    url = f'https://darknetdiaries.com/episode/{num}/' 
    r = s.get(url)
    # Check if the request was successful
    if r.status_code == 200:
        return r.text
    else:
        print(f'    [!] Failed to get the episode {num} page')

def get_download_link(page):
    link = re.search(r'"mp3": "https://www\.podtrac\.com/pts/redirect\.mp3/(.+?)\.mp3"', page)
    if link is not None:
        return "https://www.podtrac.com/pts/redirect.mp3/" + link.group(1) + ".mp3"

def get_title(page):
    title = re.search(r'<h1>(.+?)</h1>', page)
    if title is not None:
        title = title.group(1)
        if exfat_illegal_chars:
            for k, v in exfat_illegal_chars.items():
                title = title.replace(k, v)
        return title

def get_cover(s, page):
    link = re.search(r'<p><img src="/imgs/(.+?)"', page)
    if link is None:
        return None
    else:
        link = 'https://darknetdiaries.com/imgs/' + link.group(1)
        r = s.get(link)
        # Check if the request was successful
        if r.status_code == 200:
            return r.content, link.split('.')[-1]

def get_date(page):
    date = re.search(r'<p>(.+?) \| Plays: <span id="downloads"></span></p>', page)
    if date is not None:
        return date.group(1).split(' | ')[0]

def get_description(page):
    description = re.search(
    r'<p><img src="\/imgs\/.+?" \/><\/p>(.+?)<h3 id="\w+">\w+<\/h3>',
    page, re.S
    )
    if description is not None:
        description = description.group(0)
        soup = BeautifulSoup(description, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text().strip().strip('References')
        text = text.strip()
        return text 

def get_tags(page):
    tags = re.findall(r'<a href="\/categories\/(.+?)"><div class="', page)
    return tags

def get_transcript(s, num):
    url = f'https://darknetdiaries.com/transcript/{num}/'
    r = s.get(url)
    # Check if the request was successful
    if r.status_code == 200:
        page = r.text
        transcript = re.search(r'<pre>(.+?)</pre>', page, re.S)
        if transcript is not None:
            transcript = transcript.group(1)
            soup = BeautifulSoup(transcript, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            text = text.strip()
            return text 
    print(f'    [!] Failed to get the transcript for episode {num}')

def set_metadata(mp3, title, image=None, image_type=None, track_num=None,
                 description=None):
    audiofile = eyed3.load(str(mp3))
    audiofile.initTag()
    audiofile.tag.artist = 'Darknet Diaries'
    audiofile.tag.album = title 
    audiofile.tag.title = title
    audiofile.tag.genere = 'True Crime'
    audiofile.tag.images.set(3, image, f'image/{image_type}')
    audiofile.tag.track_num = track_num
    audiofile.tag.description = description
    audiofile.tag.save()

def download(s, link, path):
    response = s.get(link)
    
    # Check if the request was successful
    if response.status_code == 200:
        with open(path, 'wb') as f:  # Open a file in binary mode for writing
            f.write(response.content)       # Write the content to the file
        print('    [+] Downloaded.')
        return True
    else:
        print('    [!] Failed to download file')
        return False

def download_episode(s, num, path, transcript=False):
    page = get_episode_page_contents(s, num)
    title = get_title(page)
    dl_link = get_download_link(page)
    path = path / title 
    if not path.exists():
        path.mkdir()
    path = path / (title + '.mp3')
    if path.exists():
        print('    [+] Downloaded.')
        return
    else:
        if download(s, dl_link, path):
            image, image_type = get_cover(s, page)
            description = ', '.join(get_tags(page)) + '\n'
            description += '\n' + get_date(page) + '\n'
            description += '\n' + get_description(page)
            if transcript:
                transcript = get_transcript(s, num)
                with (path.parent / 'transcript.txt').open('w') as f:
                    f.write(transcript)
            set_metadata(path, title, image, image_type, num, description)

def get_last_episode_num(s):
    r = s.get('https://darknetdiaries.com/episode/')
    if r.status_code == 200:
        page = r.text
        num = re.findall(r'<h2 class="post__title"><a href="\/episode\/(.+?)\/">EP ', page)
        if num is not None:
            return int(num[0])
    print(f'    [!] Failed to get the last episode number.')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='Darknet Diaries',
            description='Scrap and download episodes from Darknet Diaries.',
            epilog= 'By default it downloads all the episodes without the transcripts.'
            )
    parser.add_argument('--episodes', type=int, nargs='+', default=None,
                       help=('Specific episode number(s) to download. '
                            + 'If not provided, downloads all episodes.'))
    parser.add_argument('--path', type=str, default=PATH,
                       help='Path to save episodes (default: ./Darknet Diaries)')
    parser.add_argument('--transcript', action='store_true', default=False, 
                        help='Download the transcript.')
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        path.mkdir(parents=True)

    s = requests.Session()
    if args.episodes:
        # Download specific episodes
        print("\n[*] Downloading episodes "
              + f"{', '.join([str(e) for e in args.episodes])}.\n")
        for num in args.episodes:
            print(f"\n[-] Processing episode {num}")
            download_episode(s, num, path, transcript=args.transcript)
    else:
        last_episode = get_last_episode_num(s)
        print(f"\n[*] Downloading all episodes from {last_episode} to 1...\n")
        for num in range(last_episode, 0, -1):
            print(f"\n[-] Processing episode {num}")
            try:
                download_episode(s, num, path, transcript=args.transcript)
            except Exception as e:
                print(f"    [-] Error downloading episode {num}: {str(e)}")
                continue

