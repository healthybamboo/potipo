import pytest
from freezegun import freeze_time
from django.test import client
from django.core.management import call_command


# テストの共通処理
class TesTemp:
    # セットアップを行う
    @pytest.fixture(autouse=True, scope='class')
    def setUp(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            # # fixturesからデータを読んでDBに入れる
                call_command('loaddata', 'threads/fixtures/parent_category.json')
                call_command('loaddata', 'threads/fixtures/category.json')
                call_command('loaddata', 'tests/assets/question.json')
            
# トップページのテスト
class TestTopPage(TesTemp):
    # 正しくページが表示されるか
    @pytest.mark.django_db
    def test_show_top_page(self):
        c = client.Client()
        response = c.get('/')
        assert response.status_code == 200

# 詳細ページのテスト
class TestQuestionDetail(TesTemp):
    # 正しくページが表示されるか
    @freeze_time("2022-11-25")
    @pytest.mark.django_db
    def test_show_question_detail(self):
        c = client.Client()
        response = c.get('/question/1/')
        assert response.status_code == 200    
    
    # テキストが正しく表示されるか
    @freeze_time("2022-11-25")
    @pytest.mark.django_db
    def test_is_title_correct(self):
        c = client.Client()
        response = c.get('/question/1/').content.decode('utf-8')
        
        assert 'ハローワールド' in response 
     
    # テキストが正しく表示されるか２
    @freeze_time("2022-11-25")
    @pytest.mark.django_db
    def test_is_title_correct2(self):
        c = client.Client()
        response = c.get('/question/4/').content.decode('utf-8')
        
        assert '夢か現実か'in response
        
    # 期限切れの質問ならば、リダイレクトされるか
    @freeze_time("2022-11-27")
    @pytest.mark.django_db
    def test_over_reply_dead_line(self):
        c = client.Client()
        response = c.get('/question/1')
        
        assert response.status_code == 301 or response.status_code == 302
    

# 新着質問ページのテスト
class TestLatestQuestion(TesTemp):
    # 正しくページが表示されるか
    @pytest.mark.django_db
    def test_show_question_detail(self):
        c = client.Client()
        response = c.get('/question/latest')
        assert response.status_code == 200    

# 人気質問ページのテスト
class TestPopulerQuestion(TesTemp):
    # 正しくページが表示されるか
    @pytest.mark.django_db
    def test_show_question_detail(self):
        c = client.Client()
        response = c.get('/question/popular')
        assert response.status_code == 200
    
# 質問作成ページのテスト
class TestCreateQuestion(TesTemp):
    # 正しくページが表示されるか
    @pytest.mark.django_db
    def test_show_question_detail(self):
        c = client.Client()
        response = c.get('/question/create')
        assert response.status_code == 200
        
# 回答作成ページのテスト
class TestCreateAnswer(TesTemp):
    # 正しくページが表示されるか
    @pytest.mark.django_db
    def test_show_question_detail(self):
        c = client.Client()
        response = c.get('/question/1/createanswer')
        assert response.status_code == 200
        
class TesTemp2():
    @pytest.fixture(autouse=True, scope='class')
    def setUp(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            # # fixturesからデータを読んでDBに入れる
                call_command('loaddata', 'threads/fixtures/parent_category.json')
                call_command('loaddata', 'threads/fixtures/category.json')
                call_command('loaddata', 'tests/assets/question.json')
                call_command('loaddata', 'tests/assets/answer.json')
    

# 理由作成ページのテスト
class TestCreateReason(TesTemp2):
    # 正しくページが表示されるか
    @pytest.mark.django_db
    def test_show_create_reason(self):
        c = client.Client()
        response = c.get('/answer/1/createreason')
        assert response.status_code == 200