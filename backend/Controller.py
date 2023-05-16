import json
from aiohttp import web
from Model import UserModel, FeedModel, PostModel


class UserController:
    def __init__(self, user_model):
        self.user_model = user_model

    async def login(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'username' not in data or 'password' not in data:
            return web.HTTPBadRequest()

        username = data['username']
        password = data['password']
        user = await self.user_model.authenticate_user(username, password)
        print(user)
        if user:
            session_id = await self.user_model.create_session(username)
            print(session_id)
            return web.json_response({'session_id': session_id, 'name': user['name'], 'profil': user['profil']})
        else:
            return web.HTTPUnauthorized()

    async def logout(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'session_id' not in data:
            return web.HTTPBadRequest()

        session_id = data['session_id']
        await self.user_model.delete_session(session_id)

        return web.json_response({'message': 'Logged out successfully'})

    async def render_login_form(self, request: web.Request) -> web.Response:
        # Logique de rendu du formulaire de connexion
        pass


class FeedController:
    def __init__(self, feed_model):
        self.feed_model = feed_model

    async def get_feed(self, request: web.Request) -> web.Response:
        data = request.query
        if 'session_id' not in data:
            return web.HTTPBadRequest()

        feed = await self.feed_model.get_feed()

        return web.json_response({'feed': feed})

    async def render_feed(self, request: web.Request) -> web.Response:
        # Logique de rendu de la page d'alimentation (feed)
        pass


class PostController:
    def __init__(self, post_model):
        self.post_model = post_model

    async def create_post(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'session_id' not in data or 'content' not in data:
            return web.HTTPBadRequest()

        session_id = data['session_id']
        username = ''  # Récupérer le nom d'utilisateur correspondant à la session
        content = data['content']
        await self.post_model.create_post(username, content)

        return web.json_response({'message': 'Post created successfully'})

    async def render_create_post_form(self, request: web.Request) -> web.Response:
        # Logique de rendu du formulaire de création de post
        pass
