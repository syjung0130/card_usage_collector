# -*- coding: utf-8 -*-
import pandas as pd
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

from os.path import exists

class KBCardUsageCollector:
    def __init__(self) -> None:
        self.font_path = ".\\nanum-all\\나눔 글꼴\\나눔고딕\\NanumFontSetup_TTF_GOTHIC\\NanumGothic.ttf"
        self.df_cols = []
        self.col_names_to_be_deleted = []

    def set_font(self):
        self.font = font_manager.FontProperties(fname=self.font_path).get_name()
        rc('font', family=self.font)

    def read_dataframe(self, file_path):
        self.xl_path = file_path
        file_exists = exists(file_path)
        self.df = pd.read_excel(self.xl_path)

    def redefine_dataframe(self):
        for col in self.df.columns:
            if 'Unnamed: ' in col:
                self.col_names_to_be_deleted.append(col)
                continue
            # print('{0}'.format(repr(col)))
            self.df_cols.append(col)

        self.col_names_to_be_deleted.append('승인번호')
        # col_names_to_be_deleted.append('상태')
        self.col_names_to_be_deleted.append('적립(예상)\n포인트리')
        self.col_names_to_be_deleted.append('할인금액')
        self.col_names_to_be_deleted.append('해외이용금액\n($)')

        self.df_redefined = self.df.drop(self.col_names_to_be_deleted, axis=1)
        # print(df_redefined)
        self.df_redefined = self.df_redefined[self.df_redefined['결제예정일'] == '2023-01-05']
        cancled_idx = self.df_redefined[self.df_redefined['상태'] == '취소전표매입'].index
        self.df_redefined = self.df_redefined.drop(cancled_idx)
        print(self.df_redefined)
    
    def show_price_by_store(self):
        dict_stores = {}
        for store in self.df_redefined['이용하신곳']:
            if not store in dict_stores:
                # 한 가게에서 쓴 금액 총액 구하기
                df_store = self.df_redefined[self.df_redefined['이용하신곳'] == store]
                dict_stores[store] = df_store['국내이용금액\n(원)'].sum()
                # print('type: {0}'.format(type(df_store)))
        
        plt.barh(range(len(dict_stores)), list(dict_stores.values()), align='center')
        plt.yticks(range(len(dict_stores)), list(dict_stores.keys()))
        plt.show()

if __name__ == "__main__":
    collector = KBCardUsageCollector()

    collector.set_font()
    xl_path = '.\카드이용내역_20221124_20221224.xls'
    collector.read_dataframe(xl_path)
    collector.redefine_dataframe()
    collector.show_price_by_store()