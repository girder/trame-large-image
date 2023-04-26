import json

from large_image.tilesource import TileSource
from trame.widgets import leaflet
from trame_client.widgets.core import AbstractElement

from .. import module
from ..module.manager import add_routes, register


def bounds(source, srs="EPSG:4326"):
    return source.getBounds(srs=srs)


def center(source, srs="EPSG:4326"):
    bnds = bounds(source, srs=srs)
    return (
        (bnds["ymax"] - bnds["ymin"]) / 2 + bnds["ymin"],
        (bnds["xmax"] - bnds["xmin"]) / 2 + bnds["xmin"],
    )


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)
            add_routes(self.server)


class GeoJSViewer(HtmlElement):
    def __init__(self, tile_source, **kwargs):
        if isinstance(tile_source, TileSource):
            tile_source = register(tile_source)
        super().__init__(
            "geo-js-viewer",
            tile_source=tile_source,
            # TODO: support metadata with reference key
            metadata=json.dumps(tile_source.getMetadata()).replace('"', "'"),
            **kwargs,
        )
        self._attr_names += [
            ("tile_source", "tileSource"),
            "metadata",
        ]


class LargeImageLTileLayer(HtmlElement):
    def __init__(self, tile_source, **kwargs):
        if isinstance(tile_source, TileSource):
            tile_source = register(tile_source)
        super().__init__(
            "large-image-l-tile-layer",
            tile_source=tile_source,
            **kwargs,
        )
        self._attr_names += [
            ("tile_source", "tileSource"),
        ]


class LargeImageLMap(leaflet.LMap):
    def __init__(self, tile_source, **kwargs):
        m = tile_source.getMetadata()
        try:
            zoom = m["levels"] - m["sourceLevels"]
            kwargs.setdefault("center", ("center", center(tile_source)))
        except KeyError:
            zoom = 0
        kwargs.setdefault("zoom", ("zoom", zoom))
        super().__init__(**kwargs)
