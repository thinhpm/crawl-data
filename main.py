from core import Core
from core import BeddingLegend


if __name__ == '__main__':
    core = BeddingLegend()

    list_category = core.get_list_category()

    for category in list_category:
        data = core.get_list_item(category)
        # print((data))
        break