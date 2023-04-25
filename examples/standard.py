import large_image
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

from trame_large_image.widgets import trame_large_image

server = get_server()
state, ctrl = server.state, server.controller

state.trame__title = "Standard Large Image Viewer"


source = large_image.open("examples/multi_all.yml")


with SinglePageLayout(server) as layout:
    layout.title.set_text(state.trame__title)

    # Main content
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            trame_large_image.GeoJSViewer(
                tile_source=source,
            )

    # Footer
    layout.footer.hide()


if __name__ == "__main__":
    server.start()
