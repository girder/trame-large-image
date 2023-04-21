<script lang="ts">
import GeoJSViewer from '@/components/GeoJSViewer/index.vue';

export default {
  name: 'HomePage',
  components: {
    GeoJSViewer,
  },
  data() {
    // This test assumes a tile server with this item is available and running
    return {
      tileURL: 'http://localhost:3333/tile/{z}/{x}/{y}.png',
      metadata: {
        levels: 8,
        sizeX: 20000,
        sizeY: 12000,
        tileWidth: 256,
        tileHeight: 256,
      },
    };
  },
};
</script>

<template>
  <div id="app">
    <v-app>
      <GeoJSViewer :tileURL="tileURL" :metadata="JSON.stringify(metadata)" />
    </v-app>
  </div>
</template>
