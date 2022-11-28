from django.shortcuts import (
    render,
    redirect,
    HttpResponse,
    get_object_or_404,
    get_list_or_404,
    Http404,
)
from .models import Question, Answer, Reason, ParentCategory, Category
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import (
    QuestionCreateForm,
    AnswerFormset,
    AnswerCreateForm,
    ReasonCreateForm,
    add_some_days,
    SearchQuestionForm,
)
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.forms.utils import ErrorList
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

# 質問を作成するためのview
class CreateQuestion(generic.CreateView):

    # Questioモデルを使う
    model = Question

    # 質問を作成するためのフォームとテンプレートの関連付けを行う
    template_name = "threads/create_question.html"
    form_class = QuestionCreateForm

    # 質問の作成が完了したら、作成した質問の回答ページにリダイレクトする
    def get_success_url(self):
        return reverse("threads:detail_question", kwargs={"pk": self.object.id})

    # Getでアクセスされたときの処理
    def get_context_data(self, **kwargs):
        # コンテキストを設定
        ctx = super(CreateQuestion, self).get_context_data(**kwargs)

        # POSTリクエスとの場合？
        if self.request.method == "POST":
            ctx["formset"] = AnswerFormset(self.request.POST,
                                           self.request.FILES)

        # GETリクエストの場合
        else:
            # 親カテゴリを全て取得
            ctx["parentcategory_list"] = ParentCategory.objects.all()

            # 回答のフォームを設定
            ctx["formset"] = AnswerFormset()

        # コンテキストを返す
        return ctx

    # フォームからPOSTでアクセスされたときの処理
    def form_valid(self, form):
        ctx = self.get_context_data()

        # フォームセットを取得
        formset = ctx["formset"]

        # 正しいフォームセットかどうかをチェック
        if formset.is_valid():
            # 入力内容を保存
            self.object = form.save(commit=False)
            formset.instance = self.object
            answers = formset.save(commit=False)

            # 回答の数を確認
            count = len(answers)

            # 回答数が2つ以上の場合
            if count >= 2:
                # 質問を保存
                self.object.save()
                # 回答を保存
                formset.save()

            # 回答数が2つ未満の場合
            else:
                # topページにリダイレクト
                return redirect("threads:top")

        # フォームが正しくない場合
        else:
            ctx["form"] = form

            # そのままフォームを返す
            return self.render_to_response(ctx)

        #
        result = super().form_valid(form)
        messages.success(self.request, "「{}」を作成しました".format(form.instance))
        return result


# 回答を作成するためのview
class CreateAnswer(generic.CreateView):

    # Answerモデルを使う
    model = Answer

    # 回答を作成するためのフォームとテンプレートの関連付けを行う
    template_name = "threads/create_answer.html"
    form_class = AnswerCreateForm

    # Getでアクセスされたときの処理
    def get_context_data(self, **kwargs):
        ctx = super(CreateAnswer, self).get_context_data(**kwargs)

        # quetionに質問のQuestionObjectを入れる
        ctx["question"] = get_object_or_404(Question, pk=self.kwargs["pk"])

        return ctx

    # postされたときの処理
    def form_valid(self, form):
        # バリデーションが通ったときの処理
        if form.is_valid():
            # questionを取得する
            question = get_object_or_404(Question, pk=self.kwargs["pk"])

            # 現在時刻が質問の終了時刻よりも前であるか
            if question.reply_dead_line > timezone.now():

                # 回答の追加が許可されているか
                if question.let_answer_add:
                    # formの内容を保存する
                    self.object = form.save(commit=False)

                    # 回答の対象となる質問を設定する
                    self.object.parent_question = question

                    # 回答の投票数の初期値は回答の作成者の分を足して１とする
                    self.object.vote = 1

                    # 保存する
                    self.object.save()

                    # 質問の回答数を１増やす
                    question.all_answer_numbers += 1

                    # 変更を保存する
                    quetion.save()

                # 回答の追加が許可されていない場合
                else:
                    # 質問の詳細ページにリダイレクトする
                    return redirect("threads:detail_question", question.id)

            # 質問の回答期限が過ぎている場合
            else:
                # 質問の結果ページにリダイレクトする
                return redirect("threads:rt", question.id)

        # バリデーションが通らなかった場合
        else:
            ctx["form"] = form
            return self.render_to_response(ctx)

        # 処理が終わったら結果を返す
        result = super().form_valid(form)
        messages.success(self.request, "「{}」を作成しました".format(form.instance))
        return result

    # 回答の作成が完了したら、作成した回答の回答ページにリダイレクトする
    def get_success_url(self):
        # 回答の対象となる質問のidを取得
        question = self.object.parent_question

        # 質問のQ<質問ID>をkeyとして、
        key = "Q" + str(question.id)

        # もし、理由の追加が許可されていれば、
        if question.let_reason_add:
            self.request.session[key] = self.object.id
            return reverse("threads:ad", kwargs={"pk": self.object.id})

        # 許可されていなければ、質問の回答ページにリダイレクトする
        else:
            self.request.session[key] = 0
            return reverse("threads:rt",
                           kwargs={"pk": self.object.question.id})


