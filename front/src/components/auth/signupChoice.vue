<script setup lang="ts">
import { ref } from 'vue';
import apiService from '@/services/apiService';
import type { ApiResponse } from '@/interfaces/apiResponseInterface';
import { v4 as uuidv4 } from 'uuid';
import { useUtilsStore } from '@/stores/UtilsStore';
import router from '@/router';
import BaseInput from '@/components/base/BaseInput.vue';
import IconPerson from '@/components/icons/icon-person.vue';
import IconAsso from '@/components/icons/icon-asso.vue';

const showToast = useUtilsStore().showToast;


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

        <!-- <GoogleLogin :callback="callback" />
        <div class="or">
            <div class="line"></div>
            <span>ou</span>
            <div class="line"></div> -->
        <div class="choice-container">
            <router-link to="/signup/perso" class="choice">
                <IconPerson class="choice-icon" />
                <span>Compte personnel</span>
            </router-link>
            <router-link to="/signup/asso" class="choice">
                <IconAsso class="choice-icon" />
                <span>Compte association</span>
            </router-link>
        </div>
        <router-link to="/login" class="go-login">
            Vous utilisez déjà cleanwalk.org : <span>Connectez-vous</span>
        </router-link>
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

        .choice-container {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-direction: column;
            .choice {
                padding: 1rem 2rem;
                border-radius: 5px;
                border-radius: 8px;
                border: 1px solid #CBD5E1;
                background-color: var(--primary-color);
                color: #373646;
                font-weight: 700;
                text-decoration: none;
                font-size: 24px;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                min-width: 26rem;
                &:hover {
                    background-color: var(--primary-color-dark);
                }
                
                .choice-icon {
                    width: 48px; 
                    height: 48px;
                }
            }
        }
    }

</style>