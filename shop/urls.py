from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import ProductViewSet, CategoryViewSet, CreateReview, UpdateDeleteReview
from order.views import OrderViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, 'products')
router.register('categories', CategoryViewSet, 'categories')
router.register('orders', OrderViewSet, 'orders')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
    # path('api/v1/reviews/', CreateReview.as_view())
    path('api/v1/reviews/<int:pk>/', UpdateDeleteReview.as_view())
]
    # path('api/v1/products/', ListCreateProductsView.as_view({'get': 'list', 'post': 'create'})),
    # path('api/v1/products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}))


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)