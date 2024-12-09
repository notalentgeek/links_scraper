from urllib.parse import urlparse


def strip_url(url):
    # Parse the URL to extract the netloc (the domain part)
    parsed_url = urlparse(url)

    # Get the domain and remove the 'www.' part if it exists
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]

    # Return the stripped domain
    return domain
