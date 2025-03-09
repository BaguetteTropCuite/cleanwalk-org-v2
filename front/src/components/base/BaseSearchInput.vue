<script setup lang="ts">
import IconSearch from '../icons/icon-search.vue';

// Utilisation de defineModel pour permettre la liaison bidirectionnelle avec v-model
const model = defineModel<string>();

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    type: {
        type: String,
        default: 'text',
    },
    placeholder: {
        type: String,
        default: '',
    }
});
</script>

<template>
    <div class="input-wrapper">
        <input
            :type="type"
            :name="name"
            :placeholder="placeholder"
            v-model="model"
            :id="name"
            class="input"
        />
        <IconSearch class="icon-search" />
    </div>
</template>

<style scoped lang="scss">
.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;

    .input {
        width: 100%;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px;
        padding-right: 40px; // Ajout d'un padding pour l'icône
        margin-top: 0.5rem;
        font-size: 14px;
        font-style: normal;
        font-weight: 500;

        &::placeholder {
            color: #94A3B8;
        }

        &:focus {
            outline: none;
        }
    }

    .icon-search {
        position: absolute;
        right: 12px;
        pointer-events: none; // Pour que l'icône ne bloque pas les clics sur l'input
        stroke: #65707F;
        bottom: 12px;
    }
}
</style>
