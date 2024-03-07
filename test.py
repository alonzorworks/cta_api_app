import ssl
from urllib.request import urlopen, HTTPSHandler
import json

def get_json_from_link(url):
    """Can turn link into a readable JSON format."""
    # Create a custom context that allows all ciphers
    ctx = ssl.create_default_context()
    ctx.set_ciphers('DEFAULT:@SECLEVEL=0')

    # Create a custom HTTPS handler with the custom context
    https_handler = HTTPSHandler(context=ctx)

    # Open the URL with the custom HTTPS handler
    with urlopen(url, context=ctx, https_handler=https_handler) as response:
        data = response.read().decode("utf-8")

    return json.loads(data)