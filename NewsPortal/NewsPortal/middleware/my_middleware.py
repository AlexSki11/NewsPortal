
class Check_model(): 
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        response = self.get_response(request)
        #print(request.mobile, "yes")
        return response
    
    def __process_view__(request, view_func, view_args, view_kwargs):
        print(request, 'yes2')
