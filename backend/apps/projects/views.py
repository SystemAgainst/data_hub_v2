from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Image
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Projects.
    Full support for List, Create, Retrieve, Update, Delete + image upload.
    """
    queryset = Project.objects.all().prefetch_related('images')
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        """Additional endpoint to upload images to an existing project"""
        project = self.get_object()
        files = request.FILES.getlist('image_files')

        if not files:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        for file in files:
            image = Image.objects.create(image=file)
            project.images.add(image)

        serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
