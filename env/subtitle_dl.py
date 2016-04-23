# TODO: Replace spaces in the series variable with a dash 
# automatically.
# TODO: Add more comments
# TODO: Improve variable names
# TODO: Add extract subtitles from .rar file function
# TODO: Add rename and move to the correct folder function
# TODO: Add requirements.txt file
# TODO: Add GUI?

import requests
from bs4 import BeautifulSoup

class SubtitleDownloader:
    """Downloads and renames subtitles. Also 
    puts them in the correct folder.
    """

    def download_subtitles(self, series, ep, host, lang='english'):
        """Downloads the subtitles"""

        # I split series and ep into two variables so the urls that 
        # doesn't include the series name can be filtered out.
        params = '/subtitles/release?q=%s %s' % (str(series), str(ep))
        url = 'https://subscene.com'
        
        user_agent = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url + params, headers=user_agent)
        soup = BeautifulSoup(r.text, 'html5lib')
 
        # This puts all the links with the desired language and series 
        # in a list.
        link_list = []
        for link in soup.find_all('a'):
            if lang in link.get('href') and series in link.get('href'):
                link_list.append(link.get('href'))

        # Looks if the subtitles are compatible with the desired host.
        for subtitle_link in link_list:
            r = requests.get(url + subtitle_link, headers=user_agent)
            soup = BeautifulSoup(r.text, 'html5lib')

            if host in soup.get_text():
                for link in soup.find_all('a'):
                    if 'download' in link.get('href'):
                        download_link = url + link.get('href')
                        break

        try:
            downloader = requests.get(download_link)
            with open('subtitles.rar', 'wb') as outfile:
                print('Downloading file...')
                outfile.write(downloader.content)
        except UnboundLocalError:
            print('No subtitles found.')


if __name__ == '__main__':
    sd = SubtitleDownloader()
    sd.download_subtitles('series', 'episode', 'host', 'language')
