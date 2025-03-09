<script setup lang="ts">
import iconCross from '../icons/icon-cross.vue';
import { useAccountStore } from '@/stores/AccountStore';

const lougout = useAccountStore().logout;

defineProps({
    isVisible: Boolean,
    togglePopup: Function,
});


</script>

<template>
    <div v-if="isVisible" class="popup" @click="togglePopup!">
        <div class="popup-content" @click.stop>
            <div class="cross"><iconCross @click="togglePopup!" /></div>
            <h2>Se déconnecter</h2>
            <p>Etes vous certain de vouloir vous déconnecter ?</p>
            <div class="btn-container">
                <button @click="togglePopup!" class="cancel-button">annuler</button>
                <button @click="lougout()" class="danger-button">confirmer</button>
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
        position: relative;
        z-index: 1001;

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