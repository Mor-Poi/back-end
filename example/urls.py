# example/urls.py
from django.urls import path


from example.views import (
    views,
    school_view,
    booking_view,
    checklist_view,
    template_view,
    miscellaneous_view,
    search_view,
    chart_view,
)

urlpatterns = [
    path("", views.index),
    path('login/', views.login_method,name='user_login'),
    path("booking/search", search_view.SearchAPIView.as_view(), name="search"),
    path("booking/", booking_view.BookingView.as_view(), name="booking"),
    path("booking/<str:id>/", booking_view.BookingViewID.as_view(), name="booking_id"),
    path("school/", school_view.SchoolView.as_view(), name="school"),
    path("school/<str:id>/", school_view.SchoolViewID.as_view(), name="school_id"),
    path("template/", template_view.TemplateView.as_view(), name="template"),
    path(
        "template/<str:id>/", template_view.TemplateViewID.as_view(), name="template_id"
    ),
    path("checklist/", checklist_view.ChecklistView.as_view(), name="checklist"),
    path(
        "checklist/<str:id>/",
        checklist_view.ChecklistViewID.as_view(),
        name="checklist_id",
    ),
    path("miscellaneous/", miscellaneous_view.MiscellaneousView.as_view(), name="miscellaneous"),
    path(
        "chart/1/",
        chart_view.ChartOneView.as_view(),
        name="chart_1",
    ),
    path(
        "chart/2/",
        chart_view.ChartTwoView.as_view(),
        name="chart_2",
    ),
    path(
        "chart/3/",
        chart_view.ChartThreeView.as_view(),
        name="chart_3",
    ),
    path(
        "chart/4/",
        chart_view.ChartFourView.as_view(),
        name="chart_4",
    ),
]
