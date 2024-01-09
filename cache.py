from datetime import datetime, timedelta
from typing import NamedTuple, Callable, Any
from collections import OrderedDict

class CacheItem(NamedTuple):
    value: Any
    expiry_time: datetime

class CacheInfo(NamedTuple):
    hits: int
    misses: int
    maxsize: int
    currsize: int
    itemttl: int = 0

def ttl_cache(maxsize=128, ttl=600) -> Callable:
    '''
    Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned,
    and not re-evaluated.

    If maxsize is set, the cache will store a maximum of that many items before
    deleting the last item added to the cache.
    
    If ttl is set, the cache will store items for that many seconds before
    deleting the cache item.
    
    If both maxsize and ttl are set, the cache will store items until either
    maxsize items are reached or the ttl is reached, whichever happens first.
    
    If neither maxsize or ttl are set, the cache will use default values of 
    maxsize=128 and ttl=600.
    '''

    cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def decorator(func: Callable):
        return cache(func)

    decorator.clear = cache.clear
    decorator.get_cache_info = cache.get_cache_info
    return decorator

class TTLCache:
    def __init__(self, maxsize=128, ttl=600):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()
        self.cache_info = CacheInfo(hits=0, misses=0, maxsize=maxsize, currsize=0, itemttl=ttl)

    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            now = datetime.now()
            key = (args, frozenset(kwargs.items()))
            if key in self.cache:
                cache_item = self.cache[key]
                if cache_item.expiry_time > now:
                    self.cache_info = self.cache_info._replace(
                        hits=self.cache_info.hits+1, 
                        currsize=len(self.cache)
                        )
                    return cache_item.value
                else:
                    del self.cache[key]
            result = func(*args, **kwargs)
            expiry_time = now + timedelta(seconds=self.ttl)
            cache_item = CacheItem(value=result, expiry_time=expiry_time)
            self.cache[key] = cache_item
            if len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)
            self.cache_info = self.cache_info._replace(
                misses=self.cache_info.misses+1, 
                currsize=len(self.cache)
                )
            return result
        
        wrapper.clear = self.clear
        wrapper.get_cache_info = self.get_cache_info
        return wrapper
    
    def get_cache_info(self):        
        return f"CacheInfo(hits={self.cache_info.hits}, misses={self.cache_info.misses}, maxsize={self.cache_info.maxsize}, currsize={len(self.cache)}, itemttl={self.cache_info.itemttl})"

    def clear(self):
        self.cache.clear()
        self.cache_info = self.cache_info._replace(
            hits=0, 
            misses=0, 
            currsize=0,
            itemttl=self.ttl
            )
        return self.cache_info