from django.shortcuts import redirect
from django.http import Http404

class ErrorHandlingMiddleWare:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        

        response = self.get_response(request)


        if response.status_code in (400,401,403, 404,500):
            print("an error occured")
            return redirect("error_page")


        return response

        
