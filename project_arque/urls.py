from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from content_manager.views import ArticleViewSet, GalleryPostViewSet
from contact_form.views import ContactSubmissionCreateView, api_upload_video
from django.conf import settings
from django.views.static import serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'gallery-posts', GalleryPostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/contact/', ContactSubmissionCreateView.as_view(), name='contact_submit'),
    path('api/upload-video/', api_upload_video, name='api_upload_video'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]