from django.urls import path

from . import views

app_name = "construction"

urlpatterns = [
    path("constructions/", views.ConstructionListView.as_view(), name="construction-list"),
    path("constructions/new/", views.ConstructionCreateView.as_view(), name="construction-create"),
    path("constructions/<int:pk>/", views.ConstructionDetailView.as_view(), name="construction-detail"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/new/", views.OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path(
        "orders/<int:order_id>/contract/new/",
        views.ContractForWorkCreateView.as_view(),
        name="contract-create",
    ),
]
