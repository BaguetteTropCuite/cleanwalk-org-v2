<script setup lang="ts">
import { ref } from 'vue';
import apiService from '@/services/apiService';
import type { ApiResponse } from '@/interfaces/apiResponseInterface';
import { v4 as uuidv4 } from 'uuid';
import { useUtilsStore } from '@/stores/UtilsStore';
import router from '@/router';
import BaseInput from '@/components/base/BaseInput.vue';
import { GoogleLogin } from 'vue3-google-login';
import { useAccountStore } from '@/stores/AccountStore';
import { type CallbackTypes } from 'vue3-google-login';

const accountStore = useAccountStore();
const showToast = useUtilsStore().showToast;

const callbackGoogleLogin: CallbackTypes.CredentialCallback = async (response) => {
    await accountStore.googleLoginSignup(response.credential);
};

const email = ref("");
const name = ref("");
const password = ref("");
const confirmPassword = ref("");

const signup = async ( ) => {
    if(!name.value) {
        showToast("Veuillez renseigner votre prénom", false);
        return;
    }
    if(!email.value) {
        showToast("Veuillez renseigner votre email", false);
        return;
    }
    if(!password.value || !confirmPassword.value) {
        showToast("Veuillez renseigner votre mot de passe", false);
        return;
    }
    if(password.value !== confirmPassword.value) {
        showToast("Les mots de passe ne correspondent pas", false);
        return;
    }
    const response:ApiResponse = await apiService.kyPostWithoutToken( "/users", {
        email: email.value,
        password: password.value,
        name: name.value,
        profile_picture: 'https://api.dicebear.com/8.x/fun-emoji/svg?seed=' + uuidv4(),
        role_id: 1
    });
    if(response.success === false) {
        showToast(response.data.message as string, false);
        return;
    } else {
        showToast("Votre compte a été créé avec succès", true);
        setTimeout(() => {
            router.push('/login').then(() => router.go(0));
        }, 1000);

    }
    
    
}

</script>

<template>
    <section class="container">

        <h1>
            Choisissez le type de compte qui vous correspond :
        </h1>

        <GoogleLogin :callback="callbackGoogleLogin" />
        <div class="or">
            <div class="line"></div>
            <span>ou</span>
            <div class="line"></div>
        </div>
        <form @submit.prevent="signup()">
            <BaseInput v-model="name" label="Comment voulez vous qu'on vous appelle ?" name="name" type="text" placeholder="nom, prenom, pseudo ... ." />
            <BaseInput v-model="email" label="Email" name="email" type="email" placeholder="user@domain.fr" />
            <BaseInput v-model="password" label="Mot de passe" name="password" type="password" placeholder="Votre mot de passe" />
            <BaseInput v-model="confirmPassword" label="Confirmez le mot de passe" name="confirmPassword" type="password" placeholder="Votre mot de passe" />
            <button class="action-button" type="submit">S' inscrire</button>
            <router-link to="/login" class="go-login">
                Vous utilisez déjà cleanwalk.org : <span>Connectez-vous</span>
            </router-link>
        </form>
        </section>
</template>

<style scoped lang="scss">


    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        overflow: hidden;
        padding: 0 2rem;
        h1 {
            font-size: 24px;
            font-weight: 500;
            margin-bottom: 1rem;
        }
    }

    .go-login {
        color: var(--text-color-secondary);
        font-size: 12px;
        width: 100%;
        text-align: left;
        margin-top: 2rem;

        span {
            color: var(--text-color-primary);
            font-weight: 500;
            cursor: pointer;
            text-decoration: underline;
        
        }
    }
    .or {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem 0;
        span {
            margin: 0 1rem;
        }
        .line {
            width: 35vw;
            height: 1px;
            background-color: #747474;
        }
    }

    form {
            margin-top: 3rem;
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
</style>