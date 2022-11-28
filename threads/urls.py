from django.urls import path
from . import views

app_name = 'threads'

urlpatterns = [
    path('',views.Top.as_view(),name ="top"),
    path('question/create',views.CreateQuestion.as_view(),name="create_question"),
    path('question/latest',views.LatestList.as_view(),name="latest_question"),
    path('question/popular',views.PopulateList.as_view(),name="popular_question"),
    path('searchquestions',views.SearchQuestion.as_view(),name="search_question"),

    path('question/<int:pk>/',views.QuestionDetail.as_view(),name="detail_question"),
    path('question/<int:pk>/createanswer',views.CreateAnswer.as_view(),name="ca"),
    path('voteanswer',views.voteAnswer,name="va"),

    path('answer/<int:pk>/',views.AnswerDetail.as_view(),name="ad"),
    path('answer/<int:pk>/createreason',views.CreateReason.as_view(),name="cr"),
    path('votereason',views.voteReason,name="vr"),

    path('question/<int:pk>/result',views.Result.as_view(),name="rt"),
    path('question/<int:pk>/oriclo',views.OriginalQuestionAndCloneQuestions.as_view(),name="oc"),

    path('question/clonecreate',views.createclone,name="cc"),

]
