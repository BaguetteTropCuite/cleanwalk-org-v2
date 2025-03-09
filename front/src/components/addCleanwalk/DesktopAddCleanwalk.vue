<script setup lang="ts">
import { ref, type Ref } from 'vue';
import { useCleanwalkForm } from '@/composables/useAddCleanwalk'; // Import the composable
import AutocompleteAddress from '@/components/base/AutocompleteAddress.vue';
import dragDrop from '@/components/dragDrop.vue';
import BaseInput from '@/components/base/BaseInput.vue';
import router from '@/router';
import { useUtilsStore } from '@/stores/UtilsStore';
import BaseTextarea from '@/components/base/BaseTextarea.vue';
import dateService from '@/services/dateService';
import IconClock from '@/components/icons/icon-clock.vue';
import IconMiniMap from '@/components/icons/icon-mini-map.vue';


const titles = ref([
  'Nom et lieu de l\'évènement',
  'Date et horaire',
  'Description de votre évènement ',
  'Ajouter une image',
  'Aperçu de votre cleanwalk'
]);


const showToast = useUtilsStore().showToast;
// Import the composable
const {
  dragDropRef,
  newCleanwalk,
  dateCleanwalk,
  handleSelectAddress,
  setDate,
  upload,
} = useCleanwalkForm(); // Destructure the composable to access the data and methods

const progress = ref(1);

// Advice messages for the user
const conseils = ref([
  'Choisissez un titre court pour votre ramassage, qui permettra de donner une idée globale de votre événement pour intéresser les potentiels participants. Ne vous perdez pas dans les détails (heure, matériel, etc.) que vous pourrez inscrire dans la suite de ce formulaire. Si une activité est associée à votre ramassage (running, randonnée, …), vous pouvez l’indiquer dans le titre pour que cela soit mis en avant.',
  'Choisissez ici la date, la durée de votre ramassage (activités annexes comprises - goûter, pique-nique, …)',
  'Utilisez cet espace pour donner toute information complémentaire aux potentiels participants : matériel à apporter, parcours prévu, état des lieux, précisions sur le point de rendez-vous, etc.',
  'Vous avez la possibilité d’ajouter une image ou un visuel pour illustrer votre événement. Si vous ne choisissez pas d’image, une image par défaut sera appliquée automatiquement.',
]);

const getConseil = () => {
  return conseils.value[progress.value - 1];
};

// Handling next and previous buttons
const next = () => {
  if (progress.value === 1 && (!newCleanwalk.value.name || !newCleanwalk.value.address)) {
    showToast('Please enter a name and address for your event', false);
    return;
  }
  if (progress.value === 2) {
    setDate();
    if (!newCleanwalk.value.date_begin || !newCleanwalk.value.duration || newCleanwalk.value.duration < 0) {
      showToast('Please enter a valid start and end time', false);
      return;
    }
  }
  if (progress.value === 3 && !newCleanwalk.value.description) {
    showToast('Please enter a description for your event', false);
    return;
  }
  if (progress.value === 5) {
    upload();
    return;
  }

  progress.value += 1;
};

const back = () => {
  if (progress.value === 1) {
    router.push('/add');
    return;
  }
  progress.value -= 1;
};

</script>

