import aiohttp
from Routes.Get_request import CachedRequest
from Models.user_model import User_info
from Models.Repo_model import Repo
import asyncio
class GitManager:

    GITHUB_PAT = "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"
    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}"  # Include the token in the headers
    }

    @classmethod
    async def get_user_profile(cls, username):
        url = f"https://api.github.com/users/{username}"
        result, starred_repo = await asyncio.gather(CachedRequest.get(url), GitManager.get_user_starred_repository(username))
        result['most_starred_repo'] = starred_repo
        user = User_info(**result)
        print(type(user))
        return user

    @classmethod
    async def get_user_repository_global(cls, username):
        url = f"https://api.github.com/users/{username}/repos"
        result = await CachedRequest.get(url)
        return result
    @classmethod
    async def get_user_repository(cls, username):
        result = await GitManager.get_user_repository_global(username)
        repository_names = {}
        i = 1
        for obj in result:
            repository_names[f'{i}'] = obj['name']
            i += 1
        return repository_names

    @classmethod
    async def get_userdefined_repository(cls, user_name, repository_name):
        url = f"https://api.github.com/repos/{user_name}/{repository_name}"
        repo_data = await CachedRequest.get(url)
        contributor_url = repo_data['contributors_url']
        contributor_data = await CachedRequest.get(contributor_url)
        contributor_count = 0
        for temp in contributor_data:
            contributor_count += (temp['contributions'])
        repo_data['contributor_count'] = contributor_count
        repo_data['username'] = user_name
        result = Repo(**repo_data)
        return result


    @classmethod
    async def get_user_sorted_repository(cls, user_name, query_params):
        sorting_type = query_params['type'][0]
        url = f"https://api.github.com/users/{user_name}/repos"
        user_repos = await CachedRequest.get(url)
        final_result = []
        for temp in user_repos:
            user_repo_name = temp['name']
            user_defined_repo_info = await GitManager.get_userdefined_repository(user_name, user_repo_name)
            temp = []
            temp.append(user_defined_repo_info.name)
            temp.append(user_defined_repo_info.forks_count)
            temp.append(user_defined_repo_info.stargazers_count)
            temp.append(user_defined_repo_info.contributor_count)
            final_result.append(temp)

        if sorting_type == 'star':
            final_result = sorted(final_result, key=lambda x: x[2], reverse=True)
        elif sorting_type == 'fork':
            final_result = sorted(final_result, key=lambda x: x[1], reverse=True)
        elif sorting_type == 'recent activity':
            final_result = sorted(final_result, key=lambda x: x[3], reverse=True)
        return {"List": final_result, "Status Code": "200"}

    @classmethod
    async def get_user_starred_repository(cls, name):
        async with aiohttp.ClientSession() as session:
            response = await GitManager.get_user_repository_global(name)
            starred_repository_name = ""
            max_star = 0
            for temp in response:
                current_star_count = temp['stargazers_count']
                if max_star <= current_star_count:
                    starred_repository_name = temp['name']
                    max_star = current_star_count
                return starred_repository_name

    @classmethod
    async def get_user_compare(cls, query_params):
        username1 = query_params['username1'][0]
        username2 = query_params['username2'][0]
        user_response1_result, user_response2_result = await asyncio.gather(GitManager.get_user_profile(username1), GitManager.get_user_profile(username2))
        final_result = {
            'User1': user_response1_result,
            'User2': user_response2_result
        }
        return final_result

    @classmethod
    async def get_repo_compare(cls, body):
        username1 = body['username1']
        username2 = body['username2']
        repo1 = body['repo1']
        repo2 = body['repo2']
        repo_details1_result, repo_details2_result = await asyncio.gather(GitManager.get_userdefined_repository(username1, repo1),
                                                    GitManager.get_userdefined_repository(username2, repo2))
        final_result = {
            'user1': repo_details1_result,
            'user2': repo_details2_result
        }
        return final_result




















