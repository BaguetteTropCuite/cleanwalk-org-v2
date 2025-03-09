<script setup lang="ts">
import type { Association } from '@/interfaces/userInterface';
import defaultBanner from '../assets/default-banner.svg';

// Accept association as prop instead of fetching it
const props = defineProps<{
    asso: Association
}>();

</script>
<template>
    <div class="container">
        <img :src="props.asso.banner_img ? props.asso.banner_img : defaultBanner" alt="banner asso" class="banner">
        <img :src="props.asso.profile_picture" alt="logo asso" class="pp">
    </div>
    <div class="text-container">
        <h1>{{ props.asso.name }}</h1>
        <p>{{ props.asso.description }}</p>
    </div>
</template>
<style scoped lang="scss">
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    .banner {
        width: 100%;
        height: 150px;
        aspect-ratio: 21;
        object-fit: cover;
        margin-top: 58px;
    }
    .pp {
        position: relative;
        width: 96px;
        margin-top: -60px;
        object-fit: cover;
        height: 96px;
        border-radius: 9999px;
        background-color: #ffc107;
    }
}
.text-container {
    padding: 0 2rem;
}
</style>