<template>
  <section class="section">
    <div class="container">
      <h1>Organiser un ramassage</h1>
      <h2>{{ titles[progress - 1] }}</h2>
      <div class="form">
        <div v-if="progress === 1">
          <BaseInput v-model="newCleanwalk.name" name="text" type="text" label="nom de la cleanwalk"
            placeholder="Saisissez le nom de votre événement" />
          <AutocompleteAddress v-model:query="newCleanwalk.address" label="adresse" @select-suggestion="handleSelectAddress" />
        </div>
        <div v-if="progress === 2">
          <BaseInput v-if="progress === 2" v-model="dateCleanwalk.dateDay" name="date" type="date"
            label="Date de l'évènement" />
          <BaseInput v-if="progress === 2" v-model="dateCleanwalk.hourBegin" name="hourBegin" type="time"
            label="Heure de début" />
          <BaseInput v-if="progress === 2" v-model="dateCleanwalk.hourEnd" name="hourEnd" type="time"
            label="Heure de fin" />
        </div>
        <BaseTextarea v-if="progress === 3" v-model="newCleanwalk.description" name="description" id="description"
          label="Description" :rows="4" />
        <dragDrop ref="dragDropRef" v-if="progress >= 4" :auto-upload="false" format="card" />
        <div v-if="progress === 5" class="preview">
          <h3>{{ newCleanwalk.name }}</h3>
          <div class="date-locate">
            <div class="divtop">
              <IconClock />
              <div>
                {{ dateService.getCleanwalkWrittenDate(new Date(newCleanwalk.date_begin), newCleanwalk.duration) }}
              </div>
            </div>
            <div class="bot">
              <IconMiniMap />
              <div>{{ newCleanwalk.address }}</div>
            </div>
          </div>
          <p>{{ newCleanwalk.description }}</p>
        </div>


      </div>
      <div v-if="progress<=4" class="help">
        <h3>Aide</h3>
        <p>{{ getConseil() }}</p>
      </div>
      <div class="btn-container">
        <button class="btn back" @click="back()" v-if="progress !== 1">{{ progress === 5 ? 'Modifier' : 'Précédent' }}</button>
        <div class="btn" v-else></div>
        <button class="btn next btn" @click="next()">{{ progress === 5 ? 'Publier' : 'Suivant' }}</button>
      </div>
    </div>

    <div class="progress">
      <h3>Progression</h3>
      <ul class="progression-bar">
        <li :class="{ active: progress === 1 }">Informations générales</li>
        <li :class="{ active: progress === 2 }">Dates et horaires</li>
        <li :class="{ active: progress === 3 }">Description</li>
        <li :class="{ active: progress === 4 }">Photo et visuel</li>
        <li :class="{ active: progress === 5 }">Aperçu</li>
      </ul>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.btn-container {
  display: flex;
  justify-content: space-between;
  gap: 2.5rem;
  flex-grow: 1;
  width: 40rem;
  margin-top: 1.5rem;

  .btn {
    flex: 1;
    padding: 1.25rem;
    font-weight: 700;
    font-size: 1.125rem;
    border-radius: 8px;

    &.back {
      border: solid 1px #65707F;
      background-color: #F8FAFD;
    }

    &.next {
      background-color: var(--color-primary);
      color: #fff;
    }
  }
}

.section {
  padding-top: 14vh;
  display: flex;
  justify-content: space-evenly;
}

.container {
  width: clamp(20rem, 80%, 40rem);

  h1 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1vh;
    width: 100%;
    text-align: center;
  }

  h2 {
    font-size: 1.5rem;
    font-weight: 700;
    width: 100%;
    text-align: left;
  }

  .form {
    display: flex;
    flex-direction: column;
    background-color: #F8FAFD;
    border-radius: 8px;
    border: 1px solid #CBD5E1;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .help {
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    background-color: #E1F4F8;
    padding: 1.5rem;

    h3 {
      font-weight: 700;
    }

  }

}

.progress {
  padding-top: 3.9rem;

  h3 {
    width: 100%;
    text-align: left;
    font-weight: 700;
    padding-bottom: 0.5rem;
  }

  .progression-bar {
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 0.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 0.5rem;

    li {
      width: 100%;
      padding: 0.75rem;
      border-radius: 4px;
      font-weight: 500;
      font-size: 1.125rem;

      &.active {
        background-color: #E1F4F8;
        border: 1px solid #CBD5E1;
      }
    }
  }



}

@media screen and (min-width: 1500px) {
  .progress {
    position: absolute;
    transform: translateX(250%);
  }
}

@media screen and (min-height: 800px) {
  .btn-container {
    position: absolute;
    bottom: 5vh;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 0;


  }

}
</style>
