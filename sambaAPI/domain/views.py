from django.shortcuts import render

from rest_framework import viewsets
from .models import Domain
from .serializers import DomainSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class DomainViewSet(viewsets.ModelViewSet):
	#permission_classes = [IsAuthenticated,]
	queryset = Domain.objects.all().order_by('domain_name')
	serializer_class = DomainSerializer

	@action(detail=False)
	def domainname_list(self, request):
		data = []
		queryset = Domain.objects.all().order_by('domain_name')
		for query in queryset:
			data.append(query.domain_name)
		return Response(data,status=status.HTTP_201_CREATED)
