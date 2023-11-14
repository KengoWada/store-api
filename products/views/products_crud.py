from http import HTTPStatus

from django.urls import path
from rest_framework.response import Response

from core.mixins import StaffOrReadOnlyAPIViewMixin
from core.pagination import ResultSetPagination
from core.permissions import IsStaffOrReadOnly

from products.models import Product
from products.serializers import ProductSerializer


class ProductCreateListAPIView(StaffOrReadOnlyAPIViewMixin):
    permission_classes = [IsStaffOrReadOnly]
    paginator = ResultSetPagination()

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            response = {"error": serializer.errors}
            return Response(response, status=HTTPStatus.BAD_REQUEST)

        serializer.save()
        response = {"message": "Done", "product": serializer.data}
        return Response(response, status=HTTPStatus.CREATED)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(is_removed=False)

        products = products.order_by("created_at")
        products = self.paginator.paginate_queryset(queryset=products, request=request)

        serializer = ProductSerializer(products, many=True)
        response = self.paginator.get_paginated_response(serializer.data)
        return Response(response, status=HTTPStatus.OK)


class ProductDetailsUpdateAPIView(StaffOrReadOnlyAPIViewMixin):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("id")
        is_staff = request.user.is_authenticated and request.user.is_staff

        product = Product.objects.filter(pk=product_id).first()
        if product is None or (not is_staff and product.is_removed):
            response = {"error": "Invalid product id."}
            return Response(response, status=HTTPStatus.NOT_FOUND)

        serializer = ProductSerializer(product)
        response = {"message": "Done", "product": serializer.data}
        return Response(response, status=HTTPStatus.OK)

    def patch(self, request, *args, **kwargs):
        product_id = kwargs.get("id")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            response = {"error": "Invalid product id."}
            return Response(response, status=HTTPStatus.NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            response = {"error": serializer.errors}
            return Response(response, status=HTTPStatus.BAD_REQUEST)

        serializer.save()
        response = {"message": "Done", "product": serializer.data}
        return Response(response, status=HTTPStatus.OK)


urlpatterns = [
    path("", ProductCreateListAPIView.as_view(), name="products-create-list"),
    path(
        "<int:id>/",
        ProductDetailsUpdateAPIView.as_view(),
        name="product-details-update",
    ),
]
