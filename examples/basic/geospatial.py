import large_image
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import leaflet, vuetify

from trame_large_image.widgets import LargeImageLeafletMap, LargeImageLeafletTileLayer

server = get_server()
state, ctrl = server.state, server.controller

state.trame__title = "Geospatial Large Image Viewer"


source = large_image.open(
    "data/landcover_sample_1000.tif",
    projection="EPSG:3857",
    encoding="PNG",
)


with SinglePageLayout(server) as layout:
    # Toolbar
    layout.title.set_text(state.trame__title)

    # Main content
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with LargeImageLeafletMap(tile_source=source):
                leaflet.LTileLayer(
                    url=(
                        "basemap_url",
                        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    ),
                    attribution=(
                        "attribution",
                        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                    ),
                )
                LargeImageLeafletTileLayer(tile_source=source)

    # Footer
    layout.footer.hide()


if __name__ == "__main__":
    server.start()
