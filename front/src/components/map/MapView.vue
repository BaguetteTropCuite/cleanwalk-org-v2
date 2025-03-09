<script setup lang="ts">
import { LMap, LTileLayer, LMarker, LIcon } from "@vue-leaflet/vue-leaflet";
import L, { type PointExpression } from "leaflet";
import greenMapIcon from "@/assets/green-map.svg";
import blueMapIcon from "@/assets/blue-map.svg";
import { ref, type Ref } from "vue";
import type { Cleanwalk, SingleCleanwalk } from "@/interfaces/cleanwalkInterface";


const props = defineProps<{
    cleanwalk: SingleCleanwalk;
}>();

const center: Ref<PointExpression> = ref([props.cleanwalk.pos_lat, props.cleanwalk.pos_long]);
const zoom = ref(13);

</script>

<template>
   <div class="map-container">
            <l-map ref="map" v-model:zoom="zoom" v-model:center="center" :min-zoom="5":useGlobalLeaflet="false">
                <l-tile-layer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"></l-tile-layer>
                    <l-marker 
                        :lat-lng="L.latLng(cleanwalk.pos_lat, cleanwalk.pos_long)">
                        <l-icon :icon-size="[25, 41]" :icon-anchor="[12, 41]"
                            :iconUrl="cleanwalk.host?.role_id === 1 ? blueMapIcon : greenMapIcon">
                        </l-icon>
                    </l-marker>
            </l-map>
        </div>
</template>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
}

.map {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}
</style>
