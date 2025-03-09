import { defineStore } from 'pinia'
import { ref } from 'vue';
import type { Ref } from 'vue';
import type { User, Association, modifyAssociation } from '@/interfaces/userInterface';
import apiService from '@/services/apiService';
import router from '@/router';
import type { ApiResponse } from '@/interfaces/apiResponseInterface';

export const useAccountStore = defineStore('account', () => {
    const tokenName = 'access_token';
    const CurrentUser: Ref<User|undefined> = ref();
    const isLoggedIn = ref(false);

    const setToken = (token: string) => {
        //set token in local storage
        localStorage.setItem(tokenName, token);
        
    }

    const getOrganizationById = async (organizationId: number) => {
        const response: ApiResponse = await apiService.kyGet('/users/association/' + organizationId);
        if (!response.success) {
            return undefined;
        }
        return response.data as unknown as Association;
    }

    async function logout() {
        isLoggedIn.value = false;
        localStorage.removeItem(tokenName);
        CurrentUser.value = undefined;
        router.push({ name: 'login' });
    }

    async function tokenLogin(): Promise<boolean> {
        const token:string = getAccessToken() as string;
        if (!token) {
            isLoggedIn.value = false;
            return isLoggedIn.value;
        }
        
        const response:ApiResponse = await apiService.kyPost('/users/token-login', {}, token);
        if (response.success !== true) {
            isLoggedIn.value = false;
            return isLoggedIn.value;
        }
        
        isLoggedIn.value = true;
        const user: User = {
            email: response.data.email as string,
            name: response.data.name as string,
            id: response.data.id as number,
            role: response.data.role as 'organization' | 'user',
            profile_picture: response.data.profile_picture as string,
        }
        CurrentUser.value = user;
        return isLoggedIn.value;
    }

    const changePassword = async (userId: number, token: string, oldPassword: string, newPassword: string) => {
        const response: ApiResponse = await apiService.kyPut('/users/password/' + userId, {
            old_password: oldPassword,
            new_password: newPassword
        }, token);
        return response.success;
    }

    const getAccessToken = ():string | undefined => {
        return localStorage.getItem(tokenName) as string;
    }

    const modifyUser = (userId: number, token: string, name?: string, profile_picture?: string) => {
        apiService.kyPut('/users/' + userId, {
            name: name,
            profile_picture: profile_picture,
        }, token);
    }

    const modifyAssociation = (asso: modifyAssociation) => {
        apiService.kyPut('/users/association/' + CurrentUser.value!.id, asso as Record<string, unknown>, getAccessToken()!);
    };

    const getAssoList = async () => {
        const response: ApiResponse = await apiService.kyGet('/users/associations');
        return response.data as unknown as Association[];
    }

    const googleLoginSignup = async (credential: string) => {
        const response: ApiResponse = await apiService.kyPostWithoutToken('/users/google-login', {'token': credential});
        if (response.success !== true) {
            return false;
        }
        setToken(response.data.access_token as string);
        isLoggedIn.value = true;
        router.push({ path: '/' });
        CurrentUser.value = response.data.user as User;
        isLoggedIn.value = true;
        return true;
    }

    return { setToken, logout, isLoggedIn, tokenLogin, CurrentUser, getAccessToken, modifyUser, changePassword, getOrganizationById, modifyAssociation, getAssoList, googleLoginSignup };
})