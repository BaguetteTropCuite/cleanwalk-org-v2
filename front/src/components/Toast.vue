<script setup lang="ts">
import { ref } from 'vue';
import { useUtilsStore } from '@/stores/UtilsStore';

const toast = useUtilsStore().toast;


</script>

<template>
    <div class="toast" :class="{ 'toast-success': toast.isSuccess, 'toast-error': !toast.isSuccess, 'is-visible': toast.isVisible }">
        <p>{{ toast.message }}</p>
    </div>
</template>

<style scoped lang="scss">
.toast {
    opacity: 0;
    position: fixed;
    transform: translateY(-100%);
    top: 0;
    right: 0;
    padding: 5px 20px;
    border-radius: 0 0 0 8px;
    color: #fff;
    font-weight: bold;
    z-index: 9999;
    transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out; // Réduisez la durée et ajoutez opacity
    pointer-events: none;

    &.is-visible {
        transform: translateY(0);
        opacity: 1;
    }

    &.toast-success {
        background-color: #3ee243;
    }

    &.toast-error {
        background-color: #f44336;
    }
}
</style>
