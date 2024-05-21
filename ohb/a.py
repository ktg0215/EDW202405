import pandas as pd
import os
from models import Ohb_items
import django



# Djangoの設定を読み込むための環境変数を設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # config.settings を適切な設定ファイルのパスに置き換えてください

# Djangoの初期化

django.setup()

def import_csv_to_model(csv_file_path):
    # CSVファイルをPandas DataFrameとして読み込む
    df = pd.read_csv(csv_file_path)

    # DataFrameをモデルに登録する
    for index, row in df.iterrows():
        # CSVの各列からデータを取得
        item_name = row['item_name']
        item_price = row['item_price']
        item_type = row['item_type']
        item_no = row['item_no']

        # モデルのインスタンスを作成して保存
        Ohb_items.objects.create(
            item_name=item_name,
            item_price=item_price,
            item_type=item_type,
            item_no=item_no
        )

# 使用例
csv_file_path = 'static/db.csv'  # CSVファイルのパスを適切に指定してください
import_csv_to_model(csv_file_path)

if __name__ == "__main__":
    # ここで処理を実行する
    pass