import aiomysql
import bcrypt
from uuid import uuid4
from aiohttp import web


class UserModel:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def authenticate_user(self, username, password):
        async with self.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = "SELECT * FROM user WHERE username = %s AND password = %s"

                await cur.execute(query, (username, password))

                result = await cur.fetchone()
        if result:
            session_id = str(uuid4())
            self.sessions[session_id] = username
            return web.json_response({'session_id': session_id, 'name': result[1] + ' ' + result[2], 'profil': result[3]})
        else:
            return None

    async def create_session(self, username):
        session_id = str(uuid4())
        return session_id

    async def delete_session(self, session_id):
        # Supprimer la session de la base de données ou du cache, si nécessaire
        pass


class FeedModel:
    def __init__(self, db_poo):
        self.db_pool = db_poo

    async def get_feed(self):
        async with self.db_pool.get() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                query = "SELECT * FROM feeds INNER JOIN user ON user.id=feeds.user_id"
                await cur.execute(query)
                results = await cur.fetchall()
        feed = []
        for result in results:
            post = {
                'username': result['nom']+' '+result['prenom'],
                'profil': result['profil'],
                'text': result['text'],
                'image': result['image'],
                'likes': result['likes']
            }
            feed.append(post)
        return feed


class PostModel:
    def __init__(self):
        self.posts = []

    async def create_post(self, username, content):
        post = {'username': username, 'content': content}
        self.posts.append(post)