# 理由は作成するためのview
class CreateReason(generic.CreateView):

    # Reasonモデルを使う
    model = Reason

    # 回答に対する理由を作成するためのフォームとテンプレートの関連付けを行う
    template_name = "threads/create_reason.html"
    form_class = ReasonCreateForm

    # 理由の作成が完了したら、大元の質問のページにリダイレクトする
    def get_success_url(self):
        return reverse(
            "threads:rt",
            kwargs={"pk": self.object.parente_answer.parent_question.id})

    # templateに埋め込む変数を設定する
    def get_context_data(self, **kwargs):
        ctx = super(CreateReason, self).get_context_data(**kwargs)

        # answerに回答のAnswerObjectを入れる
        ctx["answer"] = get_object_or_404(Answer, pk=self.kwargs["pk"])
        return ctx

    # postされたときの処理
    def form_valid(self, form):
        answer = get_object_or_404(Answer, pk=self.kwargs["pk"])
        question = answer.parent_question

        # 現在時刻が質問の終了時刻よりも前であるかつ、理由の追加が許可されているか
        if question.reply_dead_line > timezone.now(
        ) and question.let_reason_add:
            # バリデーションが通ったか
            if form.is_valid():
                # formの内容を保存する
                self.object = form.save(commit=False)

                # 理由の対象となる回答を設定する
                self.object.parente_answer = answer

                # 理由の投票数の初期値は理由の作成者の分を足して１とする
                self.object.vote = 1

                # 保存する
                self.object.save()

                # keyを設定する
                key = "Q" + str(question.id)

                self.request.session[key] = 0

            # バリデーションが通らなかった場合
            else:
                ctx["form"] = form
                return self.render_to_response(ctx)

        # 現在時刻が質問の終了時刻よりも後であるか、理由の追加が許可されていない場合
        else:
            # 質問の結果ページにリダイレクトする
            return redirect("threads:rt", ans.parent_question.id)

        # 処理が終わったら結果を返す
        result = super().form_valid(form)
        messages.success(self.request, "「{}」を作成しました".format(form.instance))
        return result


# トップページのview
class Top(generic.ListView):

    # Questionモデルを使う
    model = Question

    # トップページ用のテンプレートを指定する
    template_name = "threads/top.html"

    # Getでアクセスされたときの処理
    def get_context_data(self, **kwargs):

        # コンテキストの設定
        ctx = super(Top, self).get_context_data(**kwargs)

        # 最新の質問一覧を10個取得する
        late_question = (Question.objects.all().filter(
            reply_dead_line__gt=timezone.now()).order_by("-created_time")[:10])

        # 作成されてからの時間を保持する
        ctime = {}
        for question in late_question:
            s = (timezone.now() - question.created_time).total_seconds()

            # 秒数を時間に直す
            hours = int(s / 3600)

            # 1日以上経過している場合
            if hours >= 24:
                # 日数を計算する
                day = int(hours / 24)
                ctime[question.id] = "約{0}日前".format(day)

            # 1時間経っていない場合
            elif hours < 1:
                # 分数を計算する
                minute = int(s / 60)

                ctime[question.id] = "約{0}分前".format(minute)

            # 　1時間以上経過していて、24時間未満の場合
            else:
                ctime[question.id] = "約{0}時間前".format(hours)

        ctx["ctime"] = ctime

        # 人気の質問の一覧を取得する
        populer_questions = (Question.objects.all().filter(
            reply_dead_line__gt=timezone.now()).order_by("-all_answer_numbers")
                             [:10])

        # 親カテゴリを全て取得する
        parent_categorys = ParentCategory.objects.all()

        # コンテキストに設定
        ctx["latestquestions"] = late_question
        ctx["populerquestions"] = populer_questions
        ctx["parent_categorys"] = parent_categorys

        # コンテキストを返す
        return ctx


