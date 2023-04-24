import geo from 'geojs';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    tileURL: {
      type: String,
      required: true,
    },
    metadata: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const view = ref(null);
    const metadata = JSON.parse(props.metadata.replaceAll("'", '"'));

    function createViewer() {
      const { map, layer } = geo.util.pixelCoordinateParams(
        view.value,
        metadata.sizeX,
        metadata.sizeY,
        metadata.tileWidth,
        metadata.tileHeight
      );
      const layerParams = {
        ...layer,
        url: props.tileURL,
      };
      view.value = geo.map({
        node: view.value,
        ...map,
      });
      view.value.createLayer('osm', layerParams);
    }

    return {
      view,
      createViewer,
    };
  },
  mounted() {
    this.createViewer();
  },
});
