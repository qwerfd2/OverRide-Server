from starlette.applications import Starlette
from starlette.responses import FileResponse, Response, JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import os
import databases
import sqlalchemy
import json
import secrets
from sqlalchemy import Table, Column, Integer, String, JSON, Boolean, Float, ForeignKey, update, insert
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
import time

from config import HOST, PORT, DEBUG, SSL_CERT, SSL_KEY, REGISTRATION

#------------- DB -------------

DB_NAME = "player.db"
DB_PATH = os.path.join(os.getcwd(), DB_NAME)
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

player = Table(
    "player",
    metadata,
    Column("id", String(64), primary_key=True),
    Column("name", String(64), unique=True, nullable=False),
    Column("banned", Boolean, nullable=False),
    Column("rating", Float, nullable=False),
    Column("data", JSON, nullable=False),
)

rank = Table(
    "rank",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("player_id", String(64), ForeignKey("player.id"), nullable=False),
    Column("key", String(64), nullable=False),
    Column("score", Integer, nullable=False),
    Column("isFC", Boolean, nullable=False),
)

redeem = Table(
    "redeem",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("code", String(64), nullable=False),
    Column("item", JSON, nullable=False),
    Column("expire", Integer, nullable=False),
    Column("limit", Integer, nullable=False),
    Column("roster", JSON, nullable=False),
)

async def init_db():

    if not os.path.exists(DB_PATH):
        print("[DB] Creating new database:", DB_PATH)
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    
    await engine.dispose()
    print("[DB] Database initialized successfully.")

async def get_player_data(user_id):
    query = player.select().where(player.c.id == user_id)
    player_info = await database.fetch_one(query=query)
    if player_info:
        return dict(player_info)
    else:
        return None

async def set_player_data(user_id, data_field, new_data):
    if data_field not in player.c:
        raise ValueError(f"Invalid column name: {data_field}")
    
    query = player.update().where(player.c.id == user_id).values({data_field: new_data})
    await database.execute(query)

# ------------ CDN -------------

root_folder = os.path.dirname(os.path.abspath(__file__))
allowed_folders = ["OverRapid", "Resources", "OverRide"]

async def serve_file(request):
    path = request.path_params['path']
    first_level_folder = path.split('/')[0]
    if first_level_folder in allowed_folders:
        file_path = os.path.realpath(os.path.join(os.getcwd(), path))
        if os.path.isfile(file_path):
            return FileResponse(file_path)

    return Response("File not found", status_code=404)

#------------ API -------------

