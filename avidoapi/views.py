from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from avidoapp.models import User


# Create your views here.


@api_view(['POST'])
def block_user(request, id):
    user = get_object_or_404(User, id=id)
    user.is_block = True
    date_time_obj = datetime.strptime(request.data['time_unblock'], '%Y-%m-%d %H:%M')
    user.time_unblock = date_time_obj
    user.save()
    return Response({'data': {'code': 200, 'message': 'Пользователь заблокирван!'}}, status=HTTP_200_OK)
