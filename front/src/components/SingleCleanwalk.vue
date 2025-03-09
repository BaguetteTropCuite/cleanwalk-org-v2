<script setup lang="ts">
import type { SingleCleanwalk } from '@/interfaces/cleanwalkInterface'
import iconClock from './icons/icon-clock.vue';
import iconMiniMap from './icons/icon-mini-map.vue';
import { onMounted, ref, onUnmounted, computed } from 'vue';
import router from '@/router';
import dateService from '@/services/dateService';
import { useAccountStore } from '@/stores/AccountStore';
import LeaveCwPopup from './popups/LeaveCwPopup.vue';
import ParticipationPopup from './popups/ParticipationPopup.vue';
import MapView from './map/MapView.vue';
import TopBar from './TopBar.vue';
import { useUtilsStore } from '@/stores/UtilsStore';
import { useCleanwalkStore } from '@/stores/CleanwalkStore';

const cleanwalkStore = useCleanwalkStore();
const currenUserId = ref(useAccountStore().CurrentUser?.id);
const token = ref(useAccountStore().getAccessToken());
const showToast = useUtilsStore().showToast;

// Define props with modelValue for two-way binding
const props = defineProps<{ 
  modelValue: SingleCleanwalk 
}>();

// Define emit to update the parent's value
const emit = defineEmits<{
  (e: 'update:modelValue', value: SingleCleanwalk): void
}>();

// Create computed property for two-way binding
const cleanwalk = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const showLeaveCwPopup = ref(false);
const toogleLeaveCwPopup = () => {
  showLeaveCwPopup.value = !showLeaveCwPopup.value;
}

let showParticipationPopup = ref(false);
const toggleParticipationPopup = () => {
  showParticipationPopup.value = !showParticipationPopup.value;
}

const getDate = () => {
  if (cleanwalk.value && cleanwalk.value.date_begin && cleanwalk.value.duration) {
    return dateService.getCleanwalkWrittenDate(new Date(cleanwalk.value.date_begin), cleanwalk.value.duration);
  }
}

const leaveCleanwalk = async () => {
  if (!cleanwalk.value || !currenUserId.value || !token.value) {
    router.push('/login');
    return;
  }
  await cleanwalkStore.leaveCleanwalk(cleanwalk.value.id, token.value, currenUserId.value);
  
  // Update the cleanwalk object through the computed setter
  const updatedCleanwalk = { ...cleanwalk.value };
  updatedCleanwalk.is_user_participant = false;
  cleanwalk.value = updatedCleanwalk;
  
  showToast('Désinscription réussie', true);
  toogleLeaveCwPopup();
}

const handleJoinCleanwalk = async (data: { participantCount: number, isAnonymous: boolean }) => {
  if (!cleanwalk.value || !currenUserId.value || !token.value) {
    router.push('/login');
    return;
  }
  await cleanwalkStore.joinCleanwalk(cleanwalk.value.id, token.value, data.participantCount, currenUserId.value);
  
  // Update the cleanwalk object through the computed setter
  const updatedCleanwalk = { ...cleanwalk.value };
  updatedCleanwalk.is_user_participant = true;
  cleanwalk.value = updatedCleanwalk;
  
  showToast('Inscription réussie', true);
  toggleParticipationPopup();
}

const actionButton = () => {
  if (!cleanwalk.value || !currenUserId.value || !token.value) {
    router.push('/login');
    return;
  }
  if (cleanwalk.value.host.author_id === currenUserId.value) {
    // edit cleanwalk
    router.push(`/cleanwalk/edit/${cleanwalk.value.id}`);
    return;
  }
  if (cleanwalk.value.is_user_participant === true) {
    // leave cleanwalk
    toogleLeaveCwPopup();
    return;
  }
  if (cleanwalk.value.is_user_participant === false) {
    // join cleanwalk
    toggleParticipationPopup();
    return;
  }
}

const getActionButtonText = (): string => {
  if (cleanwalk.value?.host.author_id === currenUserId.value) {
    return "Editer la cleanwalk";
  }
  if (cleanwalk.value?.is_user_participant === true) {
    return "Se désinscrire";
  }
  if (cleanwalk.value?.is_user_participant === false) {
    return "Je participe";
  }
  return "";
}

// Add a function to check if we're on desktop
const isDesktop = ref(false);
// Add a function to check if we're on iOS
const isIOS = ref(false);

