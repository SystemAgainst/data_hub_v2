from rest_framework import serializers
from .models import Project, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ProjectSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    # For uploading new images while creating/updating a project
    image_files = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True,
        help_text="Upload one or more images"
    )

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'address', 'documents_storage', 'expenses_sheet',
            'description', 'images', 'image_files', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'images']

    def create(self, validated_data):
        image_files = validated_data.pop('image_files', [])
        project = Project.objects.create(**validated_data)

        for image_file in image_files:
            image = Image.objects.create(image=image_file)
            project.images.add(image)

        return project

    def update(self, instance, validated_data):
        image_files = validated_data.pop('image_files', [])

        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Add new images if any
        for image_file in image_files:
            image = Image.objects.create(image=image_file)
            instance.images.add(image)

        return instance
