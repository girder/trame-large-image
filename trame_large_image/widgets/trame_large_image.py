import json

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


# Expose your vue component(s)
class GeoJSViewer(HtmlElement):
    def __init__(self, tile_source, **kwargs):
        super().__init__(
            "geo-js-viewer",
            tile_source_key=register(tile_source),
            metadata=json.dumps(tile_source.getMetadata()).replace('"', "'"),
            **kwargs,
        )
        self._attr_names += [
            ("tile_source_key", "tileSourceKey"),
            "metadata",
        ]


class LargeImageLeafletTileLayer(leaflet.LTileLayer):
    def __init__(self, tile_source, **kwargs):
        tile_source_key = register(tile_source)
        self._state_key = f"_LILTileLayer_{hash(id(self))}"
        _fvar = "{" + f"{self._state_key}" + "}"
        url = f"`/large-image/${_fvar}/tile/{{z}}/{{x}}/{{y}}.png`"
        super().__init__(
            url=(url,),
            **kwargs,
        )
        self.server.state[self._state_key] = tile_source_key
        add_routes(self.server)


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
