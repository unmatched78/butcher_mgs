# orders/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from config.permissions import IsShopStaff, IsClient
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.decorators import action


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related("shop", "customer").prefetch_related("lines")

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsClient()]
        if self.action in ("update", "partial_update"):
            return [permissions.IsAuthenticated(), IsShopStaff()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            return self.queryset.filter(customer=user.client_profile)
        return self.queryset.filter(shop=user.shop_profile)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.role == "shop":
            context["shop"] = self.request.user.shop_profile
        return context

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated, IsShopStaff])
    def invoice(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="invoice_{order.id}.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Invoice for Order #{order.id}")
        p.drawString(100, 780, f"Customer: {order.customer.user.get_full_name() or order.customer.user.username}")
        p.drawString(100, 760, f"Total: RWF {order.total}")
        y = 740
        for line in order.lines.all():
            p.drawString(100, y, f"{line.quantity} x {line.item.name} @ RWF {line.unit_price}")
            y -= 20
        p.showPage()
        p.save()
        return response

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated, IsShopStaff])
    def delivery_note(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="delivery_note_{order.id}.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Delivery Note for Order #{order.id}")
        p.drawString(100, 780, f"Customer: {order.customer.user.get_full_name() or order.customer.user.username}")
        y = 760
        for line in order.lines.all():
            p.drawString(100, y, f"{line.quantity} x {line.item.name}")
            y -= 20
        p.showPage()
        p.save()
        return response

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated, IsShopStaff])
    def print(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response({"order": serializer.data, "print_initiated": True})