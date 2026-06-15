# rate-limiter
Sliding window for request limiting logic and round robin for request load balancing

To run
> `docker run -d -p 6379:6379 --name my-redis redis`
> create virtual env
> pip install fastapi uvicorn redis

> uvicorn main:app --reload --port 8000
> new terminal
> uvicorn main:app --reload --port 8001
> new (3rd) terminal
> docker run -d -p 8080:8080 --name my-load-balancer -v "$(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro" nginx
