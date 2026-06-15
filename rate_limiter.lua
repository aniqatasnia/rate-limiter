-- keys/args passed from FastAPI
local key = KEYS[1]          -- user IP or API key (example "rate_limit:192.168.1.1")
local now = tonumber(ARGV[1]) -- current timestamp for request in milliseconds
local window = tonumber(ARGV[2]) -- window size in milliseconds (millisecond window for max requests)
local limit = tonumber(ARGV[3])  -- max allowed requests

local clear_before = now - window

-- SLIDING WINDOW ALGORITHM:
-- removing timestamps older than current window
redis.call('ZREMRANGEBYSCORE', key, 0, clear_before)

-- count requests left
local current_requests = redis.call('ZCARD', key)

-- verify user request limit status
if current_requests < limit then
    -- adding current request timestamp to sorted set
    -- now => score / value
    redis.call('ZADD', key, now, now)
    return 1 -- request allowed
else
    return 0 -- request denied
end