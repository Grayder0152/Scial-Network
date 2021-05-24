from .models import Post, LikeAnalytics
from .serializers import PostSerializer
from .services import format_date, date_generator, is_liked

from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        for post in self.get_queryset():
            post.is_liked = is_liked(post, user)
            post.save()
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['author'] = self.request.user.id
        return super().post(request, *args, **kwargs)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        post = self.get_queryset().first()
        post.is_liked = is_liked(post, self.request.user)
        post.save()
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs.get('pk'))
        if post.author.id == self.request.user.id:
            request.data['author'] = self.request.user.id
            return super().update(request, *args, **kwargs)
        return Response({"PermissionError": "This post can change only it author"})

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs.get('pk'))
        if post.author.id == self.request.user.id:
            return super().destroy(request, *args, **kwargs)
        return Response({"PermissionError": "This post can delete only it author"})


class PostLike(generics.UpdateAPIView):
    queryset = Post.objects.all()

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        if user not in post.liked_by.all():
            post.liked_by.add(user)
            LikeAnalytics.objects.create(user=user, post=post)
            response = {"Like": "You have successfully LIKED the post"}
        else:
            post.liked_by.remove(user)
            LikeAnalytics.objects.get(user=user, post=post).delete()
            response = {"Unlike": "You have successfully REMOVE the like from the post"}

        post.save()
        return Response(response)


class LikeAnalyticsViews(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        if 'date_from' in request.query_params and 'date_to' in request.query_params:
            date_from = format_date(request.query_params.get('date_from'))
            date_to = format_date(request.query_params.get('date_to'))

            if date_to < date_from:
                return Response({"DateError": "'date_to' must be bigger then 'date_from'"})

            analytics = LikeAnalytics.objects.filter(
                Q(liked_time__gte=date_from) & Q(
                    liked_time__lte=date_to))

            response = {}
            for i in date_generator(date_from, date_to):
                response[f'{i}'] = analytics.filter(liked_time=i).count()
            return Response(response)
        else:
            return Response({"ParametersError": "You must pass two parameters: 'date_from' and 'date_to'"})


class UserActivity(generics.GenericAPIView):

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user is not None:
            return Response({
                "last_login": user.last_login.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                "last_active": user.profile.last_request.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            })
        return Response({
            "FoundError": "User not found"
        })


class LoginApiViews(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.data['username'])
        user.last_login = timezone.localtime()
        user.save()
        return super().post(request, *args, **kwargs)