// Check screen size and device OS on mount and when window resizes
const checkScreenSize = () => {
  isDesktop.value = window.innerWidth >= 768;
  // Check if device is iOS (iPhone, iPad, iPod)
  isIOS.value = /iPad|iPhone|iPod/.test(navigator.userAgent) && !(window as any).MSStream;
};

onMounted(() => {
  checkScreenSize();
  window.addEventListener('resize', checkScreenSize);
});

// Clean up event listener
onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});
</script>

<template>
  <TopBar backUrl="/" pageName="Cleanwalk" />
  <LeaveCwPopup :isVisible="showLeaveCwPopup" :tooglePopup="toogleLeaveCwPopup" :leaveCw="leaveCleanwalk" />
  <ParticipationPopup :isVisible="showParticipationPopup" @close="toggleParticipationPopup" @confirm="handleJoinCleanwalk" />
  
  <main>
    <div>
      <img v-if="cleanwalk" class="cover" :src="cleanwalk?.img_url" alt="cover image" />
    </div>

    <div class="desktop-layout" v-if="isDesktop && cleanwalk">
      <div class="container">
        <h1>{{ cleanwalk?.name }}</h1>
        <div class="date-location">
          <div class="top">
            <icon-clock />
            <div>{{ getDate() }}</div>
          </div>
          <div class="bot">
            <iconMiniMap />
            <div>{{ cleanwalk?.address }}</div>
          </div>
        </div>
        
        <div class="map-links">
          <!-- Conditionally show Apple Maps or Google Maps depending on device -->
          <a v-if="isIOS" 
             :href="`https://maps.apple.com/?q=${cleanwalk?.address}&ll=${cleanwalk?.pos_lat},${cleanwalk?.pos_long}`"
             target="_blank">
            <img src="../assets/appleMap.svg" alt="Apple Maps logo">
            <h4>Ouvrir dans Plans</h4>
          </a>
          <a v-else 
             :href="`https://www.google.com/maps/?q=${cleanwalk?.pos_lat},${cleanwalk?.pos_long}`"
             target="_blank">
            <img src="../assets/googleMap.svg" alt="Google Maps logo">
            <h4>Ouvrir dans Google Maps</h4>
          </a>
          
          <a :href="`https://www.openstreetmap.org/?mlat=${cleanwalk?.pos_lat}&mlon=${cleanwalk?.pos_long}`"
            target="_blank">
            <img src="../assets/osm_logo.webp" alt="OpenStreetMap logo">
            <h4>Ouvrir dans OpenStreetMap</h4>
          </a>
        </div>
        
        <div v-if="cleanwalk?.host.author_id === currenUserId" class="participant-count">
          {{ cleanwalk?.participant_count }} participant(s)
        </div>
        
        <div class="orga">
          <div class="left">
            <div>organisé par:</div>
            <h2> {{ cleanwalk?.host?.name }} </h2>
          </div>
          <div class="right" v-if="cleanwalk?.host?.profile_picture">
            <img :src="cleanwalk.host.profile_picture" alt="profile-picture">
          </div>
        </div>
        
        <button class="button-primary" @click="actionButton()">
          {{ getActionButtonText() }}
        </button>
        
        <p class="description">
          {{ cleanwalk?.description }}
        </p>
      </div>
      
      <div class="map-section">
        <h3>Localisation</h3>
        <div class="map-container">
          <MapView 
            v-if="cleanwalk?.pos_lat && cleanwalk?.pos_long"
            :cleanwalk = "cleanwalk"
          />
        </div>
      </div>
    </div>

    <!-- Mobile layout -->
    <div class="container" v-if="!isDesktop">
      <h1>{{ cleanwalk?.name }}</h1>
      <div class="date-location">
        <div class="top">
          <icon-clock />
          <div>{{ getDate() }}</div>
        </div>
        <div class="bot">
          <iconMiniMap />
          <div>{{ cleanwalk?.address }}</div>
        </div>
      </div>
      
      <div class="map-links">
        <!-- Conditionally show Apple Maps or Google Maps depending on device -->
        <a v-if="isIOS" 
           :href="`https://maps.apple.com/?q=${cleanwalk?.address}&ll=${cleanwalk?.pos_lat},${cleanwalk?.pos_long}`"
           target="_blank">
          <img src="../assets/appleMap.svg" alt="Apple Maps logo">
          <h4>Ouvrir dans Plans</h4>
        </a>
        <a v-else
           :href="`https://www.google.com/maps/?q=${cleanwalk?.pos_lat},${cleanwalk?.pos_long}`"
           target="_blank">
          <img src="../assets/googleMap.svg" alt="Google Maps logo">
          <h4>Ouvrir dans Google Maps</h4>
        </a>

        <!-- Always show OpenStreetMap -->
        <a :href="`https://www.openstreetmap.org/?mlat=${cleanwalk?.pos_lat}&mlon=${cleanwalk?.pos_long}`"
          target="_blank">
          <img src="../assets/osm_logo.webp" alt="OpenStreetMap logo">
          <h4>Ouvrir dans OpenStreetMap</h4>
        </a>
      </div>
      
      <div v-if="cleanwalk?.host.author_id === currenUserId">
        {{ cleanwalk?.participant_count }} participant(s)
      </div>
      
      <div class="orga">
        <div class="left">
          <div>organisé par:</div>
          <h2> {{ cleanwalk?.host?.name }} </h2>
        </div>
        <div class="right" v-if="cleanwalk?.host?.profile_picture">
          <img :src="cleanwalk.host.profile_picture" alt="profile-picture">
        </div>
      </div>
      
      <button class="button-primary" @click="actionButton()">
        {{ getActionButtonText() }}
      </button>
      
      <p class="description">
        {{ cleanwalk?.description }}
      </p>
    </div>
  </main>
