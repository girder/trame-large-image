import io

import large_image
from aiohttp import web
from large_image.exceptions import TileSourceXYZRangeError
from large_image.tilesource import TileSource
from trame.app import get_server

ROOT_API = "large-image"
TILE_ENDPOINT = "tile/{z}/{x}/{y}.png"
METADATA_ENDPOINT = "metadata"


class TileSourceManager:
    SOURCES = {}
    ROUTES_ADDED = False

    def __init__(self):
        raise NotImplementedError(
            "The TileSourceManager class cannot be instantiated."
        )  # pragma: no cover

    @staticmethod
    def register(source):
        key = TileSourceManager.get_key(source)
        # TODO: should we weakref?
        TileSourceManager.SOURCES[key] = source
        return key

    @staticmethod
    def unregister(source):
        if isinstance(source, TileSource):
            key = TileSourceManager.get_key(source)
        else:
            key = source
        del TileSourceManager.SOURCES[key]  # TODO

    @staticmethod
    def get_key(source):
        if isinstance(source, int):
            return source
        # return hash(source.getLRUHash(source.getState()))
        return hash(id(source))

    @staticmethod
    def get_source(key):
        try:
            return TileSourceManager.SOURCES[key]
        except KeyError as e:
            raise KeyError(f"Source not managed: {str(e)}")

    @staticmethod
    def get_root_url(source):
        key = TileSourceManager.get_key(source)
        return f"/{ROOT_API}/{key}"

    @staticmethod
    def get_tile_url(source):
        return f"{TileSourceManager.get_root_url(source)}/{TILE_ENDPOINT}"

    @staticmethod
    def _get_source(request):
        try:
            key = request.rel_url.query["tileSource"]
        except KeyError as e:
            raise web.HTTPNotFound(text=str(e))

        try:
            key = int(key)
        except ValueError:
            source = large_image.open(key, projection="EPSG:3857", encoding="PNG")
        else:
            try:
                source = TileSourceManager.get_source(key)
            except KeyError as e:
                raise web.HTTPNotFound(text=str(e))
        return source

    @staticmethod
    async def metadata(request):
        """REST endpoint to get image metadata."""
        source = TileSourceManager._get_source(request)
        return web.json_response(source.getMetadata())

    @staticmethod
    async def tile(request):
        """REST endpoint to server tiles from image in ZXY standard."""
        source = TileSourceManager._get_source(request)
        z = int(request.match_info["z"])
        x = int(request.match_info["x"])
        y = int(request.match_info["y"])
        try:
            tile_binary = source.getTile(x=x, y=y, z=z)
        except TileSourceXYZRangeError as e:
            raise web.HTTPNotFound(text=str(e))
        return web.Response(body=io.BytesIO(tile_binary), content_type="image/png")

    @staticmethod
    def routes():
        return [
            web.get(f"/{ROOT_API}/{METADATA_ENDPOINT}", TileSourceManager.metadata),
            web.get(f"/{ROOT_API}/{TILE_ENDPOINT}", TileSourceManager.tile),
        ]


def register(source):
    if isinstance(source, int):
        if source not in TileSourceManager.SOURCES:
            raise KeyError
        key = source
    else:
        key = TileSourceManager.register(source)
    return key


def unregister(source):
    return TileSourceManager.unregister(source)


def get_tile_url(source):
    return TileSourceManager.get_tile_url(register(source))


def add_routes(server=None):
    # TODO: this is not robust enough
    if TileSourceManager.ROUTES_ADDED:
        return
    if server is None or isinstance(server, str):
        server = get_server(server)

    @server.controller.add("on_server_bind")
    def _(wslink_server):
        """Add our custom REST endpoints to the trame server."""
        wslink_server.app.add_routes(TileSourceManager.routes())

    TileSourceManager.ROUTES_ADDED = True
