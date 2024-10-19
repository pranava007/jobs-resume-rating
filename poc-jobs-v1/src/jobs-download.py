import requests

from bs4 import BeautifulSoup




def html_to_text(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        with open(filename, 'w') as file:
            file.write(text)
        return text
    else:
        print(
            f"Failed to fetch HTML from {url}. Status code: {response.status_code}")
        return None

# Example usage
# url = "http://example.com"
# text = html_to_text(url)
# if text:
#     print(text)


def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename} successfully!")
    else:
        print(
            f"Failed to download {filename}. Status code: {response.status_code}")


# Example usage
url = "https://www.innovasolutions.com/careers-usa/search.php#/jobs/944807"
outputfilename = "innova-jobid-944807.txt"
# download_file(url, outputfilename

#  pip install beautifulsoup4
# pip install requsts

text = html_to_text(url, outputfilename)
if text:
    print(text)
