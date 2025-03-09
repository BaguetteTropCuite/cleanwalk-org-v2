<script setup lang="ts">
import MobileHome from '@/components/MobileHome.vue';
import DesktopHome from '@/components/DesktopHome.vue';
import navBar from '@/components/NavBar.vue';
import { useCleanwalkStore } from '@/stores/CleanwalkStore';
import { onMounted } from 'vue';
import { useDevice } from '@/composables/useDevice';


const store = useCleanwalkStore();

const { isMobile } = useDevice();
onMounted( async () => {
  await store.getAllCleanwalks();
});
</script>

<template>
    <MobileHome v-if="isMobile" />
    <DesktopHome v-if="!isMobile" />
    <navBar />
</template>
