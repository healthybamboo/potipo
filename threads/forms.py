from django import forms
from threads.models import Question, Answer, Reason, ParentCategory, Category
from django.utils import timezone
from datetime import timedelta

# 質問を検索するためのフォーム


class SearchQuestionForm(forms.Form):
    # 　ここでは単にデータベースからデータを取得するだけ

    # 最大１００文字までテキストを入力できる
    text = forms.CharField(max_length=100)

    # 親カテゴリーを選択するためのフォームとして、全ての親カテゴリーを渡す（選択は必須ではない）
    pc = ParentCategory.objects.all()
    parent_category = forms.ModelChoiceField(pc, required=False)

    # 上記の親に対しての子供カテゴリーを選択するためのフォームとして、全ての子供カテゴリーを渡す（選択は必須ではない）
    c = Category.objects.all()
    category = forms.ModelChoiceField(c, required=False)


# 何日後かを選択と、その日のtimestampを返す関数
def add_some_days(cdays):
    return (timezone.now() + timedelta(days=cdays)).strftime("%Y-%m-%d 23:59:59")


# 質問の期限を設定するにあたり選択できる日数のリストを返す関数
def get_days_list():
    # 選択肢を格納するリスト
    days_list = []

    # ２週間分をリストにして返す
    for i in range(1, 15):
        text = str(i) + "日後"
        if i == 1:
            text = "明日"
        elif i == 2:
            text = "明後日"
        elif i == 7:
            text = "1週間後"
        elif i == 14:
            text = "2週間後"

        days_list.append((add_some_days(i), text))
    return days_list


# 質問を新規で作成するためのフォーム
class QuestionCreateForm(forms.ModelForm):
    class Meta:
        # Questionモデルとの紐付けを行う
        model = Question
        fields = ('text', 'let_answer_add', 'let_reason_add',
                  'reply_dead_line', 'parent_category', 'category')
        
        # 回答の期限を選択するためのフォームとして、上記の関数で作成したリストを渡す（選択は必須ではない）
        widgets = {'reply_dead_line': forms.Select(choices=get_days_list())}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 質問の内容を入力するためのフォームにidを付与する
        self.fields['text'].widget.attrs['id'] = 'qtext'
        
        # 質問の内容を入力するためのフォームにplaceholderを付与する
        self.fields['text'].widget.attrs['placeholder'] = '質問内容'
        
        # 質問の内容を入力するためのフォームは100文字まで入力可能である
        self.fields['text'].widget.attrs['maxlength'] = '100'
        
        # 質問の追加を許可するかどうかのチェックボックスにidを付与する
        self.fields['let_answer_add'].widget.attrs['class'] = 'let'
        
        # 理由の追加を許可するかどうかのチェックボックスにidを付与する
        self.fields['let_reason_add'].widget.attrs['class'] = 'let'
        
        # 質問の期限を選択するためのフォームにidを付与する
        self.fields['reply_dead_line'].widget.attrs['class'] = 'let'
        
        # カテゴリーを選択するためのフォームにidを付与する
        self.fields['category'].widget.attrs['required'] = 'True'


AnswerFormset = forms.inlineformset_factory(
    Question, Answer, fields=(('text',)),
    extra=2, max_num=10, can_delete=False,
)


# 回答を新規で作成するためのフォーム
class AnswerCreateForm(forms.ModelForm):
    class Meta:
        # Answerモデルとの紐付けを行う
        model = Answer
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 回答の内容を入力するためのフォームにplaceholderを付与する
        self.fields['text'].widget.attrs['placeholder'] = '選択肢'
        
        # 回答の内容を入力するためのフォームは50文字まで入力可能である
        self.fields['text'].widget.attrs['maxlength'] = '50'


# 理由を新規で作成するためのフォーム
class ReasonCreateForm(forms.ModelForm):
    class Meta:
        # Reasonモデルとの紐付けを行う
        model = Reason
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 理由を入力するためのフォームにplaceholderを付与する
        self.fields['text'].widget.attrs['placeholder'] = '理由'
        
        # 理由を入力するためのフォームは50文字まで入力可能である
        self.fields['text'].widget.attrs['maxlength'] = '50'
