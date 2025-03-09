<script setup lang="ts">
import { ref } from 'vue';
import DeleteAccountPopup from '../popups/DeleteAccountPopup.vue';

const isPopupVisible = ref(false);

const togglePopup = () => {
  isPopupVisible.value = !isPopupVisible.value;
};
</script>

<template>
  <div class="delete-account-button-container">
    <DeleteAccountPopup :is-visible="isPopupVisible" :toggle-popup="togglePopup" />
    
    <button @click="togglePopup()" class="delete-account">
      Clôturer son compte
    </button>
  </div>
</template>

<style scoped lang="scss">
.delete-account-button-container {
  width: 100%;
  text-align: right;
  margin-top: 20px;
  
  .delete-account {
    background-color: transparent;
    border: none;
    padding: 0;
    color: #FF5757;
    font-size: 12px;
    font-weight: 400;
    text-decoration: underline;
    cursor: pointer;
    opacity: 0.8;
    
    &:hover {
      opacity: 1;
    }
  }
}
</style>