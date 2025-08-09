from openbachelors.const.filepath import ASSET_DIRPATH
from openbachelors.util.helper import download_file


def test_download_file():
    download_file(
        "https://dl.google.com/tag/s/dl/chrome/install/googlechromestandaloneenterprise64.msi",
        "chrome.exe",
        ASSET_DIRPATH,
    )
