from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


@api_view(['get'])
def frontend_backend_health(request):
    return Response({
        "status":"operational",
        "service": "Pet Spa API",
        "timestamp": datetime.now(),
        "connection": "stablished",
    })