# 質問を検索するview
class SearchQuestion(generic.TemplateView):

    # 質問を検索するためのテンプレートの関連付けを行う
    template_name = "threads/search_questions.html"

    # Getでアクセスされたときの処理
    def get_context_data(self, **kwargs):

        # question全て取得！？
        object_list = Question.objects.all()

        # 検索ワードを取得
        word = self.request.GET.get("word")

        # ステータスを取得
        active = self.request.GET.get("active")

        # 親カテゴリを取得
        parent_category = self.request.GET.get("parent_category")

        # 子カテゴリを取得
        category = self.request.GET.get("category")

        # 並び替えを取得
        order = self.request.GET.get("order")

        # ステータスが指定されている場合
        if active != "None":
            # 投票中の質問のみを取得
            if active == "True":
                object_list = object_list.filter(
                    reply_dead_line__gt=timezone.now())
            else:
                # 終了した質問のみを取得
                object_list = object_list.filter(
                    reply_dead_line__lt=timezone.now())

        # 親カテゴリが指定されている場合
        if parent_category:
            # 親カテゴリで絞り込み
            parent_category = ParentCategory(id=int(parent_category))
            object_list = object_list.filter(parent_category=parent_category)

        # 子カテゴリが指定されている場合
        if category:
            # 子カテゴリで絞り込み
            category = Category(id=int(category))
            object_list = object_list.filter(category=category)

        # 検索ワードが指定されている場合
        if word:
            object_list = object_list.filter(Q(text__icontains=word))

        # 回答数が多い順に並び替え
        if order == "1":
            object_list = object_list.order_by("all_answer_numbers")

        # 新しい順に並び替え
        elif order == "2":
            object_list = object_list.order_by("-created_time")

        # 古い順に並び替え
        elif order == "3":
            object_list = object_list.order_by("created_time")

        # 投票数が少ない順に並び替え
        else:
            object_list = object_list.order_by("-all_answer_numbers")

        # １ページに表示する質問の数
        MAX_PAGE_NUM = 30

        # ページネーションの設定
        paginator = Paginator(object_list, MAX_PAGE_NUM)
        page = self.request.GET.get("page", 1)
        page_num = math.floor(object_list.count() / MAX_PAGE_NUM) + 1

        try:
            pages = paginator.page(page)
        # ページ番号が整数でない場合
        except PageNotAnInteger:
            pages = paginator.page(1)
        # 空のページが指定された場合は最初のページを表示する
        except EmptyPage:
            pages = paginator.page(1)

        # コンテキストの設定
        ctx = super(SearchQuestion, self).get_context_data(**kwargs)

        # 検索ようのフォームを設定
        ctx["form"] = SearchQuestionForm

        # 親カテゴリーを設定
        ctx["parentcategory"] = ParentCategory.objects.all()

        # 質問の一覧を設定
        ctx["questions"] = pages

        # ページの数を設定
        ctx["page_num"] = page_num

        # コンテキストを返す
        return ctx


