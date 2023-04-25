r"""
Define your classes and create the instances that you need to expose
"""
import logging
import large_image
import json

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import leaflet, vuetify
from large_image_trame.widgets import large_image_trame as my_widgets


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class Engine:
    def __init__(self, server=None):
        if server is None:
            server = get_server()

        self._server = server

        # initialize state + controller
        state = server.state
        # ctrl =  server.controller

        # Set state variable
        state.trame__title = "Large Image Trame"

        self.image = large_image.open("large_image_trame/data/multi_all.yml")
        # self.image = large_image.open(
        #     "/data/rasters/TC_NG_SFBay_US_Geo.tif",
        #     projection="EPSG:3857",
        #     encoding="PNG",
        # )

        # props cannot be sent as dict and cannot contain double-quotes
        state.metadata = json.dumps(self.image.getMetadata()).replace('"', "'")

        # Bind instance methods to controller
        # ctrl.reset_resolution = self.reset_resolution
        # ctrl.on_server_reload = self.ui
        # ctrl.widget_click = self.widget_click
        # ctrl.widget_change = self.widget_change

        # Bind instance methods to state change
        # state.change("resolution")(self.on_resolution_change)

        # Generate UI
        self.ui()

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def show_in_jupyter(self, **kwargs):
        from trame.app import jupyter

        logger.setLevel(logging.WARNING)
        jupyter.show(self._server, **kwargs)

    def ui(self, *args, **kwargs):
        with SinglePageLayout(self._server) as layout:
            # Toolbar
            layout.title.set_text("Trame")

            # Main content
            with layout.content:
                with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                    my_widgets.GeoJSViewer(
                        tile_source=self.image,
                    )

                    # with my_widgets.LargeImageLeafletMap(tile_source=self.image):
                    #     leaflet.LTileLayer(
                    #         url=(
                    #             "basemap_url",
                    #             "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    #         ),
                    #         attribution=(
                    #             "attribution",
                    #             '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                    #         ),
                    #     )
                    #     my_widgets.LargeImageLeafletTileLayer(self.image)

            # Footer
            layout.footer.hide()
