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
      apiRoot: 'http://localhost:8080/api/v1',
      itemID: '641c68e18076e407876e8c38',
    };
  },
};
</script>

<template>
  <div id="app">
    <v-app>
      <GeoJSViewer :apiRoot="apiRoot" :itemID="itemID" />
    </v-app>
  </div>
</template>
