import io

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server_thread import ServerThread
from starlette.responses import StreamingResponse

from large_image.tilesource import TileSource


def get_server(
    src: TileSource,
    port: int = 3333,
    debug: bool = False,
    start: bool = True,
    host: str = "127.0.0.1",
):
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/metadata")
    async def get_metadata():
        return src.getMetadata()

    @app.get("/tile/{z}/{x}/{y}.png")
    async def get_tile(z: int, x: int, y: int):
        tile_binary = src.getTile(x, y, z)
        return StreamingResponse(io.BytesIO(tile_binary), media_type="image/png")

    server = ServerThread(app, port=port, debug=debug, start=start, host=host)

    return server


def bounds(src, srs="EPSG:4326"):
    return src.getBounds(srs=srs)


def center(src, srs="EPSG:4326"):
    extent = bounds(src, srs=srs)
    return (
        (extent["ymax"] - extent["ymin"]) / 2 + extent["ymin"],
        (extent["xmax"] - extent["xmin"]) / 2 + extent["xmin"],
    )
