import TileLayerMixin from 'vue2-leaflet/src/mixins/TileLayer.js';
import Options from 'vue2-leaflet/src/mixins/Options.js';
import { optionsMerger, propsBinder, findRealParent } from 'vue2-leaflet/src/utils/utils.js';
import { tileLayer, DomEvent } from 'leaflet';

import 'leaflet/dist/leaflet.css';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LargeImageLTileLayer',
  mixins: [TileLayerMixin, Options],
  props: {
    tileSource: {
      type: String,
      required: true,
    },
    tileLayerClass: {
      type: Function,
      default: tileLayer,
    },
  },
  setup(props) {
    function createLayer() {
      const url = `/large-image/${props.tileSource}/tile/{z}/{x}/{y}.png`;

      // TODO: limit request bounds of the tileLayer
      const options = optionsMerger(this.tileLayerOptions, this);
      this.mapObject = this.tileLayerClass(url, options);
      DomEvent.on(this.mapObject, this.$listeners);
      propsBinder(this, this.mapObject, this.$options.props);
      this.parentContainer = findRealParent(this.$parent);
      this.parentContainer.addLayer(this, !this.visible);
      this.$nextTick(() => {
        /**
         * Triggers when the component is ready
         * @type {object}
         * @property {object} mapObject - reference to leaflet map object
         */
        this.$emit('ready', this.mapObject);
      });

    }

    return {
      createLayer,
    };
  },
  mounted() {
    this.createLayer();
  },
});