# 最新の質問を表示するためのview
class LatestList(generic.TemplateView):

    # テンプレートの関連付けを行う
    template_name = "threads/latest_questions.html"

    # Getでアクセスされたときの処理
    def get_context_data(self, **kwargs):

        # コンテキストの設定
        ctx = super(LatestList, self).get_context_data(**kwargs)

        # 最新の質問を取得
        latest_questions = (Question.objects.all().filter(
            reply_dead_line__gt=timezone.now()).order_by("-created_time"))

        # ページネーションの設定
        MAX_PAGE_NUM = 30
        paginator = Paginator(latest_questions, MAX_PAGE_NUM)
        page = self.request.GET.get("page", 1)
        page_num = math.floor(latest_questions.count() / MAX_PAGE_NUM) + 1

        try:
            pages = paginator.page(page)
        # ページ番号が整数でない場合は最初のページを表示する
        except PageNotAnInteger:
            pages = paginator.page(1)

        # 空のページが指定された場合は最初のページを表示する
        except EmptyPage:
            pages = paginator.page(1)

        # コンテキストにpagesを設定
        ctx["questions"] = pages

        # 質問がいつ作成されたかを保持する辞書
        ctime = {}

        # 最新の質問を一つずつ取り出す
        for question in latest_questions:

            # 質問が作成された時間が何秒前かを計算
            s = (timezone.now() - question.created_time).total_seconds()

            # 秒を時間に変換
            hours = int(s / 3600)

            # 1日以上前の質問の場合
            if hours >= 24:
                # 日に変換
                day = int(hours / 24)
                ctime[question.id] = "約{0}日前".format(day)

            # 1時間未満の質問の場合
            elif hours < 1:
                # 分に変換
                minute = int(s / 60)
                ctime[question.id] = "約{0}分前".format(minute)

            # 1時間以上前かつ1日未満の質問の場合
            else:
                ctime[question.id] = "約{0}時間前".format(hours)

        # コンテキストを設定
        ctx["ctime"] = ctime
        ctx["page_num"] = page_num

        # コンテキストを返す
        return ctx


# 人気の質問を表示するためのview
class PopulateList(generic.TemplateView):
    # 使用するテンプレートを指定
    template_name = "threads/populer_questions.html"

    # GETリスクエストの処理を行う
    def get_context_data(self, **kwargs):
        # １ページに表示する質問の最大数
        MAX_NUM = 30
        # コンテキストの定義
        ctx = super(PopulateList, self).get_context_data(**kwargs)

        # 人気の質問を取得する
        popular_quetions = (Question.objects.all().filter(
            reply_dead_line__gt=timezone.now()).order_by("-all_answer_numbers")
                            )
        # ページネーションの設定
        paginator = Paginator(popular_quetions, MAX_NUM)
        page_num = math.floor(popular_quetions.count() / MAX_NUM) + 1
        page = self.request.GET.get("page", 1)

        # ページネーションの処理

        # 通常は指定されたページを表示する
        try:
            pages = paginator.page(page)

        # ページ番号が整数でない場合
        except PageNotAnInteger:
            pages = paginator.page(1)
        # 空のページが指定された場合は最初のページを表示する
        except EmptyPage:
            pages = paginator.page(1)

        # コンテキストの設定
        ctx["questions"] = pages
        ctx["page_num"] = page_num

        # 最後にコンテキストを返す
        return ctx


# 　同じ質問を作成するためのview


class OriginalQuestionAndCloneQuestions(generic.ListView):

    # Questionモデルとの紐付け
    model = Question

    # GETでアクセスされたときの処理
    def get(self, request, *args, **kwargs):
        # URLのパラメータから質問を取得
        question = get_object_or_404(Question, id=self.kwargs["pk"])

        # 質問がcloneされているかどうかを判定
        if question.original_question == 0:
            origin_question = question

        # 質問がcloneされている場合は元の質問をオリジンとする
        else:
            origin_question = get_object_or_404(Question,
                                                id=question.original_question)

        # originに紐づいた質問の一覧を取得
        questions = Question.objects.all().filter(
            original_question=origin_question.id)

        # activeを最初はtrueに設定
        active = True

        # 質問の一覧が一つ以上ある場合
        if len(questions) > 0:
            # 最新の質問がまだ回答期限内の場合
            if questions.last().reply_dead_line < timezone.now():
                active = False
        else:
            # 質問がまだ回答期限内の場合
            if origin_question.reply_dead_line < timezone.now():
                active = False

        # コンテキストの設定
        context = {
            "oriquestion": origin_question,
            "cloquestions": questions,
            "active": active,
        }

        # テンプレートをレンダリングして返す
        return render(request, "threads/OQACQ.html", context)


