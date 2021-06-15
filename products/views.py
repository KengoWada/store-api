from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from products import products_crud
from products.models import Product
from products.permissions import IsStaffOrReadOnly
from products.serializers import GetProductSerializer


class ProductCreateList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]

    def post(self, request):
        return products_crud.create(request=request)

    def get(self, request):
        return products_crud.get_not_deleted(request=request)


class ProductRetrieveUpdateDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]

    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(self.request, product)
            return product
        except Product.DoesNotExist:
            return None

    def get(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            response = {'message': 'Invalid product id'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return products_crud.get_by_id(request=request, product=product)

    def patch(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            response = {'message': 'Invalid product id'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return products_crud.patch(request=request, product=product)

    def put(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            response = {'message': 'Invalid product id'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return products_crud.update(request=request, product=product)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            response = {'message': 'Invalid product id'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return products_crud.delete(request=request, product=product)
