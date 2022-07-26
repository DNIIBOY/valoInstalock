from requests import get, exceptions
from constants import VERSION_NUMBER


class UpdateHandler:
    def __init__(self):
        self.current_version = VERSION_NUMBER

        latest_version = get_latest_version()
        # In case of lost connection, assume current version is latest
        self.latest_version = latest_version if latest_version != "No Connection" else self.current_version

    def is_latest_version(self) -> bool:
        """
        :return: boolean indicating if the current version is the latest version
        """
        current_digits = [int(i) for i in self.current_version[1:].split(".")]
        latest_digits = [int(i) for i in self.latest_version[1:].split(".")]

        for current_digit, latest_digit in zip(current_digits, latest_digits):
            if current_digit < latest_digit:
                return False
            elif current_digit > latest_digit:
                return False

        return True

    def is_future_version(self) -> bool:
        """
        :return: boolean indicating if the current version is newer than the latest version
        """
        current_digits = [int(i) for i in self.current_version[1:].split(".")]
        latest_digits = [int(i) for i in self.latest_version[1:].split(".")]

        for current_digit, latest_digit in zip(current_digits, latest_digits):
            if current_digit > latest_digit:
                return True
            elif current_digit < latest_digit:
                return False

        return False


def get_latest_version() -> str:
    try:
        response = get("https://api.github.com/repos/DNIIBOY/valoInstalock/releases/latest")
        return response.json()["tag_name"]
    except exceptions.ConnectionError:
        return "No Connection"


if __name__ == '__main__':
    UH = UpdateHandler()
    print(UH.is_future_version())
    print(get_latest_version())
