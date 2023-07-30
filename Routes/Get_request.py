from sanic import Sanic,response, Blueprint, text
from sanic import Sanic,response, Blueprint
from sanic.response import text, json
from sanic.request import Request
import sys
from sanic_ext import render
import time
import asyncio
from sanic import exceptions
import aiohttp
from sanic.exceptions import NotFound, BadRequest
from aiohttp_client_cache import CachedSession, SQLiteBackend

class Request:

    @classmethod
    async def get(cls, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 400:
                    raise BadRequest()
                elif response.status == 404:
                    raise NotFound()
                result = await response.json()
                return result

class CachedRequest(Request):
    @classmethod
    async def get(cls, url):
        async with CachedSession(cache=SQLiteBackend('demo_cache', expire_after=60 * 60)) as session:
            async with session.get(url) as response:
                print(f'Is response coming from cache<user_info.py): {response.from_cache}')
                if response.status == 400:
                    raise BadRequest()
                elif response.status == 404:
                    raise NotFound()
                result = await response.json()
                return result