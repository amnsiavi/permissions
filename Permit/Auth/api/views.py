from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from Auth.api.serializer import AuthSerializer
from Auth.permissions import IsAdminUser, IsRegularUser


@api_view(['GET','POST'])
@permission_classes([IsAdminUser | IsRegularUser])
def get_user(request):
    
    try:
        if request.method == 'GET':
            if request.user.is_authenticated:
                
                user = User.objects.all()
                serializer = AuthSerializer(user,many=True)

                return Response({
                    'data':serializer.data,
                })
            else:
                return Response({
                    'errors':'User is not authenticated'
                }
                )
        elif request.method == 'POST':
            if len(request.data) == 0:
                return Response({
                    'errors':'Recieved Empty Object'
                })
            if request.user.is_authenticated and request.user.is_superuser:
                serializer = AuthSerializer(data=request.data)
                if serializer.is_valid():
                    username = serializer.validated_data.get('username')
                    email = serializer.validated_data.get('email')
                    password = serializer.validated_data.get('password')
                    is_admin = serializer.validated_data.get('is_superuser')

                    if is_admin:
                        User.objects.create_superuser(
                            username=username, email=email,
                            password=password
                        )
                        return Response({
                            'data':serializer.data,
                            'msg':'Admin Created'
                        })
                    else:
                        User.objects.create_user(
                            username=username, email=email,
                            password=password
                        )
                        return Response({
                            'data':serializer.data,
                            'msg':'Guest user created'
                        })
                else:
                    return Response({
                        'errors':'Bad Request'
                    })
            else:
                return Response({
                    'errors':'User is not authenticated'
                }
                )
        else:
            return Response({
                'errors':'Method Not Allowed'
            })
    
    
    except ValidationError as ve:
        return Response({
            'errors':str(ve)
        })
    except Exception as e:
        return Response({
            'error',str(e)
        })
