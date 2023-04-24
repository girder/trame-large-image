from trame.widgets import leaflet
from trame_client.widgets.core import AbstractElement

from .tiler import Tiler
from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


# Expose your vue component(s)
class GeoJSViewer(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "geo-js-viewer",
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


class LargeImageLTileLayer(leaflet.LTileLayer):
    def __init__(self, tile_source, **kwargs):
        super().__init__(**kwargs)
        self.tiler = Tiler(tile_source)

        @self._server.controller.add("on_server_bind")
        def app_available(wslink_server):
            """Add our custom REST endpoints to the trame server."""
            wslink_server.app.add_routes(self.tiler.routes())
