from django.shortcuts import render

# Create your views here.
# ================================ #
#   Index
# ================================ #
def index(request):
    return render(request,
                  'competitions/index.html')