# 質問のcloneを作成するための処理
def createclone(request):
    # POSTでアクセスされた場合
    question = get_object_or_404(Question,
                                 id=request.POST.get("original_quesion"))
    # clone達のoriginalのidを取得
    questions = Question.objects.all().filter(original_question=question.id)

    # questionはオリジナルである。
    clone_original_question = question.id

    # すでにcloneが存在する場合
    if len(questions) > 0:
        question = questions.last()
        # original_questionに紐づいたquestionのリストの最後のquestionを取得。

    # questionが回答期限内の場合
    if question.reply_dead_line < timezone.now():
        # questionの内容をコピー
        clone_text = question.text
        clone_let_answer_add = question.let_answer_add
        clone_let_reason_add = question.let_reason_add
        clone_parent_question = question.id
        clone_parent_category = question.parent_category
        clone_category = question.category

        # cloneのquestionの回答期限を設定
        somedays = (question.reply_dead_line - question.created_time).days
        clone_reply_deadline = add_some_days(somedays)

        # cloneのquestionを作成
        clone_question = Question(
            text=clone_text,
            parent_category=clone_parent_category,
            category=clone_category,
            reply_dead_line=clone_reply_deadline,
            let_answer_add=clone_let_answer_add,
            let_reason_add=clone_let_reason_add,
            original_question=clone_original_question,
        )

        # cloneのquestionを保存
        clone_question.save()

        # questionに紐づいたanswerを取得
        answers = get_list_or_404(Answer, parent_question=question)

        # 回答の内容を保持するリスト
        texts = []
        votes = []

        # questionに紐づいたanswerの内容をコピー
        for answer in answers:
            # テキストをリストについか
            texts.append(answer.text)
            # choicesのvoteとchoicesの
            votes.append(answer.vote)

        # TODO:ソートプログラムを改良する
        # バブルソート並び替え（要素数が多いと時間がかかる）
        for i in range(len(votes)):
            for j in range(len(votes) - 1, i, -1):
                if votes[j] > votes[j - 1]:
                    # voteと対応するtextも入れ替える
                    votes[j], votes[j - 1] = votes[j - 1], votes[j]
                    texts[j], texts[j - 1] = texts[j - 1], texts[j]

        # votesの上位10個のみを利用するため一部を削除
        while len(votes) > 10:
            # votesの最後の要素から削除
            texts.pop()
            votes.pop()

        # 回答を作成する処理
        for i in range(len(votes)):
            # 回答を作成する、尚votesは必要ないので設定しない
            answer = Answer(text=texts[i], parent_question=clonequestion)

            # 回答を保存
            answer.save()

        return redirect("threads:detail_question", clonequestion.id)
    else:
        return redirect("threads:latest_question")


# 質問の詳細を表示するためのview
class QuestionDetail(generic.DetailView):
    # Questionとの紐付け
    model = Question
    context_object_name = "question"

    # Getリクエストでアクセスされた場合
    def get(self, request, *args, **kwargs):
        
        # 質問を取得
        question = get_object_or_404(Question, pk=self.kwargs["pk"])
        
        # 質問が回答期限内か
        if question.reply_dead_line > timezone.now():
            
            # keyを設定
            key = "Q" + str(question.id)
            
            # もし、すでに回答済みの場合
            if key in request.session:
                
                # どこまで回答したかを表す変数
                value = request.session[key]
                
                # 全ての投票を終えた場合
                if value == 0:
                    return redirect("threads:rt", self.kwargs["pk"])
                
                # 回答のみ終えた場合
                else:
                    # valueが0でない、つまり全ての工程が終わっていなければ、answerのdeatailに飛ばす
                    return redirect("threads:ad", pk=value)
            else:
                # 回答を取得
                answers = Answer.objects.all().filter(parent_question=question)
                
                # コンテキストを設定
                ctx = {"question": question, "answers": answers}
                
                # コンテキストを返す
                return render(request, "threads/detail_question.html", ctx)
        else:
            # 結果ページに飛ばす
            return redirect("threads:rt", self.kwargs["pk"])


# 回答に投票するためのview
def voteAnswer(request):
    # 回答のidをリクエストから取得
    answer = get_object_or_404(Answer, id=request.POST.get("id"))

    # 回答の対象になる質問を取得
    question = answer.parent_question

    # 質問が回答期限内の場合
    if question.reply_dead_line > timezone.now():
        # 回答に投票
        answer.vote += 1

        # 質問の回答数を増やす
        question.all_answer_numbers += 1

        # 変更を保存
        answer.save()
        question.save()

        # ブラウザに投票したことを記録するためのkeyを作成
        key = "Q" + str(question.id)

        # 理由の追加が許可されている場合
        if question.let_reason_add:
            # cookieにkeyを保存
            request.session[key] = answer.id

            # 回答の詳細画面にリダイレクト
            return redirect("threads:ad", pk=answer.id)

        # 許可されていない場合
        else:
            # cookieにkeyを保存
            request.session[key] = 0

            # 回答の結果画面にリダイレクト
            return redirect("threads:rt", pk=question.id)
    else:
        # 回答期限を過ぎている場合は結果画面にリダイレクト
        return redirect("threads:rt", pk=question.id)


