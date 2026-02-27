from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Note
from .serializers import NoteSerializer
from utils.response import success_response, error_response
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwner



class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('q')
        sort = self.request.query_params.get('sort')
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')

        queryset =  Note.objects.filter(
            user=user,
            is_deleted=False
        ).only('id', 'title', 'content', 'created_at')
        # 🔍 Search
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        # 📅 Date filter
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        # 🔃 Sorting
        if sort == 'new':
            queryset = queryset.order_by('-created_at')
        elif sort == 'old':
            queryset = queryset.order_by('created_at')

        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(
                success_response(serializer.data, "Notes fetched")
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(success_response(serializer.data))
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(success_response(serializer.data, "Note created"))

        return Response(
            error_response(serializer.errors, "Validation failed"), 
            status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # soft delete
        instance.is_deleted = True
        instance.save()

        return Response(success_response(message="Note deleted"))
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, "Note updated"))

        return Response(
            error_response(serializer.errors, "Validation failed"),
            status=status.HTTP_400_BAD_REQUEST
        )