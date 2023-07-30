from sanic import Sanic,response, Blueprint, exceptions
from sanic.response import text, json
from sanic_ext import render, validate
from Managers.Git_Manager import GitManager
from Models.user_model import Check_validate


blueprint_app = Blueprint("GIT")

@blueprint_app.get("/")
async def hello_world(request):
    return text("Hello, world.")

@blueprint_app.get("/users/<username:str>")
async def get_user(request, username):
    obj = GitManager()
    response = await obj.get_user_profile(username)
    return await render("dummy_user_display.html", context={'user': response}, status=400)

@blueprint_app.get('/users/<name:str>/repos')
async def get_user_repos(request, name):
    data = await GitManager.get_user_repository(name)
    data['username'] = name
    return await render("dummy_user_repos.html", context={'repository_names': data}, status=400)

@blueprint_app.get('/users/<user_name:str>/<repository_name:str>')
async def get_userdefined_repo(request, user_name, repository_name):
    response = await GitManager.get_userdefined_repository(user_name, repository_name)
    return await render("dummy_userdefined_repo.html", context={'data': response}, status=400)


@blueprint_app.get('/users/<name:str>/sort_repo')
@validate(query=Check_validate)
async def get_user_sortedrepos(request, name, query=Check_validate):
        query_params = request.args
        response = await GitManager.get_user_sorted_repository(name, query_params)
        return await render("dummy_sort_repo.html", context={'data': response}, status=400)


@blueprint_app.get('/users/user_compare')
async def get_compare(request):
    query_params = request.args
    response = await GitManager.get_user_compare(query_params)
    user_response1 = response['User1']
    user_response2 = response['User2']
    return await render("dummy_user_compare.html",
                        context={'content1': user_response1, 'content2': user_response2}, status=400)

@blueprint_app.post('/users/repo_compare')
async def get_compare_repo(request):
    body = request.json
    response = await GitManager.get_repo_compare(body)
    repo_details1 = response['user1']
    repo_details2 = response['user2']
    return await render("dummy_repo_compare.html",
                        context={'content1': repo_details1, 'content2': repo_details2},
                        status=400)




@blueprint_app.exception(exceptions.InvalidUsage)
async def handle_invalid_usage(request, exception):
    return response.json({"error": "Invalid input type for query parameter 'type'."}, status=400)