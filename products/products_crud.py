from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from .models import Product
from .pagination import ProductPagination
from .serializers import (GetProductSerializer, ProductSerializer,
                          StockRecordSerializer)
from .validators import (validate_create_product, validate_patch_product,
                         validate_update_product)


def create(request):
    result = validate_create_product(request.data)
    if not result['is_valid']:
        response = {'message': 'Invalid values', 'errors': result['errors']}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    product_serializer = ProductSerializer(data=request.data)
    if product_serializer.is_valid():
        product_serializer.save()

    data = {'action': 'create_product'}
    stock_record_serializer = StockRecordSerializer(data=data)
    if stock_record_serializer.is_valid():
        stock_record_serializer.save(
            user=request.user, product=product_serializer.instance)

    serializer = GetProductSerializer(product_serializer.instance)
    response = {'message': 'Done', 'product': serializer.data}
    return Response(response, status=status.HTTP_201_CREATED)


def get_all(request):
    products = Product.objects.all().order_by('created_at')

    paginator = ProductPagination()
    results = paginator.paginate_queryset(products, request=request)

    serializer = GetProductSerializer(results, many=True)

    response = paginator.get_paginated_response(serializer.data)
    return Response(response, status=status.HTTP_200_OK)


def get_not_deleted(request):
    products = Product.objects.filter(is_deleted=False).order_by('created_at')

    paginator = ProductPagination()
    results = paginator.paginate_queryset(products, request=request)

    serializer = GetProductSerializer(results, many=True)

    response = paginator.get_paginated_response(serializer.data)
    return Response(response, status=status.HTTP_200_OK)


def get_by_id(request, product):
    if product.is_deleted and not request.user.is_staff:
        response = {'message': 'Invalid id'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    serializer = GetProductSerializer(product)
    response = {'message': 'Done', 'product': serializer.data}
    return Response(response, status=status.HTTP_200_OK)


def update(request, product):
    result = validate_update_product(request.data)
    if not result['is_valid']:
        response = {'message': 'Invalid values', 'errors': result['errors']}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(
        product, data=request.data, partial=True)
    if not serializer.is_valid():
        response = {'message': 'Invalid values',
                    'errors': serializer.errors}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Keep stock records
    data = {'action': 'update_product_details'}
    stock_record_serializer = StockRecordSerializer(data=data)
    if not stock_record_serializer.is_valid():
        response = {'message': 'Invalid values',
                    'errors': stock_record_serializer.errors}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    stock_record_serializer.save(
        user=request.user, product=serializer.instance)

    serializer = GetProductSerializer(serializer.instance)

    response = {'message': 'Done', 'product': serializer.data}
    return Response(response, status=status.HTTP_200_OK)


def patch(request, product):
    result = validate_patch_product(request.data)
    if not result['is_valid']:
        response = {'message': 'Invalid values', 'errors': result['errors']}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    actions = {
        'discount_product': discount_product,
        'remove_product_discount': remove_product_discount,
        'add_product_stock': add_stock,
        'remove_product_stock': remove_stock,
    }

    action = list(request.data.keys())[0]

    func = actions.get(action, lambda: 'Invalid value')
    return func(request, product)


def discount_product(request, product):
    data = request.data['discount_product']

    product_serializer = GetProductSerializer(product, data=data, partial=True)
    if product_serializer.is_valid():
        product_serializer.save()

    data = {'action': 'discount_product'}
    stock_reccord_serializer = StockRecordSerializer(data=data)
    if stock_reccord_serializer.is_valid():
        stock_reccord_serializer.save(
            user=request.user, product=product)

    response = {'message': 'Done', 'product': product_serializer.data}
    return Response(response, status=status.HTTP_200_OK)


def remove_product_discount(request, product):
    data = {'discount_price': 0}

    product_serializer = GetProductSerializer(product, data=data, partial=True)
    if product_serializer.is_valid():
        product_serializer.save()

    data = {'action': 'discount_product'}
    stock_reccord_serializer = StockRecordSerializer(data=data)
    if stock_reccord_serializer.is_valid():
        stock_reccord_serializer.save(
            user=request.user, product=product)

    response = {'message': 'Done', 'product': product_serializer.data}
    return Response(response, status=status.HTTP_200_OK)


def add_stock(request, product):
    data = request.data['add_product_stock']

    product.quantity = F('quantity') + data['increment_by']
    product.save()

    data = {'action': 'discount_product'}
    stock_reccord_serializer = StockRecordSerializer(data=data)
    if stock_reccord_serializer.is_valid():
        stock_reccord_serializer.save(
            user=request.user, product=product)

    response = {'message': 'Done'}
    return Response(response, status=status.HTTP_200_OK)


def remove_stock(request, product):
    data = request.data['remove_product_stock']

    product.quantity = F('quantity') - data['decrement_by']
    product.save()

    data = {'action': 'discount_product'}
    stock_reccord_serializer = StockRecordSerializer(data=data)
    if stock_reccord_serializer.is_valid():
        stock_reccord_serializer.save(
            user=request.user, product=product)

    response = {'message': 'Done'}
    return Response(response, status=status.HTTP_200_OK)


def delete(request, product):
    data = {'is_deleted': True}
    product_serializer = ProductSerializer(product, data=data, partial=True)
    if not product_serializer.is_valid():
        response = {'message': 'Invalid values',
                    'errors': product_serializer.errors}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    data = {'action': 'delete_product'}
    stock_record_serializer = StockRecordSerializer(data=data)
    if not stock_record_serializer.is_valid():
        response = {'message': 'Invalid values',
                    'errors': product_serializer.errors}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    product_serializer.save()
    stock_record_serializer.save(user=request.user, product=product)

    response = {'message': 'Done'}
    return Response(response, status=status.HTTP_200_OK)
