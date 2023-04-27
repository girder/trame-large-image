from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import leaflet, vuetify

server = get_server()
state, ctrl = server.state, server.controller

state.trame__title = "Leaflet Z-Index"


with SinglePageLayout(server) as layout:
    # Toolbar
    layout.title.set_text(state.trame__title)

    with layout.toolbar:
        layout.toolbar.style = "z-index: 2;"

        vuetify.VSpacer()

        vuetify.VSelect(
            v_model=("table_name", "table 1"),
            items=("table_names", ["table 1", "table 2", "table 3", "table 4"]),
            dense=True,
            hide_details=True,
            style="max-width: 200px;",
        )

    # Main content
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with leaflet.LMap(zoom=3, style="z-index: 0;"):
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

    # Footer
    layout.footer.hide()


if __name__ == "__main__":
    server.start()
