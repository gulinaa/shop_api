from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.filters import ProductFilter
from main.models import Product, ProductImage, Category, Review
from main.serializers import ProductListSerializer, ProductSerializer, ProductImageSerializer, CategorySerializer, \
    ReviewSerializer


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductListSerializer(products, many=True)
#     return Response(serializer.data)


# class ProductListView(APIView):
#     def __get__(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)


# class ProductListView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer


class ListCreateProductsView(ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer


# class ProductDetailsView(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#

class RetrieveUpdateDeleteProductView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description' 'category__name']
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.request.method == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_permissions(self): #создавать/удалять/редактировать может только админ а просматривать могут все
        if self.action in ['list', 'retrieve']:
            return []
        elif self.action == 'reviews':
            if self.request.method == 'POST':
                return [IsAuthenticated()]
            return []
        return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        data = request.data
        images = data.pop('images')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return Response(serializer.data)

    # api/v1/products/id/
    @action(methods=['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        data = request.data
        serializer = ReviewSerializer(data=data, context={'request': request, 'product': product})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):  # создавать/удалять/редактировать может только админ а просматривать могут все
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]


class CreateReview(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class UpdateDeleteReview(UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)