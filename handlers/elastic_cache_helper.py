import time
import uuid
import sys
import socket
import elasticache_auto_discovery
from pymemcache.client.hash import HashClient
import config

class simple_cache(dict): 
    def __init__(self): 
        self = dict() 

    def set(self, key, value): 
        self[key] = value.encode('utf-8')

    def get(self, key):
        v = super().get(key, b'')
        return v

memcache_client = None

def get_elastic_cache_client():
    return simple_cache()
    global memcache_client
    if memcache_client:
        return memcache_client

    elasticache_config_endpoint = config.config["elastic_cache_url"] + ":11211"
    nodes = elasticache_auto_discovery.discover(elasticache_config_endpoint)
    nodes = map(lambda x: (x[1], int(x[2])), nodes)
    memcache_client = HashClient(nodes)
    return memcache_client