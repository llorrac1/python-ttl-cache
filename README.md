# Python TTL Cache

A simple Python cache which supports item-level expiration.

The cache uses a dictionary to store key-value pairs. Values are stored as a tuple of the value and the expiration time. The expiration time is calculated by adding the TTL to the current time.

This cache can be used in various scenarios where caching is required, such as improving performance in data-intensive applications or reducing API calls. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Background](#background)


## Installation

git-clone this repository and import the cache class into your project.

```python # Path: README.md
from ttl_cache import Cache
```


## Usage

```python # Path: README.md
from cache import ttl_cache

mycache = ttl_cache(maxsize=5, ttl=10)

@mycache
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

if __name__ == '__main__':

    for i in range(10):
        print(fib(i))
    
    print(mycache.get_cache_info())
    print(mycache.clear())
    print(mycache.get_cache_info())

```

## Background 

I created this project to address the need for a simple Python cache that supports item-level expiration. By using a dictionary to store key-value pairs and calculating expiration time based on TTL (Time to Live), this cache provides a convenient way to manage and retrieve cached data efficiently. It can be used in various scenarios where caching is required, such as improving performance in data-intensive applications or reducing API calls. Although you could use inbuilt Python libraries such as [functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache) or [cachetools](https://cachetools.readthedocs.io/en/stable/), these tools do not provide item-level ttl out of the box. As such, this project provides a simple and lightweight alternative. 