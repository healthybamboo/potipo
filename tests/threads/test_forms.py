import pytest
from freezegun import freeze_time
from threads.forms import add_some_days
from threads.forms import get_days_list


class Test_add_days_function:    
    # 1日後の日付が返ってくるか
    @freeze_time("2019-01-01")
    def test_plus_1_day(self):
        days = 1
        time = add_some_days(days)
        assert time == "2019-01-02 23:59:59"
        
    #　月をまたいだ場合のテスト
    @freeze_time("2019-01-01")
    def test_different_month(self):
        days = 31
        time = add_some_days(days)
        assert time == "2019-02-01 23:59:59"
            
    # 年をまたいだ場合のテスト
    @freeze_time("2019-12-31")
    def test_different_year(self):
        days = 1
        time = add_some_days(days)
        assert time == "2020-01-01 23:59:59"
        

class Test_get_day_list_function:
# get_days_listの単体テストでは日付はどうでもいいので、日付は固定される、日付が正しいかは前述したadd_days_functionの結果で保証される

    # リストの要素が14個あることを確認
    def test_list_size_is_14(self,mocker):
        mocker.patch("threads.forms.add_some_days", return_value = "2019-01-02 23:59:59")
        assert len(get_days_list()) == 14

    # リストの最初には明日が入っていることを確認
    def test_tommorrow(self,mocker):    
        mocker.patch("threads.forms.add_some_days", return_value = "2019-01-02 23:59:59")
        assert get_days_list()[0] == ("2019-01-02 23:59:59", "明日")
        
    # リストの二つ目には明後日が入っていることを確認
    def test_day_after_tommorrow(self,mocker):
        mocker.patch("threads.forms.add_some_days", return_value = "2019-01-02 23:59:59")
        assert get_days_list()[1] == ("2019-01-02 23:59:59", "明後日")
        
    # リストの６番目には１週間後が入っていることを確認
    def test_1_week_later(self,mocker):
        mocker.patch("threads.forms.add_some_days", return_value = "2019-01-02 23:59:59")
        assert get_days_list()[6] == ("2019-01-02 23:59:59", "1週間後")
        
    # リストの最後には２週間後月後が入っていることを確認
    def test_2_week_later(self,mocker):
        mocker.patch("threads.forms.add_some_days", return_value = "2019-01-02 23:59:59")
        assert get_days_list()[13] == ("2019-01-02 23:59:59", "2週間後")

    # リストの２番目には3日後が入っていることを確認
    def test_3_days_later(sefl,mocker):
        mocker.patch("threads.forms.add_some_days", return_value = "2019-01-02 23:59:59")
        assert get_days_list()[2] == ("2019-01-02 23:59:59", "3日後")

    # リストの最後の一つ前には13日後が入っていることを確認
    def test_13_days_later(self,mocker):
        mocker.patch("threads.forms.add_some_days", return_value = "2019-01-02 23:59:59")
        assert get_days_list()[12] == ("2019-01-02 23:59:59", "13日後")