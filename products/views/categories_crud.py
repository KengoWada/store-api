from http import HTTPStatus

from django.urls import path
from rest_framework.response import Response

from core.mixins import StaffOrReadOnlyAPIViewMixin

from products.models import Category
from products.serializers import CategorySerializer


class CategoryCreateListAPIView(StaffOrReadOnlyAPIViewMixin):
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            response = {"error": serializer.errors}
            return Response(response, status=HTTPStatus.BAD_REQUEST)

        serializer.save()
        response = {"message": "Done", "category": serializer.data}
        return Response(response, status=HTTPStatus.CREATED)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            categories = Category.objects.all()
        else:
            categories = Category.objects.filter(is_removed=False)

        categories = categories.order_by("created_at")
        serializer = CategorySerializer(categories, many=True)
        response = {"message": "Done", "categories": serializer.data}
        return Response(response, status=HTTPStatus.OK)


class CategoryDetailsUpdateAPIView(StaffOrReadOnlyAPIViewMixin):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get("id")
        is_staff = request.user.is_authenticated and request.user.is_staff

        category = Category.objects.filter(pk=category_id).first()
        if category is None or (not is_staff and category.is_removed):
            response = {"error": "Invalid category id."}
            return Response(response, status=HTTPStatus.NOT_FOUND)

        serializer = CategorySerializer(category)
        response = {"message": "Done", "category": serializer.data}
        return Response(response, status=HTTPStatus.OK)

    def patch(self, request, *args, **kwargs):
        category_id = kwargs.get("id")
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            response = {"error": "Invalid category id."}
            return Response(response, status=HTTPStatus.NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            response = {"error": serializer.errors}
            return Response(response, status=HTTPStatus.BAD_REQUEST)

        serializer.save()
        response = {"message": "Done", "category": serializer.data}
        return Response(response, status=HTTPStatus.OK)


urlpatterns = [
    path("", CategoryCreateListAPIView.as_view(), name="category-create-list"),
    path(
        "<int:id>/",
        CategoryDetailsUpdateAPIView.as_view(),
        name="category-details-update",
    ),
]