# 回答の詳細を表示するためのview


class AnswerDetail(generic.DetailView):
    # Answerとの紐付け
    model = Answer

    # templateの指定
    template_name = "threads/detail_answer.html"

    # Getリクエストの場合
    def get(self, request, *args, **kwargs):
        # 回答のidをリクエストから取得
        ans = get_object_or_404(Answer, pk=self.kwargs["pk"])
        parent_quetsion = ans.parent_question

        # 質問が回答期限内の場合
        if parent_quetsion.reply_dead_line > timezone.now():
            # 理由の一覧を取得
            reasons = Reason.objects.all().filter(parente_answer=ans)

            # コンテキストに設定
            ctx = {"answer": ans, "reasons": reasons}

            # 回答の詳細画面を表示
            return render(request, "threads/detail_answer.html", ctx)
        else:
            # 回答期限を過ぎている場合は結果画面にリダイレクト
            return redirect("threads:rt", parent_quetsion.id)


# 理由に投票するためのview
def voteReason(request):
    # 理由のidをリクエストから取得
    reason = get_object_or_404(Reason, id=request.POST.get("id"))

    # 質問を理由が紐づいた回答から取得
    question = reason.parente_answer.parent_question

    # 質問が回答期限内の場合
    if question.reply_dead_line > timezone.now():
        # 理由に投票
        reason.vote += 1

        # 変更を保存
        reason.save()

        # ブラウザに投票したことを記録するためのkeyを作成
        key = "Q" + str(question.id)

        # cookieにkeyを保存
        request.session[key] = 0

        # 回答の結果画面にリダイレクト
        return redirect("threads:rt", pk=question.id)

    else:
        # 回答期限を過ぎている場合は結果画面にリダイレクト
        return redirect("threads:rt", pk=question.id)


# 投票結果を表示するためのview
class Result(generic.DetailView):
    # Questionとの紐付け
    model = Question

    # templateの指定
    template_name = "threads/result.html"

    # Getリクエストの場合
    def get_context_data(self, **kwargs):
        # コンテキストを設定
        ctx = super(Result, self).get_context_data(**kwargs)

        # 質問をリクエストの内容から取得
        question = get_object_or_404(Question, pk=self.kwargs["pk"])

        # 質問をコンテキストに設定
        ctx["question"] = question

        # 回答の一覧を取得
        answers = Answer.objects.all().filter(parent_question=question)

        # 必要な情報のみを返すためにリストを作成
        answerlist = []

        # 回答の一覧から一つずつ回答を取り出す
        for answer in answers:
            # 回答のテキストを取得
            answer_text = answer.text

            # 回答の投票数を取得
            answer_vote = answer.vote

            # 回答の理由が存在しているか
            if Reason.objects.filter(parente_answer=answer).exists():
                # 回答の理由を保持するためのリストを作成（２次元リスト）
                reasonlist = []

                # 回答の理由の一覧を取得
                reasons = get_list_or_404(Reason, parente_answer=answer)

                # 回答の理由の一覧から一つずつ理由を取り出す
                for reason in reasons:
                    # 理由のテキストを取得
                    reason_text = reason.text

                    # 理由の投票数を取得
                    reason_vote = reason.vote

                    # 理由のテキストと投票数をまとめたリストをリストに追加
                    reasonlist.append([reason_text, reason_vote])

                # 回答のリストに、回答のテキスト、投票数、理由のリストを追加
                answerlist.append([answer_text, answer_vote, reasonlist])
            else:
                # 理由が存在しなければ、回答のリストに、回答のテキスト、投票数を追加
                answerlist.append([answer_text, answer_vote])

        # 回答のリストをコンテキストに設定
        ctx["answerlist"] = answerlist

        # 質問が回答期限内かどうかをコンテキストに設定
        ctx["question_active"] = (
            True if question.reply_dead_line > timezone.now() else False)

        # コンテキストを返す
        return ctx
