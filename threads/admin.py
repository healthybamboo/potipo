from django.contrib import admin
from .models import Question,Answer,Reason,Category,ParentCategory,Category

# 理由モデルを管理画面に登録
class ReasonAdmin(admin.ModelAdmin):
    fieldsets = [
    ('選択肢',{'fields':['text','parente_answer','vote']}),
    ]

class ReasonInline(admin.StackedInline):
    model = Reason
    extra = 3
    can_delete = False
    verbose_name = '理由'
    fields = ('text','vote')

# 回答モデルを管理画面に登録
class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
    ('選択肢',{'fields':['text','parent_question','vote']}),
    ]
    inlines = [ReasonInline]

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 5
    can_delete = False
    verbose_name = '選択肢'
    fields = ('text','vote')

# 質問モデルを管理画面に登録
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
    ('内容',
    {'fields':['text']}),
     ('permit',
     {'fields':['reply_dead_line','let_answer_add','let_reason_add','parent_category','category']}),
     ('property',
     {'fields':['original_question','all_answer_numbers','question_active']}
     )
    ]
    inlines = [AnswerInline]

# カテゴリーモデルを管理画面に登録
class CategoryInline(admin.StackedInline):
    model = Category
    extra = 10
    can_delete = False
    verbose_name = 'カテゴリ'
    fields = ('name',)

# 親カテゴリーモデルを管理画面に登録
class ParentCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
    ('カテゴリ',
    {'fields':['name']}
    ),
    ]
    inlines = [CategoryInline]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Reason,ReasonAdmin)
admin.site.register(ParentCategory,ParentCategoryAdmin)
admin.site.register(Category)
