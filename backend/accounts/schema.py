import graphene
import graphql_jwt.shortcuts
import accounts.schema
from graphene_django import DjangoObjectType
from .models import User
from django.core.cache import cache
import uuid
import os
from dotenv import load_dotenv
from django.core.mail import send_mail
import graphql_jwt

load_dotenv()
FRONTEND_URL = os.environ['FRONTEND_URL']

# Define GraphQL type for User model
class UserType(DjangoObjectType):
    class Meta:
        model = User
        #(no password exposed)
        fields = ('id','email','user_type','phone','address')

#Mutation for checking the usertype
class CheckUserType(graphene.Mutation):
    #Define input arguments for the Mutation
    class Arguments:
        email = graphene.String(required=True)
    
    user_type = graphene.String()
    
    #Define output fields for the Mutation to return to the client
    allow_social_login = graphene.Boolean()
    message = graphene.String()

    def mutate(self,info,email):
        user = User.objects.get(email=email).first()
        if user:
            if user.user_type == 'staff':
                   return CheckUserType(
                       allow_social_login=True,
                       message='Please choose login method: Social or Magic Link',
                    )
               
            return CheckUserType(
                   allow_social_login=False,
                   message='Proceed with Magic Link',
            )
class RequestMagicLinkLogin(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        user_type = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, user_type):
        user = User.objects.filter(email=email).first()
        
        if not user:
            user = User.objects.create(
                email=email,
                username=email,
                user_type=user_type
            )
        
        token = str(uuid.uuid4())
        cache.set(f'magic_link_{token}', email, timeout=300)
        
        send_mail(
            subject='Your Magic Link Login',
            message=f'Click here to login: {FRONTEND_URL}/auth/{token}',
            from_email='noreply@petspa.com',
            recipient_list=[email]
        )
        
        return RequestMagicLinkLogin(
            success=True,
            message='Magic link sent to your email'
        )
class VerifyMagicLinkAndGenerateJWT(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
    
    success = graphene.Boolean()
    jwt_token = graphene.String()
    message = graphene.String()

    def mutate(self, info, token):
        email = cache.get(f'magic_link_{token}')
        
        if not email:
            return VerifyMagicLinkAndGenerateJWT(
                success=False,
                message='Invalid or expired magic link'
            )
        
        user = User.objects.get(email=email)
        jwt_token = graphql_jwt.shortcuts.get_token(user)
        
        return VerifyMagicLinkAndGenerateJWT(
            success=True,
            jwt_token=jwt_token,
            message='JWT token generated successfully'
        )

class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    send_magic_link = RequestMagicLinkLogin.Field()
    check_user_type = CheckUserType.Field()
    verify_magic_link = VerifyMagicLinkAndGenerateJWT.Field()
    
    # JWT mutations (optional but useful)
    verify_token = graphql_jwt.Verify.Field()     # Check if token is valid
    refresh_token = graphql_jwt.Refresh.Field()   # Get new token before expiration
    revoke_token = graphql_jwt.Revoke.Field()     # Logout/invalidate token

#  1. Check type
# mutation {
#   checkUserType(email: "user@example.com") {
#     userType
#     allowSocial
#     message
#   }
# }

#  2. Send link
# mutation {
#   requestMagicLinkLogin(
#     email: "user@example.com"
#     userType: "tutor"
#   ) {
#     success
#     message
#   }
# }

#  3. Verify and get JWT
# mutation {
#   verifyMagicLinkAndGenerateJWT(token: "abc123") {
#     success
#     jwtToken
#     message
#   }
# }
# Verify JWT is still valid
# mutation {
#   verifyToken(token: "your.jwt.token") {
#     payload
#   }
# }

# # Get new token before expiration
# mutation {
#   refreshToken(token: "your.jwt.token") {
#     token
#     payload
#   }
# }