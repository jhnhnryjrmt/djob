from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import JobForm
from .models import Job, Category
from .serializers import JobSerializer, JobDetailSerializer, CategorySerializer

# Create your views here.

class CategoriesView(APIView):
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)

        return Response(serializer.data)

class NewestJobsView(APIView):
    def get(self, request, format=None):
        job = Job.objects.all()[0:4]
        serializer = JobSerializer(job, many=True)

        return Response(serializer.data)
    
class MyJobsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        job = Job.objects.filter(created_by=request.user)
        serializer = JobSerializer(job, many=True)

        return Response(serializer.data)

class CreateJobView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        form = JobForm(request.data)

        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()

            return Response({'status': 'created'})
        else:
            return Response({'status': 'errors', 'errors': form.errors})
        
    def put(self, request, pk):
        job = Job.objects.get(pk=pk, created_by=request.user)
        form = JobForm(request.data, instance=job)
        form.save()

        return Response({'status': 'updated'})
    
    def delete(self, request, pk):
        job = Job.objects.get(pk=pk, created_by=request.user)
        job.delete()

        return Response({'status':'deleted'})

class BrowseJobsView(APIView):
    def get(self, request, format=None):
        job = Job.objects.all()

        categories = request.GET.get('categories', '')
        query = request.GET.get('query', '')

        if query:
            job = job.filter(title__icontains=query)

        if categories:
            job = job.filter(category_id__in=categories.split(','))

        serializer = JobSerializer(job, many=True)

        return Response(serializer.data)
    
class JobDetailView(APIView):
    def get(self, request, pk, format=None):
        job = Job.objects.get(pk=pk)
        serializer = JobDetailSerializer(job)

        return Response(serializer.data)