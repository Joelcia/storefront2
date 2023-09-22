from django.apps import AppConfig
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Collection, Product
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from .serializers import CollectionSerializer, ProductSerializer


# Create your views here.
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related(
            'collection').all()  # TO AVOID LAZY LOADING
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


    """ 
    REPLACED BY CODE ABOVE
    def get_queryset(self):
        return Product.objects.select_related(
            'collection').all()  # TO AVOID LAZY LOADING
    
    def get_serializer_class(self):
        return ProductSerializer """ 
    
    """ 
    REPLACED BY CODE ABOVE
    def get(self, request):
        queryset = Product.objects.select_related(
            'collection').all()  # TO AVOID LAZY LOADING
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)  # serializer
        serializer.is_valid(raise_exception=True)  # validate data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) """


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

       """  def get(self,request,id):
            product = get_object_or_404(Product, pk=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        
        def put(self,request):
            product = get_object_or_404(Product, pk=id)
            serializer = ProductSerializer(
                product, data=request.data)  # serializer
            serializer.is_valid(raise_exception=True)  # validate data
            serializer.save()
            return Response(serializer.data)
 """
        def delete(self,request):
            product = get_object_or_404(Product, pk=id) 
            if product.orderitems.count() > 0:
                return Response({'error': 'Product can not be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

""" 
REPLACED BY ABOVE
@api_view(['GET', 'POST', ])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)  # serializer
        serializer.is_valid(raise_exception=True)  # validate data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) """


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404((Collection.objects.annotate(
        products_count=Count('products'))), pk=id)

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollectionSerializer(
            collection, data=request.data)  # serializer
        serializer.is_valid(raise_exception=True)  # validate data
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection can not be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
