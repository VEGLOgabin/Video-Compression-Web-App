from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Video file size compressor API",
        default_version='v1',
        description="We are helping all users across the world to compress their video file",
        contact=openapi.Contact(email="contact.video@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)