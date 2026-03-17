web: bench serve --port 8003
redis_cache: redis-server config/redis_cache.conf
redis_queue: redis-server config/redis_queue.conf
redis_socketio: redis-server config/redis_socketio.conf
socketio: /usr/bin/node apps/frappe/socketio.js
watch: bench watch
schedule: bench schedule
worker_short: bench worker --queue short
worker_long: bench worker --queue long
worker_default: bench worker --queue default
