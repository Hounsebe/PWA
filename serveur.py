import aiomysql
import json
import bcrypt
from uuid import uuid4
from aiohttp import web
import aiohttp_cors

class FacebookServer:
    def __init__(self):
        self.app = web.Application()
        self.sessions = {}
        self.users = {}
        self.posts = []

    async def initialize(self) -> web.Application:
        self.app.router.add_get('/', self.home)
        self.app.router.add_post('/login', self.login)
        self.app.router.add_post('/logout', self.logout)
        self.app.router.add_get('/feed', self.feed)
        self.app.router.add_post('/post', self.create_post)
        self.db_pool = await aiomysql.create_pool(host='localhost', port=3306,
                                                  user='userDb', password='m4xCapacity',
                                                  db='facedb')

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

    async def login(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'username' not in data or 'password' not in data:
            return web.HTTPBadRequest()

        username = data['username']
        password = data['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed_password)
        async with self.db_pool.acquire() as conn:
               async with conn.cursor() as cur:
                      query = "SELECT * FROM user WHERE username = %s AND password = %s"
                      await cur.execute(query, (username, password))
                      result = await cur.fetchone()
        if result:
            session_id = str(uuid4())
            self.sessions[session_id] = username
            return web.json_response({'session_id': session_id})
        else:
            return web.HTTPUnauthorized()

    async def logout(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'session_id' not in data:
            return web.HTTPBadRequest()

        session_id = data['session_id']
        if session_id in self.sessions:
            del self.sessions[session_id]

        return web.json_response({'message': 'Logged out successfully'})

    async def home(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'session_id' not in data:
            return web.HTTPBadRequest()

        session_id = data['session_id']
        if session_id not in self.sessions:
            return web.HTTPUnauthorized()

        username = self.sessions[session_id]
        return web.json_response({'message': f'Welcome, {username}!'})

    async def feed(self, request: web.Request) -> web.Response:
        data = request.query
        if 'session_id' not in data:
            return web.HTTPBadRequest()

        session_id = data['session_id']
        if session_id not in self.sessions:
            return web.HTTPUnauthorized()

        async with self.db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                query = "SELECT * FROM feeds  inner join user on user.id=feeds.user_id"
                await cur.execute(query)
                results = await cur.fetchall()
        feed = []
        for result in results:
            post = {
                'username': result['nom']+' '+result['prenom'],
                'profil':result['profil'],
                'text': result['text'],
                'image': result['image'],
                'likes': result['likes']
            }
            feed.append(post)

        return web.json_response({'feed': feed})

        # Retrieve and return the feed (e.g., posts from friends)

    async def create_post(self, request: web.Request) -> web.Response:
        data = await request.json()
        if 'session_id' not in data or 'content' not in data:
            return web.HTTPBadRequest()

        session_id = data['session_id']
        if session_id not in self.sessions:
            return web.HTTPUnauthorized()

        username = self.sessions[session_id]
        content = data['content']
        post = {'username': username, 'content': content}
        self.posts.append(post)

        return web.json_response({'message': 'Post created successfully'})
    
    

    def run(self):
        web.run_app(self.initialize(),host='127.0.0.1', port=8000)
        
if __name__ == '__main__':
    server = FacebookServer()
    server.run()