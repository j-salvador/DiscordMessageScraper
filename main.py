import requests
from bs4 import BeautifulSoup
import os
from requests_testadapter import Resp


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)


requests_session = requests.session()
requests_session.mount('file://', LocalFileAdapter())
r = requests_session.get('file://dripsvpply.html')

soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('div', attrs={'class':'chatlog__message-group'})
print("Number of results in page:", len(results), "\n")

first_result = results[0]

# keywords = ['half', 'half o', 'half oz', 'half os', 'oz', 'os', 'ounce', '1/2', 'full', 'fulls'
#             'Half', 'Half o', 'Half O', 'Half oz', 'Half Oz', 'Half OZ', 'Half os', 'Half Os', 'Half OS', 'Os', 'OS', 'Oz', 'OZ', 'Ounce', 'OUNCE', 'Full', 'Fulls']
keywords = []
keywords_file = open("keywords.txt")
key = ""
while key := keywords_file.readline():
    keywords.append(key.strip())


result_count = 0
message_dates = []  # for duplicate checking

for result in results:
    username_chunk = result.contents[3].find('span')
    message_chunk = result.contents[3].find('div')

    username = username_chunk.contents[0]
    message = message_chunk.find('div').find('div').contents[0]
    date = result.contents[3].contents[3].contents[0]

    # populate message_dates with messages of interest
    for keyword in keywords:
        if keyword in message:
            if not(date in message_dates):
                message_dates.append(date)

    # print out contents of messages of interest
    for keyword in keywords:
        if keyword in message:
            for md in message_dates:
                if md == date:
                    print("Date: ", date)
                    print("Username: ", username)
                    print("Message: ", message, "\n-----------\n")
                    result_count += 1
                    message_dates.remove(date)


print("Collected ", result_count, " result/s")











####First result
# print(first_result.contents[3], "\n------\n")
# username_chunk = first_result.contents[3].find('span')
# message_chunk = first_result.contents[3].find('div')
#
# username = username_chunk.contents[0]
# message = message_chunk.find('div').find('div').contents[0]
# message_id = message_chunk.contents[1]
# date = first_result.contents[3].contents[3].contents[0]
# print("Date: ", date)
# print("Username: ", username)
# print("Message: ", message)



#first_result.contents[3].contents[5]