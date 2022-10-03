from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from library.serializers import BookSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, permissions
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm

def home(request):
    return render(request, 'home.html')

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })  

@api_view(['GET','POST'])
def book_list(request, format=None):
    if request.method=='GET':
        books=Book.objects.all()
        serializer=BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method=='POST':
        BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','POST','DELETE'])
def book_details(request, id, format=None):
    try:
        book=Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=BookSerializer(book)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def signin(request):
    if request.user.is_authenticated==False:
        if(request.method=="POST"):
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, ('There was error.'))
                return redirect('login')

        else:
            return render(request,'login.html')
    else:
        return redirect('/')

def signout(request):
    logout(request)
    return redirect('/')
    
def addbook(request):
    if request.user.is_authenticated:
        fm=BookForm(request.POST)
        if fm.is_valid():
            form=fm.save(commit=False)
            form.save()
            messages.success(request, ('Added'))
            return redirect('/')
        else:
            return render(request, 'addbook.html', {'fm':fm})

    return render(request, 'addbook.html')

def getbook(request):
    book=Book.objects.all()
    return render(request, 'getbook.html', {'book':book})
    
@login_required
def edit(request, pk):
    book=Book.objects.get(id=pk)
    if request.user.is_authenticated:
        fm=BookForm(instance=book)
        if request.method=='POST':
            fm=BookForm(request.POST, instance=book)
            if fm.is_valid():
                form=fm.save(commit=False)
                fm.save()
                return redirect('/')

        return render(request, 'edit.html', {'fm':fm})
    else:
        return redirect('/')

@login_required
def delete(request, pk):
    book=Book.objects.get(id=pk)
    if request.user.is_authenticated:
        book.delete()
        return redirect('getbook')
    else:
        return redirect('/')

