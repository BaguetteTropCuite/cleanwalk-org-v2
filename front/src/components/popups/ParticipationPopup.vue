<script setup lang="ts">
import iconCross from '../icons/icon-cross.vue';
import iconAdd from '../icons/icon-add.vue';
import iconMinus from '../icons/icon-minus.vue';
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  isVisible: boolean
}>();

const emit = defineEmits(['close', 'confirm']);

const counterParticipate = ref(1);
const isAnonyme = ref(false);
const popupRef = ref<HTMLElement | null>(null);

const counterAdd = () => {
  if (counterParticipate.value < 5) {
    counterParticipate.value++;
  }
}

const counterMinus = () => {
  if (counterParticipate.value > 1) {
    counterParticipate.value--;
  }
}

const cancel = () => {
  emit('close');
  resetForm();
}

const confirm = () => {
  emit('confirm', {
    participantCount: counterParticipate.value,
    isAnonymous: isAnonyme.value
  });
  resetForm();
}

const resetForm = () => {
  counterParticipate.value = 1;
  isAnonyme.value = false;
}

// Handle clicks outside the popup
const handleOutsideClick = (event: MouseEvent) => {
  // Check if popup is visible and click is outside popup-validation
  if (props.isVisible && popupRef.value && !popupRef.value.contains(event.target as Node)) {
    emit('close');
    resetForm();
  }
}

// Set up and clean up click event listeners
onMounted(() => {
  document.addEventListener('mousedown', handleOutsideClick);
});

onUnmounted(() => {
  document.removeEventListener('mousedown', handleOutsideClick);
});
</script>

<template>
  <div class="popup" v-if="isVisible">
    <div class="popup-validation" ref="popupRef">
      <div class="cross-container">
        <button class="cross" @click="cancel()">
          <iconCross />
        </button>
      </div>
      <h3>Validation de la participation au ramassage</h3>
      <div class="warning">Maximum 5 personnes avec vous</div>
      <div class="counter">
        <button class="button-primary minus" @click="counterMinus()">
          <iconMinus />
        </button>
        <div>{{ counterParticipate }}</div>
        <button class="button-primary add" @click="counterAdd()">
          <iconAdd />
        </button>
      </div>
      <div class="anonyme">
        <input type="checkbox" name="anonyme" id="anonyme" v-model="isAnonyme">
        <label for="anonyme">participer en anonyme</label>
      </div>
      <div class="button-container">
        <button @click="cancel()" class="cancel">Annuler</button>
        <button @click="confirm()" class="button-primary">Valider</button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100dvh;
  z-index: 999;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;

  .popup-validation {
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
    width: 90%;
    padding: 0 10%;

    @media (min-width: 768px) {
      width: 30rem;
      padding: 0 3rem;
    }

    .cross-container {
      display: flex;
      justify-content: flex-end;
      position: relative;
      margin-right: -10%; // to compensate padding :( sorry

      .cross {
        background-color: transparent;
        stroke: var(--text-color-primary);
        padding: 13px 13px 0 0;
      }
    }

    .warning {
      padding: 40px 0 10px;
      font-size: 12px;
    }

    h3 {
      font-size: 18px;
      font-weight: 700;
      text-align: center;
      max-width: 230px;
      margin: 0 auto;
    }


    .counter {
      display: flex;
      width: 100%;
      justify-content: space-between;

      button {
        width: 50px;
        height: 50px;
        stroke: #fff;
        padding-top: 4px;

        &.add {
          padding-top: 4px;

          svg {
            width: 32px;
            height: 32px;
          }
        }
      }

      div {
        font-size: 25px;
        font-style: normal;
        font-weight: 700;
        line-height: 47px;
        background-color: var(--color-secondary);
        margin: 0 20px;
        border-radius: 8px;
        flex-grow: 1;
        text-align: center;
      }
    }

    .anonyme {
      display: flex;
      padding-top: 20px;
      visibility: hidden; //provisoire
      padding: 0;

      input[type="checkbox"] {
        margin-right: 5px
      }

      label {
        display: block;
        font-size: 12px;
        padding-top: 2px;
      }
    }

    .button-container {
      display: flex;
      padding: 20px 0;

      button {
        font-weight: 500;
        padding: 15px 0;
        border-radius: 8px;

        &.cancel {
          flex-grow: 0.25;
          margin-right: 10px;
          font-size: 16px;
        }

        &.button-primary {
          flex-grow: 0.75;
        }
      }
    }
  }
}
</style>