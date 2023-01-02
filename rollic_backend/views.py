from django.http import JsonResponse
from .models import User
from .serializers import UserSerializerPatch, UserSerializerPut
from rest_framework.decorators import api_view
from .utils import represents_int
from rest_framework.exceptions import ValidationError


@api_view(["PUT", "GET"])
def put_get(request):
    """
    :param request: GET or PUT request ot /users 
    """    
    message = dict()
    status_code = None
    
    if request.method == "PUT":
        try:
            # for checking the request body is valid or not
            patch_serializer = UserSerializerPut(data=request.data)
            
            if not patch_serializer.is_valid(): 
                message = {"error": "Bad request"}
                status_code = 400
                return JsonResponse(message, status=status_code)
            if User.objects.filter(email=request.data.get("email")).count() > 0:
                message = {"error": "User with that email already exists"}
                status_code = 403
                return JsonResponse(message, status=status_code)
            
            # create and add it to database.
            username: str = request.data.get("name")
            email: str = request.data.get("email")
            password: str = request.data.get("password")

            User.objects.create(name=username, email=email, password=password)
            id_ = User.objects.get(name=username).id

            message = {"id": id_, "name": username, "email": email}
            status_code = 200
        # error handling
        except:
            message = {"error": "server error"}
            status_code = 500
        finally:
            return JsonResponse(message, status=status_code)
    
    elif request.method == "GET":
        try:
            # get operation
            user_objects = User.objects.values()
            message = list()
            for i in range(len(user_objects)):
                temp = {"id": user_objects[i]['id'], 
                        "name": user_objects[i]['name'], 
                        "email": user_objects[i]['email']}
                message.append(temp)
            status_code = 200
            
            if len(user_objects) == 0:
                message = {"error": "User with that id does not exist"}
                status_code = 404

            if len(request.data) > 0:
                message = {"error": "Bad request"}
                status_code = 400
                return JsonResponse(message, status=status_code)
        # error handling
        except:
            message = {"error": "server error"}
            status_code = 500
        finally:
            return JsonResponse(message, status=status_code, safe=False)

@api_view(["PATCH", "DELETE", "GET"])
def hanfle_multi_req(request, user_id):
    """
    :param request:
    :param user_id:
    """    
    message = dict()
    status_code = None
    
    if request.method == "PATCH":
        try:
            # for checking the request body is valid or not
            patch_serializer = UserSerializerPatch(data=request.data)
            if not represents_int(user_id) or not patch_serializer.is_valid():
                message = {"error": "Bad request"}
                status_code = 400                 
                return JsonResponse(message, status=status_code)
            if User.objects.filter(id=user_id).count() == 0:
                message = {"error": "User with that id does not exist"}
                status_code = 404
                return JsonResponse(message, status=status_code)
            # patch operation
            user_obj_name = User.objects.filter(id=user_id).values()[0]['name']
            user_obj_email = User.objects.filter(id=user_id).values()[0]['email']

            user_obj = User.objects.get(name=user_obj_name)
            user_obj.name = request.data.get("name")
            user_obj.password = request.data.get("password")
            user_obj.save()
            message = {"id": user_id, "name":  request.data.get("name"), "email": user_obj_email}
            status_code = 200
        # error handling
        except:
            message = {"error": "server error"}
            status_code = 500
        finally:
            return JsonResponse(message, status=status_code)


    elif request.method == "DELETE":
        try:
            # request checking
            if not represents_int(user_id) or len(request.data) > 0:
                message = {"error": "Bad request"}
                status_code = 400
                return JsonResponse(message, status=status_code)

            elif User.objects.filter(id=user_id).count() == 0:
                message = {"error": "User with that id does not exist"}
                status_code = 404
                return JsonResponse(message, status=status_code)
            #delete operation
            user_obj = User.objects.get(id=user_id)
            user_obj.delete()
            message = {}
            status_code = 200
        # error handling
        except:
            message = {"error": "server error"}
            status_code = 500
        finally:
            return JsonResponse(message, status=status_code)

    elif request.method == "GET":
        try:
            # request checking
            if not represents_int(user_id) or len(request.data) > 0:
                
                message = {"error": "Bad request"}
                status_code = 400
                return JsonResponse(message, status=status_code)

            if User.objects.filter(id=user_id).count() == 0:
                message = {"error": "User with that id does not exist"}
                status_code = 404
                return JsonResponse(message, status=status_code)
            # get operation
            user_name = User.objects.get(id=user_id).name
            user_email = User.objects.get(id=user_id).email
            message = {"id": user_id, "name": user_name, "email": user_email}
            status_code = 200
        # error handling
        except:
            message = {"error": "server error"}
            status_code = 500
        finally:
            return JsonResponse(message, status=status_code)