<script setup lang="ts">
import { ref } from 'vue'
import iconCross from '../icons/icon-cross.vue';

// Define props
const props = defineProps<{
  isVisible: boolean,
  tooglePopup: () => void,
  leaveCw: () => void
}>();

</script>

<template>
    <div v-if="isVisible" class="popup">
        <div class="popup-content">
            <div class="cross"><iconCross @click="tooglePopup!" /></div>
            <h2>Se désinscrire</h2>
            <p>Etes vous certain de vouloir vous désinscrire de la clenawalk</p>
            <div class="btn-container">
                <button @click="tooglePopup!" class="cancel-button">annuler</button>
                <button @click="leaveCw!" class="danger-button">confirmer</button>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;

    
    .popup-content {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        padding: 1rem;
        margin: 1.5rem;

        .cross {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 1rem;
            stroke: var(--text-color-primary);
        }

        h2 {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
            padding-bottom: 1rem;
        }

        p {
            font-size: 12px;
            font-style: normal;
            font-weight: 400;
            padding: 0 1rem;
            margin-bottom: 3rem;
        }


    }
    .btn-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
    }
}
</style>