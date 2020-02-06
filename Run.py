#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core import Core
from core import BeddingLegend


if __name__ == '__main__':
    website = str(input("Nhập trang web: "))

    if 'beddinglegend.com' not in website:
        print("Chưa hỗ trợ trang web này!")
        try:
            input("Press Enter to continue...")
        except:
            pass
    else:
        core = BeddingLegend()

        print("Đang tải xuống...")
        list_category = core.get_list_category()
        stt = 0

        for category in list_category:
            data = core.get_list_item(category)
            print("Đã hoàn thành tải xuống!")

            try:
                input("Press Enter to continue...")
            except:
                pass
            break