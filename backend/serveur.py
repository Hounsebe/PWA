import aiomysql
from aiohttp import web
import aiohttp_cors
from Model import UserModel, FeedModel, PostModel
from Controller import UserController, FeedController, PostController


class FacebookServer:
    def __init__(self):
        self.app = web.Application()
        self.sessions = {}
        self.db_pool = None

    async def initialize_db_pool(self):
        self.db_pool = await aiomysql.create_pool(host='localhost', port=3306,
                                                  user='userDb', password='m4xCapacity',
                                                  db='facedb')

    async def initialize(self) -> web.Application:
        await self.initialize_db_pool()
        self.app.router.add_get('/', self.home)

        user_model = UserModel(self.db_pool)
        feed_model = FeedModel(self.db_pool)
        post_model = PostModel()

        user_controller = UserController(user_model)
        feed_controller = FeedController(feed_model)
        post_controller = PostController(post_model)

        self.app.router.add_post('/login', user_controller.login)
        self.app.router.add_post('/logout', user_controller.logout)
        self.app.router.add_get('/feed', feed_controller.get_feed)
        self.app.router.add_post('/post', post_controller.create_post)

        cors = aiohttp_cors.setup(self.app, defaults={
            "http://127.0.0.1:5500": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        for route in list(self.app.router.routes()):
            cors.add(route)
        return self.app

    async def home(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'session_id' not in data:
            return web.HTTPBadRequest()

        session_id = data['session_id']
        if session_id not in self.sessions:
            return web.HTTPUnauthorized()

        username = self.sessions[session_id]
        return web.json_response({'message': f'Welcome, {username}!'})

    def run(self):
        web.run_app(self.initialize(), host='127.0.0.1', port=8000)
