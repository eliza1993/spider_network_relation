

def get_domain(url):
    http_pro = ''
    if 'http://' in url:
        http_pro = 'http://'
        url = url[7:]

    if 'https://' in url:
        http_pro = 'https://'
        url = url[8:]

    if '/' in url:
        index = url.index('/')
        url = url[0:index]

    url = http_pro + url
    return url



def handle_url(url = None):
    if url is None:
        return url

    # if 'http://' in url:
    #     url = url[7:]

    # if 'https://' in url:
    #     url = url[8:]
    
    if '?' in url:
        index = url.index('?')
        url = url[0:index]

    return url


