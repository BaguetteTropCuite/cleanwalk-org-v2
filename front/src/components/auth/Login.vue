<script setup lang="ts">
import { ref } from 'vue';
import apiService from '@/services/apiService';
import { useAccountStore } from '@/stores/AccountStore';
import type { User } from '@/interfaces/userInterface';
import { useUtilsStore } from '@/stores/UtilsStore';
import { GoogleLogin } from 'vue3-google-login';
import BaseInput from '@/components/base/BaseInput.vue';

const router = useRouter();

const accountStore = useAccountStore();
const showToast = useUtilsStore().showToast;
import { type CallbackTypes } from 'vue3-google-login';
import { useRouter } from 'vue-router';

const email = ref("");

const password = ref("");

const callbackGoogleLogin: CallbackTypes.CredentialCallback = async (response) => {
    await accountStore.googleLoginSignup(response.credential);
};

const login = async () => {
    if (!email.value) {
        showToast("Veuillez renseigner votre email", false);
        return;
    }
    if (!password.value) {
        showToast("Veuillez renseigner votre mot de passe", false);
        return;
    }

    // Call the login API
    const response = await apiService.kyPostWithoutToken("/users/login", {
        email: email.value,
        password: password.value
    });
    if (response.success === false) {
        showToast('Email ou mot de passe incorrect', false);
        return;
    }
    const user: User = {
        email: response.data.email as string,
        name: response.data.name as string,
        id: response.data.id as number,
        profile_picture: response.data.profile_picture as string,
        role: response.data.role as "organization" | "user",
    }
    accountStore.CurrentUser = user;
    router.push({ path: '/' });
    accountStore.setToken(response.data.access_token as string);

}


</script>

<template>
    <div class="login-container">
        <div class="login">
            <h1>
                Connectez-vous
            </h1>
            <GoogleLogin :callback="callbackGoogleLogin" />
            <div class="or">
                <div class="line"></div>
                <span>ou</span>
                <div class="line"></div>
            </div>
            <form @submit.prevent="login()">
                <BaseInput v-model="email" name="email" type="email" label="Email" placeholder="Votre mot de passe" />
                <BaseInput v-model="password" name="password" type="password" label="Mot de passe"
                    placeholder="Votre mot de passe" />
                <button class="action-button" type="submit">Se connecter</button>
            </form>
            <router-link to="/forgot-password" class="forgot-password">
                Mot de passe oublié ?
            </router-link>
        </div>
        <router-link to="/signup" class="go-signup">
            Vous êtes nouveau chez cleanwalk.org : <span class="span">Inscrivez-vous</span>
        </router-link>
    </div>
</template>

<style scoped lang="scss">
.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    width: 100%;
    height: 100vh;
    justify-content: space-evenly;
    padding: 0 2rem;

    .login {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;

        .forgot-password {
            width: 100%;
            padding-top: 1rem;
            text-align: right;
            font-size: 0.8rem;
            text-decoration: underline;
        }
    }

    h1 {
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 1rem;
        width: 100%;
    }
}

.go-signup {
    color: var(--text-color-secondary);
    font-size: 12px;
    width: 100%;
    text-align: left;
    margin-top: 2rem;

    .span {
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
    width: 100%;

    .line {
        width: 100%;
        height: 1px;
        background-color: #747474;
        margin: 0 2rem;
    }
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

@media (min-width: 1024px) {
    .login-container {
        padding-left: clamp(2rem, 10vw, 10rem);     padding-right: clamp(2rem, 10vw, 10rem);

    }
}
</style>