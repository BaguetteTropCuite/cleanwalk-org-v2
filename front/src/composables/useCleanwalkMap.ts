import { ref, computed } from "vue";
import L, { LatLngBounds, Map } from "leaflet";
import { useCleanwalkStore } from "@/stores/CleanwalkStore";
import type { Cleanwalk } from "@/interfaces/cleanwalkInterface";

export function useCleanwalkMap() {
    const cleanwalkStore = useCleanwalkStore();
    const mapInstance = ref<Map | null>(null);
    const selectedCleanwalk = ref<Cleanwalk | null>(null);
    const searchInput = ref("");

    const filteredCleanwalks = computed(() => {
        if (!searchInput.value) {
            return cleanwalkStore.cleanwalksTab;
        }
        return cleanwalkStore.cleanwalksTab.filter((cleanwalk) =>
            cleanwalk.name.toLowerCase().includes(searchInput.value.toLowerCase()) ||
            cleanwalk.address.toLowerCase().includes(searchInput.value.toLowerCase())
        );
    });

    const setMapEvents = (map: Map) => {
        mapInstance.value = map;
    };

    const setSelectedCleanwalk = (cleanwalkId: number) => {
        const cw = cleanwalkStore.cleanwalksTab.find((cleanwalk) => cleanwalk.id === cleanwalkId);
        if (cw) {
            selectedCleanwalk.value = cw;
        }
    };

    const isPointVisible = (lat: number, lng: number): boolean => {
        if (!mapInstance.value) {
            console.error("Map instance is not available");
            return false;
        }
        const bounds: LatLngBounds = mapInstance.value.getBounds();
        return bounds.contains(L.latLng(lat, lng));
    };

    const mapClick = () => {
        selectedCleanwalk.value = null;
    };


    return {
        mapInstance,
        filteredCleanwalks,
        selectedCleanwalk,
        searchInput,
        setMapEvents,
        setSelectedCleanwalk,
        isPointVisible,
        mapClick,
    };
}