</template>

<style scoped lang="scss">
@use '@/assets/main.scss';

main {
  overflow-y: auto;
}

.cover {
  width: 100vw;
  object-fit: cover;
  aspect-ratio: 21/9;
  margin-top: 58px;

  @media (min-width: 768px) {
    height: 20rem;
    width: 100%;
  }
}

.desktop-layout {
  display: flex;
  width: 90%;
  max-width: 1200px;
  margin: 2rem auto;
  gap: 2rem;

  .container {
    flex: 1;
    padding: 0;
  }

  .map-section {
    flex: 1;
    
    h3 {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 1rem;
      color: var(--text-color-primary);
    }

    .map-container {
      height: 400px;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid #ddd;
    }
  }
}

.container {
  padding: 0 26px;
  font-size: 12px;

  .description {
    width: 100%;
    //le texte ne dois pas depasser et sauter une ligne si besoins
    overflow: hidden;
    word-wrap: break-word;
  }

  h1 {
    color: var(--text-color-primary);
    font-size: 20px;
    font-style: normal;
    font-weight: 700;
    line-height: normal;
    padding: 20px 0 30px;
  }

  .date-location {
    display: flex;
    stroke: var(--text-color-primary);
    flex-direction: column;
    padding-bottom: 20px;
    font-size: 12px;

    .top {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .bot {
      margin-top: 5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
  }

  .map-links {
    display: flex;
    justify-content: space-between;
    border: dashed 2px #0cab2e;
    padding: 10px;
    margin-bottom: 20px;
    border-radius: 8px;

    a {
      display: flex;
      align-items: center;
      gap: 10px;

      img {
        width: 30px;
        height: 30px;
      }

      h4 {
        font-size: 12px;
        font-style: normal;
        font-weight: 500;
        line-height: 18px;
        letter-spacing: 0em;
        text-align: center;
        text-align: left;
        max-width: 6rem;
      }
    }
  }

  .participant-count {
    margin-bottom: 1rem;
    font-weight: 500;
  }

  .orga {
    display: flex;
    background-color: var(--color-secondary);
    justify-content: space-between;
    border-radius: 8px;
    padding: 11px 20px 4px 14px;
    margin-bottom: 20px;

    .left {
      display: flex;
      flex-direction: column;

      h2 {
        font-size: 15px;
        font-style: normal;
        font-weight: 700;
      }
    }

    .right {
      img {
        border-radius: 9999px;
        width: 44px;
        height: 44px;
        object-fit: cover;
      }
    }
  }

  .button-primary {
    padding: 15px 0;
    width: 100%;
    text-align: center;
  }

  p {
    padding-top: 20px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px;
    letter-spacing: 0em;
    text-align: left;
  }

  @media (min-width: 768px) {
    width: 100%;
    margin: 0;
    padding: 0;
  }
}
</style>