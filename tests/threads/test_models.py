import pytest
from django.core.management import call_command
from threads.models import ParentCategory,Category
from datetime import date
import json


class Test_ParentCategory:
    @pytest.fixture(autouse=True, scope='class')
    def setUp(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            # # fixturesからデータを読んでDBに入れる
            call_command('loaddata', 'threads/fixtures/parent_category.json')

    # テストデータの読み込みが正しくできているか
    @pytest.mark.django_db
    def test_is_read_data(self):
        assert ParentCategory.objects.all().count() == 7


class Test_ChildCategory:
    @pytest.fixture(autouse=True, scope='class')
    def setUp(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            # # fixturesからデータを読んでDBに入れる
            call_command('loaddata', 'threads/fixtures/parent_category.json')
            call_command('loaddata', 'threads/fixtures/category.json')

    # テストデータの読み込みが正しくできているか
    @pytest.mark.django_db
    def test_is_read_data(self):
        assert Category.objects.all().count() == 40