async def api_function(request: Request):
    data = await request.json()
    content = data.get("Content", "")
    name = data.get("Name", "")
    user_id = data.get("UserId", "")
    player_info = await get_player_data(user_id)
    content_dict = json.loads(content)

    if player_info is None:
        print("WARNING: User not found in database.")

    if name == "dataDownload":
        user_id = content_dict.get("key", "")
        if player_info:
            return JSONResponse(player_info['data'])
        else:
            return JSONResponse({})
        
    elif name == "UIDCheck":
        result = await get_player_data(content_dict.get("key", ""))
        return JSONResponse({"exists": result is not None})
        
    elif name == "dataUpload":
        content_json = content_dict["jsonString"]
        if player_info:
            await set_player_data(user_id, "data", content_json)
        elif REGISTRATION:
            query = insert(player).values(id=user_id, name=content_json["name"], banned=False, rating=0.0, data=content_json)
            await database.execute(query)

        return JSONResponse({"dummy": True})
    
    elif name == "nameCheck":
        player_name = content_dict.get("name", "")
        query = player.select().where(player.c.name == player_name)
        result = await database.fetch_one(query)
        if not REGISTRATION:
            return JSONResponse({"regClosed": True})
        
        return JSONResponse({"exists": result is not None})
        
    elif name == "getName":
        if player_info:
            if player_info['name']:
                if isinstance(player_info['banned'], str) or player_info['banned'] is None:
                    return JSONResponse({"banned": player_info['banned']})
                else:
                    return JSONResponse({"name": player_info['name']})
        
        return JSONResponse({})

    elif name == "ratingUpload":
        try:
            score = float(content_dict.get("score", ""))
        except ValueError:
            return JSONResponse({"dummy": False}, status_code=400)

        if player_info['rating'] is not None:
            await set_player_data(user_id, "rating", score)
            return JSONResponse({"dummy": True})
        else:
            return JSONResponse({"dummy": False}, status_code=400)

    elif name == "rename":
        new_name = content_dict.get("name", "")

        if player_info['banned'] > 0 or player_info['banned'] is None:
            return JSONResponse({"banned": True})
        else:
            await set_player_data(user_id, "name", new_name)
            return JSONResponse({"banned": False})
        
    elif name == "ratingPosition":
        if player_info:
            query = select(sqlalchemy.func.count()).where(player.c.rating > player_info['rating'])
            higher_count = (await database.fetch_one(query))[0]

            query = select(sqlalchemy.func.count())
            total_count = (await database.fetch_one(query))[0]

            response_data = {
                "userExists": True,
                "total": total_count,
                "count": higher_count
            }
        else:
            response_data = {"userExists": False}

        return JSONResponse(response_data)
    
    elif name == "rankUpload":
        key = content_dict.get("key", "")
        score = content_dict.get("score", 0)
        isFC = content_dict.get("isFC", False)
        query = select(rank.c.score).where(rank.c.player_id == user_id, rank.c.key == key)
        result = await database.fetch_one(query)

        if result is not None:
            if result[0] < score:
                query = update(rank).where(rank.c.player_id == user_id, rank.c.key == key).values(score=score, isFC=isFC)
                await database.execute(query)
        else:
            query = insert(rank).values(player_id=user_id, key=key, score=score, isFC=isFC)
            await database.execute(query)

        return JSONResponse({"dummy": True})
    
    elif name == "rankLeaderboard":
        key_to_match = content_dict.get("key", "")
        max_key = content_dict.get("maxKey", 99)

        query = select(rank.c.player_id, rank.c.score, rank.c.isFC).where(rank.c.key == key_to_match)
        qualified_ranks = await database.fetch_all(query)

        qualified_ranks = sorted(qualified_ranks, key=lambda x: x["score"], reverse=True)

        top_scores = qualified_ranks[:max_key]

        result_list = []
        for rank_entry in top_scores:
            player_id = rank_entry["player_id"]
            score = rank_entry["score"]
            isFC = rank_entry["isFC"]

            query = select(player.c.name).where(player.c.id == player_id)
            player_name = (await database.fetch_one(query))["name"]

            result_list.append({"name": player_name, "score": score, "isFC": bool(isFC)})

        return JSONResponse(result_list)
    
    elif name == "ratingLeaderboard":
        query = select(player.c.name, player.c.rating).order_by(player.c.rating.desc())
        result = await database.fetch_all(query)

        leaderboard = [{"name": row["name"], "score": row["rating"]} for row in result]
        return JSONResponse(leaderboard)
    
    elif name == "codeCheck":
        code = content_dict.get("code", "")

        query = select(redeem).where(redeem.c.code == code)
        redeem_info = await database.fetch_one(query)

        if redeem_info:
            item = redeem_info["item"]
            expire = redeem_info["expire"]
            limit = redeem_info["limit"]
            roster = redeem_info["roster"]
            current_time = int(time.time())
            if current_time > expire or len(roster) >= limit or user_id in roster:
                return JSONResponse({"success": False})
            
            roster.append(user_id)
            query = update(redeem).where(redeem.c.code == code).values(roster=roster)
            await database.execute(query)
            return JSONResponse({"success": True, "item": item})
        else:
            return JSONResponse({"success": False})

    elif name == "withdraw":
        return JSONResponse({})

#------------ PVP -------------

queue = []

def find_lobby_by_id(lobby_id):
    for lobby in queue:
        if lobby.get("id") == lobby_id:
            return lobby
    return None

