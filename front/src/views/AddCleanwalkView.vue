<script setup lang="ts">
import navBar from '@/components/NavBar.vue';
import TopBar from '@/components/TopBar.vue';
import DesktopAddCleanwalk from '@/components/addCleanwalk/DesktopAddCleanwalk.vue';
import MobileAddCleanwalk from '@/components/addCleanwalk/MobileAddCleanwalk.vue';
import { useDevice } from '@/composables/useDevice';

const { isMobile } = useDevice();

</script>

<template>
    <TopBar v-if="isMobile" back-url="/add" page-name="Ajouter une cleanwalk" />
    <MobileAddCleanwalk v-if="isMobile" />
    <DesktopAddCleanwalk v-if="!isMobile" />
    <navBar />
</template>