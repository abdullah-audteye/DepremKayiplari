from django.shortcuts import redirect






class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        return None

    def __call__(self, request):
        try:
            path = request.META.get('PATH_INFO', "")
            # print(path,'pathhh')
            # lang_check = (request.path.split('/')[1])

            # print(lang_check,'langcheckk')


            # if len(lang_check) == 0:
            #     lang_check = "tr"

 

            # if lang_check == "tr" or lang_check == "en":
            #     return redirect('ihbarview_tr')



        except Exception as err:
            print(err, 'errcheck')

        response = self.get_response(request)

        return response


class RedirectSubDomain:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """

        return None

    def __call__(self, request):
        try:
            pass


        except Exception as err:
            print(err, 'errcheck')

        response = self.get_response(request)

        return response