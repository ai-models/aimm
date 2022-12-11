import re


# HUGGINGFACE_REGEX = r"https:\/\/huggingface\.co\/\w+\/.+\/+resolve+\/[0-9a-zA-z]{40}\/.+"
# # GITHUB_REGEX = r"https:\/\/github\.com+\/+.+\/+.+\/+releases+\/.+"
# # regex for github path with commit hash
GITHUB_REGEX = r"https:\/\/github\.com\/\w+\/.+\/tree\/[0-9a-zA-z]{40}\/.+"

def is_url_safe(url) -> bool:
    """
    Checks whether a URL is safe to use or not.
    """
    # check if url is huggingface.co
    if "huggingface.co" in url:
        # check if url is safe
        return bool(re.match(HUGGINGFACE_REGEX, url))

    elif "github.com" in url:
        # check if url is safe
        return bool(re.match(GITHUB_REGEX, url))

    else:
        return False
