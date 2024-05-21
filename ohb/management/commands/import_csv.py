import pandas as pd
from django.core.management.base import BaseCommand
from ohb.models import Ohb_items, Items_Counts
from datetime import datetime

class Command(BaseCommand):
    help = 'Import data from CSV to Items_Counts model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV file path')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        df = pd.read_csv(csv_file_path)

        for index, row in df.iterrows():
            item_name = row['item']  # Assuming 'item' column in CSV contains item_name

            # Get or create the corresponding Ohb_items instance based on item_name
            ohb_item, created = Ohb_items.objects.get_or_create(item_name=item_name)

            item_create = row['item_create']
            item_los = row['item_los']

            # Convert date to YYYY-MM-DD format
            date_str = row['date']
            try:
                date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')
            except ValueError:
                self.stdout.write(self.style.ERROR(f'Invalid date format: {date_str}. Skipping.'))
                continue

            # Check if Items_Counts instance already exists for the date and item
            items_counts, created = Items_Counts.objects.get_or_create(
                item=ohb_item,
                date=date,
                defaults={'item_create': item_create, 'item_los': item_los}
            )

            # Update item_create and item_los if the instance already exists
            if not created:
                items_counts.item_create = item_create
                items_counts.item_los = item_los
                items_counts.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {item_name}'))
            #ターミナルで
            #python manage.py import_csv your_csv_file.csv
            #を実行するとCSVから読み込める、csvメモ帳を経由して保存しないとUTF8にならない


# import pandas as pd
# from django.core.management.base import BaseCommand
# from user.models import CustomUser
# from django.contrib.auth.hashers import make_password

# class Command(BaseCommand):
#     help = 'Import data from CSV to CustomUser model'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str, help='CSV file path')

#     def handle(self, *args, **kwargs):
#         csv_file_path = kwargs['csv_file']
#         df = pd.read_csv(csv_file_path)

#         for index, row in df.iterrows():
#             user_id = row['user_id']
#             user_name = row['user_name']
#             job = row['job']
#             user_no = row['user_no']
#             password = str(row['user_id'])  # パスワードをCSVから読み込む

#             # Check if a CustomUser instance already exists based on user_id
#             custom_user, created = CustomUser.objects.get_or_create(user_id=user_id)

#             # Update user_name, job, and user_no
#             custom_user.user_name = user_name
#             custom_user.username =user_id
#             custom_user.user_id=user_id
#             custom_user.job = job
#             custom_user.user_no = user_no
#             custom_user.password = make_password(password)  # ハッシュ化されたパスワードを保存
#             custom_user.save()

#             self.stdout.write(self.style.SUCCESS(f'Successfully imported user with ID: {user_id}'))


            #python manage.py create_csv user_create.csv
            #でcsvを読み込む、python manage.py ファイル名.py　csvファイル名