async def pvp_function(request: Request):
    data = await request.json()
    type = data.get("type", "")
    request_code = data.get("request", "")
    lobby_id = data.get("id", "")

    if type == "match":
        if request_code == "list":
            filtered_lobbies = [lobby for lobby in queue if not lobby.get("selected", False)]
            return JSONResponse(filtered_lobbies)

        elif request_code == "create":
            player_id = data.get("pid", "")
            session_id = secrets.token_urlsafe(24)
            lobby_data = {
                "data": {
                    "mp3": data.get("mp3", ""),
                    "diff": data.get("diff", ""),
                    "fm": data.get("fm", False),
                },
                "timestamp": int(time.time()),
                "players": {
                    player_id: {
                        "icon": data.get("icon", ""),
                        "level": data.get("level", 1),
                        "is4Key": data.get("is4Key", False),
                        "diff": data.get("diff", ""),
                        "options": data.get("options", []),
                        "username": data.get("username", ""),
                        "rating": data.get("rating", 0.0),
                        "achivement": data.get("achivement", "")
                    }
                },
                "waiting": True,
                "id": session_id,
                "match": {}
            }
            queue.append(lobby_data)
            return JSONResponse({"id": session_id})

        elif request_code == "purge":
            for index, lobby in enumerate(queue):
                if lobby.get("id") == lobby_id:
                    del queue[index]
                    return JSONResponse(queue)
            return JSONResponse(queue)

        elif request_code == "players":
            lobby = find_lobby_by_id(lobby_id)
            if lobby:
                return JSONResponse(lobby.get("players"))
            return JSONResponse({})

        elif request_code == "join":
            lobby = find_lobby_by_id(lobby_id)
            if lobby:
                player_id = data.get("pid", "")
                lobby["players"][player_id] = {
                    "icon": data.get("icon", ""),
                    "level": data.get("level", 1),
                    "is4Key": data.get("is4Key", False),
                    "diff": data.get("diff", ""),
                    "options": data.get("options", []),
                    "username": data.get("username", ""),
                    "rating": data.get("rating", 0.0),
                    "achivement": data.get("achivement", "")
                }
                lobby["waiting"] = False
                lobby["timestamp"] = int(time.time())
                return JSONResponse(lobby)
            else:
                return JSONResponse({})

        elif request_code == "select":
            lobby = find_lobby_by_id(lobby_id)
            if lobby:
                is_already_selected = lobby.get("selected", False)
                if not is_already_selected:
                    lobby["selected"] = True
                    return JSONResponse({"isAlreadySelected": False})
                else:
                    return JSONResponse({"isAlreadySelected": True})
            else:
                return JSONResponse({"isAlreadySelected": True})

        elif request_code == "unselect":
            lobby = find_lobby_by_id(lobby_id)
            if lobby:
                lobby["selected"] = False
                return JSONResponse({"message": ""})
            else:
                return JSONResponse({"message": ""})

        elif request_code == "match":
            lobby = find_lobby_by_id(lobby_id)
            if lobby:
                player_id = data.get("pid", "")
                match_value = data.get("match", "")
                current_timestamp = int(time.time())
                if player_id in lobby["match"]:
                    lobby["match"][player_id]["timestamp"] = current_timestamp
                    lobby["match"][player_id]["match"] = match_value
                else:
                    lobby["match"][player_id] = {
                        "timestamp": current_timestamp,
                        "match": match_value
                    }
                return JSONResponse(lobby["match"])
            else:
                return JSONResponse({})
            
        else:
            return JSONResponse({})

routes = [
    Route("/Api", api_function, methods=["POST"]),
    Route("/Pvp", pvp_function, methods=["POST"])  
]

routes.append(Route("/{path:path}", serve_file))

app = Starlette(debug=DEBUG, routes=routes)

@app.on_event("startup")
async def startup():
    await database.connect()
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    import uvicorn
    ssl_context = (SSL_CERT, SSL_KEY) if SSL_CERT and SSL_KEY else None
    uvicorn.run(app, host=HOST, port=PORT, ssl_certfile=SSL_CERT, ssl_keyfile=SSL_KEY)

# Made By Tony  2025.5.4