
from django.urls import path

from .views import ProductCreateList, ProductRetrieveUpdateDelete

urlpatterns = [
    path('', ProductCreateList.as_view()),
    path('<int:product_id>/', ProductRetrieveUpdateDelete.as_view()),
]
