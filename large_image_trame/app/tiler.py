import io

from aiohttp import web


class Tiler:
    def __init__(self, source):
        self.source = source

    async def metadata(self, request):
        """REST endpoint to get image metadata."""
        return web.json_response(self.source.getMetadata())

    async def tile(self, request):
        """REST endpoint to server tiles from image in slippy maps standard."""
        z = int(request.match_info["z"])
        x = int(request.match_info["x"])
        y = int(request.match_info["y"])
        tile_binary = self.source.getTile(x, y, z)
        return web.Response(body=io.BytesIO(tile_binary), content_type="image/png")

    def routes(self):
        return [
            web.get("/metadata", self.metadata),
            web.get("/tile/{z}/{x}/{y}.png", self.tile),
        ]
