import requests
import json
from lxml import html
from lxml import etree


class Core:
    custom_headers = {
        "accept": "*/*",
        "referer": "https://beddinglegend.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120"
                      " Safari/537.36",
        "viewport-width": "1848"
    }

    def __init__(self):
        pass

    def my_request(self, method, url, params=(), type_response='text'):
        if method == 'GET':
            req = requests.get(url, headers=self.custom_headers)
        else:
            req = requests.post(url, headers=self.custom_headers, data=params)

        content = req.content

        if type_response == 'json':
            return json.loads(content)

        if type_response == 'html':
            return html.fromstring(content)

        return content

    def get_html_from_xpath(self, string_xpath):
        return etree.tostring(string_xpath, method='html', with_tail=False)


class BeddingLegend(Core):
    home_url = "https://beddinglegend.com/"

    def get_list_category(self):
        list_category = []
        url = self.home_url

        root = self.my_request("GET", url, (), 'html')
        main_ul = root.xpath("//*[@id=\"woocommerce_product_categories-7\"]/ul/li")

        for main_li in main_ul:
            list_item = main_li.xpath("ul/li/a")

            for item in list_item:
                url = item.xpath("@href")[0]
                name = item.text

                list_category.append({
                    'name': name,
                    'url': url
                })

        return list_category

    def get_body_html(self, root):
        html = '<h3>Description</h3>'
        description = root.xpath("//*[@id=\"tab-description\"]")[0]

        description = self.get_html_from_xpath(description)
        html = html + description

        html = html + "<h3>Size Charts</h3>"

        size_chart = root.xpath("//*[@id=\"tab-size-charts\"]")[0]
        size_chart = self.get_html_from_xpath(size_chart)

        html = html + size_chart

        return html

    def get_option(self, root):
        option1_value = []

        spans = root.xpath("td[2]/div[2]/span")

        for span in spans:
            text = span.xpath("b/text()")

            if len(text) > 0:
                text = text[0]
            else:
                text = ''

            text2 = span.xpath("text()")[0]

            option1_value.append(text + text2)

        option1_value = ','.join(option1_value)

        option1_name = root.xpath("td[1]/label")[0].text

        return [option1_name, option1_value]

    def get_detail_item(self, item_url, name_category):
        results = []
        handle = ''
        title = ''
        body_html = ''
        vendor = ''
        type_t = ''
        tags = name_category
        published = 'TRUE'
        option1_name = ""
        option1_value = []
        option2_name = ""
        option2_value = ""
        option3_name = ""
        option3_value = ""

        temp = item_url.split("/")
        handle = temp[len(temp) - 1].replace("/", "")

        root = self.my_request("GET", item_url, (), 'html')

        title = root.xpath("//h1")[0].text
        body_html = self.get_body_html(root)

        option1 = root.xpath("//form/table/tbody/tr[1]")[0]
        option1_name, option1_value = self.get_option(option1)

        if len(root.xpath("//form/table/tbody/tr[2]")) > 0:
            option2 = root.xpath("//form/table/tbody/tr[2]")[0]
            option2_name, option2_value = self.get_option(option2)

        if len(root.xpath("//form/table/tbody/tr[3]")) > 0:
            option3 = root.xpath("//form/table/tbody/tr[3]")[0]
            option3_name, option3_value = self.get_option(option3)


        return option2_value

    def get_list_item(self, category):
        url_category = category['url']
        name_category = category['name']

        root = self.my_request("GET", url_category, (), 'html')

        products = root.xpath("//*[@id=\"theme-menu-pusher\"]/div[4]/div[1]/ul/li/div/a/@href")

        for product_url in products:
            data = self.get_detail_item(product_url, name_category)
            print(data)
            # break