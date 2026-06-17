from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import redis
import time

app = FastAPI()

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

with open("rate_limiter.lua", "r") as f:
    lua_script = r.register_script(f.read())

LIMIT = 5
WINDOW_MS = 10000 

@app.middleware("http")
async def rate_limiter_middleware(request: Request, call_next):
    user_ip = request.client.host
    redis_key = f"rate_limit:{user_ip}"
    current_time_ms = int(time.time() * 1000)
    
    allowed = lua_script(keys=[redis_key], args=[current_time_ms, WINDOW_MS, LIMIT])
    
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests. Slow down!"}
        )
        
    response = await call_next(request)
    return response

@app.get("/")
def home():
    return {"message": "Welcome to the protected API!"}