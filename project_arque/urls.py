from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from content_manager.views import ArticleViewSet, GalleryPostViewSet
from contact_form.views import ContactSubmissionCreateView
from django.conf import settings
from django.views.static import serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from contact_form.views import api_upload_video

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'gallery-posts', GalleryPostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/contact/', ContactSubmissionCreateView.as_view(), name='contact_submit'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/upload-video/', api_upload_video),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]