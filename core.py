import requests
import json
from lxml import html
from lxml import etree
import csv


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

    def export_csv(self, data, option="start"):
        header = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value", "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Image Src", "Image Position", "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Google Shopping / Google Product Category", "Google Shopping / Gender", "Google Shopping / Age Group", "Google Shopping / MPN", "Google Shopping / AdWords Grouping", "Google Shopping / AdWords Labels", "Google Shopping / Condition", "Google Shopping / Custom Product", "Google Shopping / Custom Label 0", "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2", "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4", "Variant Image", "Variant Weight Unit", "Variant Tax Code", "Cost per item"]
        mode = 'w'

        if option != "init":
            mode = 'a+'

        with open('file-datas.csv', mode=mode) as data_file:
            file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if option == "init":
                file_writer.writerow(header)
                return

            file_writer.writerow(data)

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

    def get_items(self, root):
        products = root.xpath("//*[@id=\"theme-menu-pusher\"]/div[4]/div[1]/ul/li")
        result = []

        for item in products:
            url = item.xpath("div/a/@href")[0]
            price = item.xpath("span[3]/ins/span/text()")[0]
            result.append([url, price])

        return result

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

    def get_detail_item(self, item_url, price, name_category):
        results = []
        handle = ''
        title = ''
        body_html = ''
        vendor = ''
        type_t = ''
        tags = name_category
        published = 'TRUE'

        temp = item_url.split("/")

        handle = temp[len(temp) - 2].replace("/", "")

        root = self.my_request("GET", item_url, (), 'html')

        title = root.xpath("//h1")[0].text
        body_html = self.get_body_html(root)

        option1 = root.xpath("//form/table/tbody/tr[1]")[0]
        option1_name, option1_value = self.get_option(option1)

        option2_name, option2_value, option3_name, option3_value = '', '', '', ''

        if len(root.xpath("//form/table/tbody/tr[2]")) > 0:
            option2 = root.xpath("//form/table/tbody/tr[2]")[0]
            option2_name, option2_value = self.get_option(option2)

        if len(root.xpath("//form/table/tbody/tr[3]")) > 0:
            option3 = root.xpath("//form/table/tbody/tr[3]")[0]
            option3_name, option3_value = self.get_option(option3)

        sku = root.xpath("//form/@data-product_id")[0]
        # data_variations = root.xpath("//form/@data-product_variations")[0]
        # data_variations = json.loads(data_variations)
        variant_grams = '0'
        variant_inventory_tracker = "shopify"
        variant_inventory_qty = ""
        variant_inventory_policy = ""
        variant_fulfillment_service = ""
        variant_price = price
        variant_compare_at_price = ""
        variant_requires_shipping = "TRUE"
        variant_taxable = "FALSE"
        variant_barcode = ""
        image_src = root.xpath("//*[@id=\"gallery-image\"]/figure/@data-zoom")[0]
        image_position = 1
        image_alt_text = root.xpath("//*[@id=\"gallery-image\"]/figure/img/@alt")[0]
        gift_card = "FALSE"
        seo_title = ""
        seo_description = ""
        google_product_category = ""
        gender = ""
        age_group = ""
        mpn = ""
        adwords_grouping = ""
        adwords_labels = ""
        condition = ""
        custom_product = ""
        custom_label0 = ""
        custom_label1 = ""
        custom_label2 = ""
        custom_label3 = ""
        custom_label4 = ""
        variant_image = ""
        variant_weight_unit = "kg"
        variant_tax_code = ""
        cost_per_item = ""

        results = [
            handle, title, body_html, vendor, type_t, tags, published, option1_name, option1_value, option2_name, option2_value, option3_name, option3_value,
            sku, variant_grams, variant_inventory_tracker, variant_inventory_qty, variant_inventory_policy, variant_fulfillment_service,
            variant_price, variant_compare_at_price, variant_requires_shipping, variant_taxable, variant_barcode, image_src,
            image_position, image_alt_text, gift_card, seo_title, seo_description, google_product_category, gender, age_group,
            mpn, adwords_grouping, adwords_labels, condition, custom_product, custom_label0, custom_label1, custom_label2,
            custom_label3, custom_label4, variant_image, variant_weight_unit, variant_tax_code, cost_per_item
        ]

        return results

    def get_list_item(self, category):
        url_category = category['url']
        name_category = category['name']

        root = self.my_request("GET", url_category, (), 'html')

        products = self.get_items(root)

        self.export_csv([], "init")

        for product_url, price in products:
            data = self.get_detail_item(product_url, price, name_category)
            self.export_csv(data)