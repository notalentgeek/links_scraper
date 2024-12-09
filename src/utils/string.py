from urllib.parse import urlparse


def get_domain(url):
    """
    Extract the domain from a given URL and remove the 'www.' prefix if it exists.

    This function parses the provided URL, extracts the netloc (domain),
    and removes the 'www.' prefix, if present, to return the clean domain.

    Args:
        url (str): The URL from which to extract the domain.

    Returns:
        str: The domain name, with the 'www.' prefix removed if it exists.

    Example:
        >>> get_domain('https://www.google.com')
        'google.com'

        >>> get_domain('http://example.org')
        'example.org'
    """
    # Parse the URL to extract the netloc (the domain part)
    parsed_url = urlparse(url)

    # Get the domain and remove the 'www.' part if it exists
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]

    # Return the stripped domain
    return domain
