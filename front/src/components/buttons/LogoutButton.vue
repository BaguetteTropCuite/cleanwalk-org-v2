<script setup lang="ts">
import { ref } from 'vue';
import iconLogout from '@/components/icons/icon-logout.vue';
import iconRightArrow from '@/components/icons/icon-right-arrow.vue';
import LogoutPopup from '../popups/LogoutPopup.vue';


// Define props
const props = defineProps({
  username: {
    type: String,
    required: false,
    default: ''
  }
});

const isPopupVisible = ref(false);

const togglePopup = () => {
  isPopupVisible.value = !isPopupVisible.value;
};
</script>

<template>
  <div class="logout-button-container">
    <LogoutPopup :is-visible="isPopupVisible" :toggle-popup="togglePopup" />
    
    <button @click="togglePopup()" class="logout">
      <iconLogout />
      <h3>Se Déconnecter</h3>
      <iconRightArrow class="arrow"/>
    </button>
  </div>
</template>

<style scoped lang="scss">
.logout-button-container {
  width: 100%;
  
  .logout {
    stroke: #FF5757;
    background-color: transparent;
    border: 1px solid #CBD5E1;
    color: #FF5757;
    width: 100%;
    display: flex;
    align-items: center;
    padding: 1rem;
    border-radius: 8px;
    margin-top: 50px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    
    &:hover {
      background-color: rgba(255, 87, 87, 0.05);
    }

    h3 {
      margin: 0 1rem;
      flex-grow: 1;
      font-size: 16px;
      font-weight: 700;
    }

    .arrow {
      stroke: #94A3B8;
    }
  }

  @media (min-width: 768px) {
    max-width: 40rem;
  }
}
</style>