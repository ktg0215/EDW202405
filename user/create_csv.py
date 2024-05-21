import pandas as pd
from django.core.management.base import BaseCommand
from user.models import CustomUser
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Import data from CSV to CustomUser model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV file path')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        df = pd.read_csv(csv_file_path)

        for index, row in df.iterrows():
            user_id = row['user_id']
            user_name = row['user_name']
            job = row['job']
            user_no = row['user_no']
            password = row['password']  # パスワードをCSVから読み込む

            # Check if a CustomUser instance already exists based on user_id
            custom_user, created = CustomUser.objects.get_or_create(user_id=user_id)

            # Update user_name, job, and user_no
            custom_user.user_name = user_name
            custom_user.username =user_id
            custom_user.user_id=user_id
            custom_user.job = job
            custom_user.user_no = user_no
            custom_user.password = make_password(password)  # ハッシュ化されたパスワードを保存
            custom_user.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully imported user with ID: {user_id}'))


            #python manage.py create_csv user_create.csv
            #でcsvを読み込む、python manage.py ファイル名.py　csvファイル名