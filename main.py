from core import Core
from core import BeddingLegend


if __name__ == '__main__':
    website = str(input("Nhap trang web: "))

    if 'beddinglegend.com' not in website:
        print("Chua ho tro trang web nay!")
        try:
            input("Press Enter to continue...")
        except:
            pass
    else:
        core = BeddingLegend()

        list_category = core.get_list_category()
        stt = 0

        for category in list_category:
            data = core.get_list_item(category)
            print("Xong!")

            try:
                input("Press Enter to continue...")
            except:
                pass
            break