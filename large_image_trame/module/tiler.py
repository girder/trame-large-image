import io

from aiohttp import web
from large_image.exceptions import TileSourceXYZRangeError

ROOT_API = "/large-image"


class Tiler:
    def __init__(self, source):
        self.source = source

    async def metadata(self, request):
        """REST endpoint to get image metadata."""
        return web.json_response(self.source.getMetadata())

    async def tile(self, request):
        """REST endpoint to server tiles from image in ZXY standard."""
        z = int(request.match_info["z"])
        x = int(request.match_info["x"])
        y = int(request.match_info["y"])
        try:
            tile_binary = self.source.getTile(x=x, y=y, z=z)
        except TileSourceXYZRangeError as e:
            raise web.HTTPNotFound(text=str(e))
        return web.Response(body=io.BytesIO(tile_binary), content_type="image/png")

    @property
    def hash(self):
        # Use this hash in the URLs to prevent
        # conflicts across multiple images or caching issues
        return hash(self.source.getLRUHash(self.source.getState()))

    @property
    def tile_url(self):
        return f"{ROOT_API}/{self.hash}/tile/{{z}}/{{x}}/{{y}}.png"

    @property
    def metadata_url(self):
        return f"{ROOT_API}/{self.hash}/metadata"

    @property
    def routes(self):
        return [
            web.get(self.metadata_url, self.metadata),
            web.get(self.tile_url, self.tile),
        ]
