import os
import re
import time
import argparse
import requests
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


MAX_RETRIES = 30
CHUNK_SIZE = 2**20  # 1 MB

WELCOME_URL = "https://file.tokybook.com/upload/welcome-you-to-tokybook.mp3"
AUDIO_BASE_URL = "https://files02.tokybook.com/audio/"

def create_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def main(url):
    book_url = url

    session = create_session()

    # Fetch the audiobook page
    response = requests.get(book_url)
    response = requests.get(book_url)
    if response.status_code != 200:
        print(f"Failed to fetch {book_url} (status {response.status_code})")
        return
    soup = BeautifulSoup(response.text, "lxml")

    # Extract audiobook title
    book_title = soup.find("div",{"class":"inside-page-hero grid-container grid-parent"}).find("h1").text.strip()
    book_title = re.sub(r'[<>:"/\\|?*]', "_", book_title)
    print(f"downloading {book_title}")
    # make a folder with book title
    os.makedirs(f"{book_title}", exist_ok=True)

    # Find chapter MP3 links
    chapter_links = extract_chapter_links(soup)
    failed = []
    for i, link in enumerate(chapter_links, start=1):
        file_name = os.path.join(book_title, f"chapter {i:02}.mp3")
        if not download_chapter(file_name, i, link, session):
            failed.append(i)

    print("All chapters downloaded!")
    if failed:
        print("The following chapters failed:", failed)


def download_chapter(file_name, i, link, session):
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"downloading chapter {i:02}.mp3 (attempt {attempt}/{MAX_RETRIES})")

        try:
            chap_response = session.get(link, stream=True, timeout=60)
            chap_size = int(chap_response.headers.get("content-length", 0))

            if chap_response.status_code == 200:
                with open(file_name, "wb") as f, tqdm(total=chap_size, unit="B"
                        , unit_scale=True, unit_divisor=1024
                        , desc=f"downloading chapter {i:02}.mp3:") as progress:
                    for chunk in chap_response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            progress.update(len(chunk))
                    f.flush()
                    os.fsync(f.fileno())

                actual_size = os.path.getsize(file_name)
                if chap_size > 0 and actual_size != chap_size:
                    print(f"Size mismatch for chapter {i:02}: expected {chap_size}, got {actual_size}")
                    print("Retrying due to incomplete download...")
                    time.sleep(2)
                    continue  # Retry

                print(f"Successfully downloaded chapter {i:02}")
                return True # Success

            else:
                print(f"HTTP error {chap_response.status_code} for {link}")


        except (requests.exceptions.RequestException, requests.exceptions.ChunkedEncodingError,

                requests.exceptions.ConnectionError, requests.exceptions.Timeout,

                urllib3.exceptions.ProtocolError, urllib3.exceptions.IncompleteRead) as e:
            print(f"Error downloading chapter {i:02}: {e}")

        time.sleep(2)

    else:
        print(f"Failed to download chapter {i:02} after {MAX_RETRIES} attempts.")
        return False


def extract_chapter_links(soup):
    chapter_links = []
    for script in soup.find_all("script"):
        if "chapter_link_dropbox" in script.text:
            for line in script.text.split("\n"):
                if "chapter_link_dropbox" in line and ".mp3" in line:
                    url = line.split('"')[3]
                    welcom_url = WELCOME_URL
                    if not url.startswith(AUDIO_BASE_URL) and url != welcom_url:
                        url = AUDIO_BASE_URL + url.replace(" ", "%20").replace('\\', "/")
                    if url != welcom_url:
                        chapter_links.append(url)
    return chapter_links


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download audiobook from Tokybook.")
    parser.add_argument("url", help="Full URL of the audiobook page")
    args = parser.parse_args()
    main(url=args.url)
