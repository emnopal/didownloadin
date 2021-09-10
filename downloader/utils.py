from urllib.parse import unquote
import requests, re


def parse_url(url):
    if 'www' in url:
        https, url = url.replace('www', 'mbasic').split('//')
    res = requests.get(f"{https}//{url}")
    if 'video_redirect' in res.text:
        url_video = re.search(r'href\=\"\/video\_redirect\/\?src\=(.*?)\"', res.text)
        new_url = unquote(url_video.group(1)).replace(':', '&')
        if "https&" in new_url:
            new_url = new_url.replace("https&", "")
        return f"{https}{new_url}"

