import requests
from lxml import html
import csv

if __name__=='__main__':
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        'referer': "https://beddinglegend.com/"
    }
    url = "https://beddinglegend.com/collections/bedding-set-duvet-cover/galaxy/"

    req = requests.get(url, headers=headers)
    root = html.fromstring(req.content)
    product = root.xpath("//*[@id=\"theme-menu-pusher\"]/div[4]/div[1]/ul/li")



    with open('myfile.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        employee_writer.writerow(['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags'])

        for item in product:
            title = item.xpath("h2/a")[0].text
            employee_writer.writerow([title])
