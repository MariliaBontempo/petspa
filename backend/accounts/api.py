from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import jwt
import datetime

@api_view(['POST'])
def request_magic_link(request):
    email = request.data.get('email')
    
    # Gera token JWT com expiração de 15 minutos
    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, settings.HASURA_GRAPHQL_JWT_SECRET['key'], algorithm='HS256')
    
    # Envia email com o link mágico
    magic_link = f"http://localhost:3000/auth/verify?token={token}"
    send_mail(
        'Seu link de acesso',
        f'Clique aqui para acessar: {magic_link}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    
    return Response({
        'success': True,
        'message': 'Magic link enviado com sucesso!'
    })