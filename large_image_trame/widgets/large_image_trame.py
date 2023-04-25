import json

from trame.widgets import leaflet
from trame_client.widgets.core import AbstractElement

from .. import module
from ..module.tiler import Tiler


def bounds(source, srs="EPSG:4326"):
    return source.getBounds(srs=srs)


def center(source, srs="EPSG:4326"):
    bnds = bounds(source, srs=srs)
    return (
        (bnds["ymax"] - bnds["ymin"]) / 2 + bnds["ymin"],
        (bnds["xmax"] - bnds["xmin"]) / 2 + bnds["xmin"],
    )


def _post_init_register_routes(instance, routes):
    @instance._server.controller.add("on_server_bind")
    def _(wslink_server):
        """Add our custom REST endpoints to the trame server."""
        wslink_server.app.add_routes(routes)


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


# Expose your vue component(s)
class GeoJSViewer(HtmlElement):
    def __init__(self, tile_source, **kwargs):
        self._tiler = Tiler(tile_source)

        super().__init__(
            "geo-js-viewer",
            tile_url=self._tiler.tile_url,
            metadata=json.dumps(tile_source.getMetadata()).replace('"', "'"),
            **kwargs,
        )
        self._attr_names += [
            ("tile_url", "tileURL"),
            "metadata",
        ]
        # self._event_names += [
        #     "click",
        #     "change",
        # ]

        _post_init_register_routes(self, self._tiler.routes)


class LargeImageLeafletTileLayer(leaflet.LTileLayer):
    def __init__(self, tile_source, **kwargs):
        self._tiler = Tiler(tile_source)

        super().__init__(url=("tile_url", self._tiler.tile_url), **kwargs)

        _post_init_register_routes(self, self._tiler.routes)


class LargeImageLeafletMap(leaflet.LMap):
    def __init__(self, tile_source, **kwargs):
        m = tile_source.getMetadata()
        try:
            zoom = m["levels"] - m["sourceLevels"]
            kwargs.setdefault("center", ("center", center(tile_source)))
        except KeyError:
            zoom = 0
        kwargs.setdefault("zoom", ("zoom", zoom))
        super().__init__(**kwargs)
