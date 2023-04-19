import axios from 'axios';
import geo from 'geojs';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    apiRoot: {
      type: String,
      required: true,
    },
    itemID: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const view = ref(null);
    const itemTileMetadata = ref();
    const tileUrl = `${props.apiRoot}/item/${props.itemID}/tiles/zxy/{z}/{x}/{y}`;
    const axiosInstance = axios.create({
      baseURL: props.apiRoot,
    });

    async function getTileMetadata() {
      const resp = await axiosInstance.get('item/' + props.itemID + '/tiles');
      if (resp.status === 200) {
        itemTileMetadata.value = resp.data;
      }
    }

    function createViewer() {
      if (!itemTileMetadata.value) return;
      const { map, layer } = geo.util.pixelCoordinateParams(
        view.value,
        itemTileMetadata.value.sizeX,
        itemTileMetadata.value.sizeY,
        itemTileMetadata.value.tileWidth,
        itemTileMetadata.value.tileHeight
      );
      const layerParams = {
        ...layer,
        url: tileUrl,
      };
      view.value = geo.map({
        node: view.value,
        ...map,
      });
      view.value.createLayer('osm', layerParams);
    }

    return {
      view,
      getTileMetadata,
      createViewer,
    };
  },
  mounted() {
    this.getTileMetadata().then(this.createViewer);
  },
});
