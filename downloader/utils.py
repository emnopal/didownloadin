from urllib.parse import unquote
import requests, re, json


def twitter_downloader(url):

    # Inspired from: https://github.com/inteoryx/twitter-video-dl

    # Endpoint
    GUEST_TOKEN_ENDPOINT = "https://api.twitter.com/1.1/guest/activate.json"
    STATUS_ENDPOINT = "https://twitter.com/i/api/graphql/"

    # Regex pattern
    CONTAINER_PATTERN = re.compile("['\"](http[^'\"]+.mp4\?tag=[0-9]{2})")
    GET_ID = re.compile(r"status/([0-9]+)")
    GET_BT = re.compile(r'["\'](AAA[a-zA-Z0-9%-]+%[a-zA-Z0-9%-]+)["\']')
    GET_JSON = re.compile(r"src=['\"]([^'\"()]*js)['\"]")
    GET_OPS = re.compile(r'\{queryId:"[a-zA-Z0-9_]+[^\}]+"')
    GET_QUERY_ID = re.compile(r'queryId:"([^"]+)"')
    GET_RESOLUTION = re.compile(r"([0-9]+)x([0-9]+)")

    headers = {}
    guest_token = {}
    bearer_token = None
    query_id = None

    response = requests.Session().get(url, headers=headers, stream=True)

    result = [line.decode("utf-8") for line in response.iter_lines()]

    # Guessing token
    try:
        for js in re.findall(GET_JSON, "".join(result)):
            file_content = requests.Session().get(js, headers=headers)
            bt = re.search(GET_BT, file_content.text)
            ops = re.findall(GET_OPS, file_content.text)
            query_op = [op for op in ops if "TweetDetail" in op]
            if len(query_op) == 1:
                query_id = re.findall(GET_QUERY_ID, query_op[0])[0]
            if bt:
                bearer_token = bt.group(1)
        headers['authorization'] =  f"Bearer {bearer_token}"
        guest_token_resp = requests.Session().post(GUEST_TOKEN_ENDPOINT, headers=headers)
        guest_token = json.loads(guest_token_resp.text)['guest_token']
        headers['x-guest-token'] = guest_token
    except:
        return {
            "Error": {
                "message": "Error while guessing token"
            }
        }

    # Getting video url
    tweet_id = re.findall(GET_ID, url)[0]
    status_params = f"TweetDetail?variables=%7B%22focalTweetId%22%3A%22{tweet_id}%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Afalse%2C%22withTweetQuoteCount%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withUserResults%22%3Atrue%2C%22withNftAvatar%22%3Afalse%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%7D"
    status_resp = requests.Session().get(f"{STATUS_ENDPOINT}{query_id}/{status_params}", headers=headers)

    available_urls  = re.findall(CONTAINER_PATTERN, status_resp.text)

    resolutions = {}
    for vs in available_urls:
        resolution = "x".join(re.findall(GET_RESOLUTION, vs)[0])
        resolutions[resolution] = vs

    return resolutions


def facebook_downloader(url):\
    # Replacing facebook url to mobile version
    if 'www' in url:
        https, url = url.replace('www', 'mbasic').split('//')

    # Requesting video url
    res = requests.get(f"{https}//{url}")

    # Getting video url
    if 'video_redirect' in res.text:
        url_video = re.search(r'href\=\"\/video\_redirect\/\?src\=(.*?)\"', res.text)
        new_url = unquote(url_video.group(1)).replace(':', '&')
        if "https&" in new_url:
            new_url = new_url.replace("https&", "")
        return {
            "default_res": f"{https}{new_url}"
        }

def parse_url(url):
    if "facebook.com" in url:
        return "Facebook", facebook_downloader(url)

    if "twitter.com" in url:
        return "Twitter", twitter_downloader(url)
