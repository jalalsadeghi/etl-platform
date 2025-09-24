# backend/app/tasks/broker.py
import os

from taskiq import TaskiqMiddleware
from taskiq_redis.redis_broker import RedisStreamBroker

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
broker = RedisStreamBroker(REDIS_URL)

# (optional) simple middleware placeholder
broker.add_middlewares(TaskiqMiddleware())
