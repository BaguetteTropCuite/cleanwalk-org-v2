<script setup lang="ts">
import { watch, ref, onMounted, type Ref } from 'vue';
import { useAccountStore } from '@/stores/AccountStore';
import router from '@/router';
import iconShuffleArrow from './icons/icon-shuffle-arrow.vue';
import { v4 as uuidv4 } from 'uuid';
import { useUtilsStore } from '@/stores/UtilsStore';
import type { Association } from '@/interfaces/userInterface';
import ProfileAssoAddon from './ProfileAssoAddon.vue';
import BaseInput from './base/BaseInput.vue';
import BaseTextarea from './base/BaseTextarea.vue';
import LogoutButton from './buttons/LogoutButton.vue';

const getToken = useAccountStore().getAccessToken;
const showToast = useUtilsStore().showToast;

const currentMdp = ref('');
const newMdp = ref('');
const confirmNewMdp = ref('');
const accountStore = useAccountStore();

const currentUser = ref(useAccountStore().CurrentUser);
const association: Ref<Association | undefined> = ref(undefined);
const userName = ref(currentUser.value?.name);
const currentDescription: Ref<string | undefined> = ref(undefined);

// Separate debounce timeouts for name and description
let debounceTimeoutName: any;
let debounceTimeoutDescription: any;

onMounted(async () => {
    if (!currentUser.value) {
        router.push('/login');
        return;
    }
    if (currentUser.value?.role === 'organization') {
        association.value = await accountStore.getOrganizationById(currentUser.value.id!);
        currentDescription.value = association.value?.description;
    }
});

// Watcher for userName with its own debounce logic
watch(() => userName.value, () => {
    if (debounceTimeoutName) {
        clearTimeout(debounceTimeoutName);
    }

    if (userName.value === useAccountStore().CurrentUser?.name) {
        return;
    }

    debounceTimeoutName = setTimeout(() => {
        if (!userName.value || userName.value === '') {
            debounceTimeoutName = undefined;
            userName.value = currentUser.value?.name;
            showToast('Veuillez entrer un nom valide', false);
            return;
        }
        useAccountStore().modifyUser(currentUser.value!.id!, getToken()!, userName.value);
        showToast('Votre nom a été modifié', true);
        useAccountStore().CurrentUser!.name = userName.value;
        debounceTimeoutName = undefined;
    }, 2000);
});

// Watcher for currentDescription with its own debounce logic
watch(() => currentDescription.value, () => {
    if (debounceTimeoutDescription) {
        clearTimeout(debounceTimeoutDescription);
    }

    if (currentDescription.value === association.value?.description) {
        return;
    }

    debounceTimeoutDescription = setTimeout(() => {
        useAccountStore().modifyAssociation({ description: currentDescription.value });
        showToast('Votre description a été modifiée', true);
        debounceTimeoutDescription = undefined;
    }, 2000);
});

const changePassword = async () => {
    if (!currentMdp.value || !newMdp.value || !confirmNewMdp.value) {
        showToast('Veuillez remplir tous les champs', false);
        return;
    }

    if (newMdp.value !== confirmNewMdp.value) {
        showToast('Les mots de passe ne correspondent pas', false);
        return;
    }

    const response = await useAccountStore().changePassword(currentUser.value!.id!, getToken()!, currentMdp.value, newMdp.value);
    if (response) {
        showToast('Votre mot de passe a été modifié', true);
    } else {
        showToast('Mot de passe actuel incorrect', false);
    }
    currentMdp.value = '';
    newMdp.value = '';
    confirmNewMdp.value = '';
};

const changeUserPP = () => {
    currentUser.value!.profile_picture = 'https://api.dicebear.com/8.x/fun-emoji/svg?seed=' + uuidv4();

    // Clear the previous timeout if it exists
    if (debounceTimeoutName) {
        clearTimeout(debounceTimeoutName);
    }

    // Set a new timeout
    debounceTimeoutName = setTimeout(() => {
        useAccountStore().modifyUser(currentUser.value!.id!, getToken()!, undefined, currentUser.value!.profile_picture);
        showToast('Votre photo de profil a été modifiée', true);
        useAccountStore().CurrentUser!.profile_picture = currentUser.value!.profile_picture;
        debounceTimeoutName = undefined; // Reset the timeout variable
    }, 2000);
};
</script>
<template>
    <section class="container">

        <profile-asso-addon v-if="association" :Asso="association"/>
        
        <div class="img-user" v-if="currentUser?.role !== 'organization'">
            <img class="pp" :src="currentUser?.profile_picture" alt="cover-img">
            <div @click="changeUserPP()" class="icon-shuffle-arrow">
                <iconShuffleArrow />
            </div>
        </div>
        <div class="content">
            <h3>{{ currentUser?.email }}</h3>
            <BaseInput v-model="userName" name="name" type="text" label="Nom" placeholder="Votre nom" />
            <BaseTextarea v-model="currentDescription" name="description" label="Description" placeholder="Votre description" />
            <form @submit.prevent="changePassword()">
                <BaseInput v-model="currentMdp" name="mdp" type="password" label="Mot de passe actuel" placeholder="Votre mot de passe" />
                <BaseInput v-model="newMdp" name="newMdp" type="password" label="Nouveau mot de passe" placeholder="Votre nouveau mot de passe" />
                <BaseInput v-model="confirmNewMdp" name="confirmNewMdp" type="password" label="Confirmation du nouveau mot de passe" placeholder="Confirmez votre nouveau mot de passe" />
                <button class="action-button" type="submit">Changer votre mot de passe</button>
            </form>
            <LogoutButton />
        </div>
    </section>

</template>
<style scoped lang="scss">
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;

  .asso-imgs {
    margin-top: 58px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;

    .pp {
      width: 96px;
      aspect-ratio: 1;
      object-fit: cover;
      border-radius: 9999px;
      position: relative;
      margin-top: -48px;
    }

    .icon-photo {
      &.pp-icon {
        position: relative;
        margin-top: -25px;
        z-index: 999;
        margin-right: -60px;
      }
    }
  }

  .img-user {
    margin-top: 9rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .pp {
      width: 96px;
      aspect-ratio: 1;
      object-fit: cover;
      border-radius: 9999px;
      position: relative;
      margin-top: -48px;
    }

    .icon-shuffle-arrow {
      width: 26px;
      height: 26px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 9999px;
      padding-right: 1px;
      padding-bottom: 1px;
      margin-top: -25px;
      z-index: 999;
      margin-right: -60px;
      stroke: #fff;
      background-color: var(--color-primary);
      transition: transform 0.3s ease-in-out;

      &:active {
        transform: rotate(-180deg);
        transition: transform 0.2s ease-in-out;
      }
    }
  }

  .content {
    width: 100%;
    padding: 1rem 2.45rem 0;

    h3 {
      margin-bottom: 1rem;
    }

    form {
      display: flex;
      width: 100%;
      flex-direction: column;
      color: #94A3B8;

      .action-button {
        margin-top: 1.5rem;
      }
    }

    .danger-button {
      margin-top: 3.5rem;
    }
  }

  .icon-photo {
    background-color: var(--color-primary);
    stroke: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px;
    border-radius: 9999px;
    width: 26px;
    height: 26px;

    &.cover {
      position: absolute;
      top: 85px;
      right: 10px;
      z-index: 999;
    }
  }

  .cover-img {
    width: 100%;
    aspect-ratio: 16/5;
    object-fit: cover;
    margin-top: 78px;
  }

  @media (min-width: 768px) {
        width: 40rem;
        margin: 0 auto;
        padding-top: 2rem;
    }
}
</style>