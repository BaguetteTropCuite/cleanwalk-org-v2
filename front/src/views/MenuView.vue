<script setup lang="ts">
import navBar from '@/components/NavBar.vue';
import Menus from '@/components/UserMenu.vue';
import TopBar from '@/components/TopBar.vue';
</script>

<template>
    <TopBar page-name="Menu" />
    <Menus />
    <navBar />
</template>