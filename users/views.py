from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
from .helpers import *


# view courses that a student has registerd for.
@require_http_methods(['GET'])
def view_student_courses(request, username):
    """
    This function should return all the courses that a user of type student
    has registerd for,
    Recieved data: The logged-in username as a url parameter
    Return data: list of all the courses data
    """
    if request.method == 'GET':
        
        # check if the user logged in
        if request.session['username'] != username:
            return JsonResponse({'error': 'something went wrong, user supposed to be logged in'}, status=401)
        
        # query the user's registered in courses
        user = User.objects.get(username=username)
        courses = courseQuerySetSerializer(user.enrolled_courses.all())
        if courses is None:
            return JsonResponse({'error': 'No courses to view'}, status=404)
        
        return JsonResponse({'success': True, 'courses': courses}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# limiting request method to this view for just the post method
@require_http_methods(['POST'])
def login_user(request):
    """
    This veiw function should check if user exiting into the database via
    authenticate() metod, if not None, login in the user
    Return: 
        json = success:True, user:user_data
    """
    # access the data send from the frontend
    if request.method == 'POST':

        # access the json object of user's cridentials sent from frontend
        username = request.POST['username']
        password = request.POST['password']

        # check upon the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # log in the user
            login(request, user)

            # return the user object
            user = user_serializer(user)
            success = {'success': True}

            return JsonResponse({ **success , **user }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credinitals'}, status=401)   # unauthorized

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@require_http_methods(['POST'])
def register_as_instructor(request):
    """
    This veiw function should take form from frontend and validate each input
    and make new instractor user with the data

    if data was valid Return: 
        json = success:True
    if data not valid Return:
        json = success:True , errors = errors

    """

    if request.method == "POST":
        # access the data send in the form
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        ssn = request.POST['ssn']
        university_id = request.POST['universityid']

        # make array of error in eorm
        error = []
        #check if first  naem valid
        if first_name.isalpha() == False:
            error.append({"first name" : "First name is not valid"})
        #check if first  naem valid
        if last_name.isalpha() == False:
            error.append({"first name" : "Last name is not valid"})
        # check if user exist 
        if username_exists(user_name):
            error.append({"user name" : "User name already exist"})
        # check if email is valid 
        if validate_email(email) == False:
            error.append({"email" : "It's not valid email"})
        # check if ssn is less than 20 number
        if len(ssn) > 14 or len(ssn) < 14:
            error.append({"SSN" : "SSN is must be 14"})
        # check if ssn is less than 20 number
        if len(university_id) > 10 and len(university_id) < 5:
            error.append({"SSN" : "University_id is greater than 10"})

        # if fount error return array of error 
        if len(error) != 0:
            return JsonResponse({'errors': error}, status=400)

        # if not found error save data in database and rtuev success message

        # add data to User object 
        user = User.objects.create_user(user_name, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True

        # add information to the user 
        info = UserInfo(user = user, ssn = ssn, university_id = university_id)
        # commit change 
        user.save()
        info.save()

        # now login the user
        login(request, user)

        user = user_serializer(user)
        success = {'success': True}

        # return success message 
        return JsonResponse({ **user, **success }, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@require_http_methods(['POST'])
def register_as_student(request):
    """
    This veiw function should take form from frontend and validate each input
    and make new student user with the data

    if data was valid Return: 
        json = success:True
    if data not valid Return:
        json = success:True , errors = errors

    """

    if request.method == "POST":
        # access the data send in the form
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        ssn = request.POST['ssn']
        university_id = request.POST['universityid']
        level = request.POST['level']

        # make array of error in eorm
        error = []
        #check if first  naem valid
        if first_name.isalpha() == False:
            error.append({"first name" : "First name is not valid"})
        #check if first  naem valid
        if last_name.isalpha() == False:
            error.append({"last name" : "Last name is not valid"})
        # check if user exist 
        if username_exists(user_name):
            error.append({"user name" : "User name already exist"})
        # check if email is valid 
        if validate_email(email) == False:
            error.append({"email" : "It's not valid email"})
        # check if ssn is less than 20 number
        if len(ssn) > 14 or len(ssn) < 14:
            error.append({"SSN" : "SSN must be 14"})
        # check if ssn is less than 20 number
        if len(university_id) > 10 and len(university_id) < 5:
            error.append({"universityid" : "University id is greater than 10"})
        #check level is correct pr not
        try:
            int(level)
            if int(level) > 7:
                error.append({"levellen" : "level must be less than 7"})
        except:
            error.append({"levelint" : "level must be integer"})

        # if found error in errors array return array of error 
        if len(error) != 0:
            return JsonResponse({'errors': error}, status=400)

        # add data to User object 
        user = User.objects.create_user(user_name, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = False

        # add information to the user 
        info = UserInfo(user = user, ssn = ssn, university_id = university_id, level = level)
        # commit change 
        user.save()
        info.save()

        # now login the user
        login(request, user)

        user = user_serializer(user)
        success = {'success': True}

        # return success message 
        return JsonResponse({ **user, **success }, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# other views