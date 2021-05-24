from .views import (
    PostList,
    PostDetail,
    PostLike,
    LikeAnalyticsViews,
    UserActivity,
    LoginApiViews
)

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('<int:pk>/like/', PostLike.as_view()),
    path('analytics/', LikeAnalyticsViews.as_view()),
    path('user-activity/<str:username>/', UserActivity.as_view()),
    path('token/', LoginApiViews.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
