<script setup lang="ts">
import { useCleanwalkMap } from '@/composables/useCleanwalkMap';
import { LMap, LTileLayer, LMarker, LIcon } from "@vue-leaflet/vue-leaflet";
import L, { type PointExpression } from "leaflet";
import { ref, watch, type Ref } from 'vue';
import greenMapIcon from "@/assets/green-map.svg";
import blueMapIcon from "@/assets/blue-map.svg";
import { useCleanwalkStore } from '@/stores/CleanwalkStore';
import BaseSearchInput from './base/BaseSearchInput.vue';
import CleanwalkListCard from './cards/CleanwalkListCard.vue';
import CleanwalkSoloCard from './cards/CleanwalkSoloCard.vue';
import type { Cleanwalk } from '@/interfaces/cleanwalkInterface';

const cleanwalkStore = useCleanwalkStore();

const {
    mapInstance,
    filteredCleanwalks,
    searchInput,
    selectedCleanwalk,
    setMapEvents,
    setSelectedCleanwalk,
    mapClick,
} = useCleanwalkMap();

// Map configuration
let zoom = ref(6);
let center: Ref<PointExpression> = ref([47.2, 0]);

// When filtered results change to exactly one cleanwalk, select it automatically
watch(filteredCleanwalks, (newVal) => {
    if (newVal.length === 1) {
        setSelectedCleanwalk(newVal[0].id!);
    } else if (newVal.length === 0) {
        selectedCleanwalk.value = null;
    }
});

// Handler for when a marker is clicked on the map
const showSoloCW = (id: number) => {
    setSelectedCleanwalk(id);
};

// Reset search and selection
const resetCleanwalkSelection = () => {
    searchInput.value = '';
    selectedCleanwalk.value = null;
    zoom.value = 6;
};

// Focus map on selected cleanwalk's location
const focusOnCleanwalk = (cleanwalk: Cleanwalk) => {
    if (mapInstance.value && cleanwalk) {
        center.value = [cleanwalk.pos_lat, cleanwalk.pos_long];
        zoom.value = 13; // Zoom in closer to the selected cleanwalk
    }
};

const onMapClick = () => {
    if (selectedCleanwalk.value) {
        zoom.value = 6;
    }
    mapClick();
};

// Watch for selected cleanwalk changes to focus the map
watch(selectedCleanwalk, (newVal) => {
    if (newVal) {
        focusOnCleanwalk(newVal);
    }
});
</script>

<template>
    <main>
        <div class="map-container">
            <l-map ref="map" v-model:zoom="zoom" v-model:center="center" @ready="setMapEvents" :min-zoom="5"
                @click="onMapClick()" :useGlobalLeaflet="false">
                <l-tile-layer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"></l-tile-layer>
                <div v-for="cleanwalk in cleanwalkStore.cleanwalksTab" :key="cleanwalk.id">
                    <l-marker @click="showSoloCW(cleanwalk.id!)" 
                        :lat-lng="L.latLng(cleanwalk.pos_lat, cleanwalk.pos_long)">
                        <l-icon :icon-size="[25, 41]" :icon-anchor="[12, 41]"
                            :iconUrl="cleanwalk.host?.role_id === 1 ? blueMapIcon : greenMapIcon">
                        </l-icon>
                    </l-marker>
                </div>
            </l-map>
        </div>

        <div class="cleanwalk-container">
            <BaseSearchInput v-model="searchInput" name="search" placeholder="Rechercher une cleanwalk" />
            <div v-if="filteredCleanwalks.length === 0" class="no-results">
                Aucune cleanwalk trouvée
            </div>
            <div class="container" ref="cleanwalkListContainer">
                <router-link v-for="cleanwalk in filteredCleanwalks"
                    :to="{ name: 'cleanwalk', params: { id: cleanwalk.id } }" 
                    :key="cleanwalk.id" 
                    class="listContainer"
                    @click.prevent="showSoloCW(cleanwalk.id!)">
                    <CleanwalkListCard :cleanwalk="cleanwalk" />
                </router-link>
            </div>
        </div>

        <CleanwalkSoloCard 
            :onClose="resetCleanwalkSelection" 
            :cleanwalk="selectedCleanwalk" 
            v-if="selectedCleanwalk"/>
    </main>
</template>

<style scoped lang="scss">
html,
body,
main {
    margin: 0;
    padding: 0;
    height: 100vh;
    width: 100vw;
}

.map-container {
    height: 100%;
    width: 100%;
    padding-top: 5.5rem;
}

.cleanwalk-container {
    position: fixed;
    bottom: 50%;
    left: 1rem;
    transform: translateY(calc(50% + 2.75rem));
    width: 30rem;
    padding: 1rem 0.9rem 1rem 1rem; // 1rem padding on the left to match the map
    background-color: #F8FAFD;
    box-shadow: 0px -10px 100px rgba(194, 194, 194, 0.2);
    z-index: 999;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: calc(100% - 9rem);
    border-radius: 8px;

    .container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        overflow-y: auto;
        max-height: 100%;
        padding-right: 0.1rem; //move scrollbar to the left
    }
    
    .no-results {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-style: italic;
    }
    
    .listContainer {
        text-decoration: none;
        color: inherit;
    }
}

/* Styliser l'ensemble de la scrollbar */
::-webkit-scrollbar {
    width: 4px; /* Ajustez la largeur à votre préférence */
  }

  /* Styliser le fond de la scrollbar */
  ::-webkit-scrollbar-track {
    background: transparent;
  }

  /* Styliser le bouton de défilement */
  ::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 10px;
  }

  /* Styliser le thumb lors du survol */
  ::-webkit-scrollbar-thumb:hover {
    background: #dfe5ec;
  }
</style>