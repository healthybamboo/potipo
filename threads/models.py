from django.db import models
from datetime import timedelta
from django.utils import timezone


# 親カテゴリーのモデル
class ParentCategory(models.Model):
    # 名前は50文字まで（カテゴリーなら十分）
    name = models.CharField(max_length=50)

    # 親カテゴリーの名前を返す
    def __str__(self):
        return self.name


# 子カテゴリーのモデル
class Category(models.Model):
    # 名前は50文字まで
    name = models.CharField(max_length=50)
    
    # 親カテゴリーの外部キーを設定
    parent = models.ForeignKey(ParentCategory, on_delete=models.PROTECT)

    # カテゴリーの名前を返す
    def __str__(self):
        return self.name


# 質問のモデル
class Question(models.Model):
    # 三日後を返す
    def in_three_days():
        return timezone.now() + timedelta(days=3)
    
    # 質問のタイトルは100文字まで
    text = models.CharField(max_length=100)
    
    # 質問の期限はデフォルトで三日後
    reply_dead_line = models.DateTimeField(default=(in_three_days()))
    
    # 回答の合計値、最初は０
    all_answer_numbers = models.PositiveIntegerField(default=0)
    
    # 質問の追加を許可するかどうか
    let_answer_add = models.BooleanField(default=False)
    
    # 理由の追加を許可するかどうか
    let_reason_add = models.BooleanField(default=False)
    
    # 質問の親カテゴリー
    parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, default=None)
    
    # 質問のカテゴリー
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None)

    # 質問がcloneであったときに、その元になった質問を保持する
    original_question = models.PositiveIntegerField(default=0)
    
    # 質問の作成日
    created_time = models.DateTimeField(auto_now_add=True,)
    
    # 質問がアクティブかどうか
    question_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.text


# 回答のモデル
class Answer(models.Model):
    # 回答の文字数は50文字まで
    text = models.CharField(max_length=50)
    
    # 回答する質問の外部キーを設定
    parent_question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answer')
    
    # 投票数を保持
    vote = models.PositiveIntegerField(default=0,)

    # 回答を返す
    def __str__(self):
        return self.text

# 理由のモデル
class Reason(models.Model):
    # 理由の文字数は50文字まで
    text = models.CharField(max_length=50)
    
    # 理由付けする回答の外部キーを設定
    parente_answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='reason')
    
    # 理由の投票数を保持
    vote = models.PositiveIntegerField(default=0,)

    # 理由を返す
    def __str__(self):
        return self.text
