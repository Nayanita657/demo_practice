import requests
from sanic import Sanic,response
from Routes.main import blueprint_app


app = Sanic("GIT_Project")
app.blueprint(blueprint_app)

async def check_Github_Api(app, loop):
    Github_url = "https://api.github.com"
    response = requests.get(Github_url)
    if response.status_code == 200:
        print("GitHub API is reachable. Starting the server...")
    else:
        print("GitHub API is down. Server will not start.")
        app.stop()
@app.listener("before_server_start")
async def before_server_start(app, loop):
    await check_Github_Api(app, loop)

@app.on_request()
async def client_checking_middleware(request):
    client = request.headers['user-agent']
    if 'postman' not in client.lower():
        return response.json({"error": "Access denied. Only Postman allowed."}, status=403)


if __name__ == '__main__':
    app.run()