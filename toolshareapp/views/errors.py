from django.shortcuts import render

def error404(request):
        return render(request,'toolshareapp/error/404.html')