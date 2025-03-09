import nominatimService from '@/services/nominatimService';
import apiService from '@/services/apiService';
import type { Cleanwalk, CleanwalkCreation, SingleCleanwalk } from '@/interfaces/cleanwalkInterface';
import router from '@/router';
import { defineStore } from 'pinia'
import {ref, computed} from 'vue';
import type {Ref} from 'vue';
import { useAccountStore } from './AccountStore';


export const useCleanwalkStore = defineStore('cleanwalk', () => {
    const getToken = useAccountStore().getAccessToken;

    const route:string = '/cleanwalks';

    let cleanwalksTab: Ref<Cleanwalk[]> = ref([]);

    async function getAllCleanwalks() {
        const route = '/cleanwalks'; // Assure-toi que cette route est correcte et complète
        try {
            const result = await apiService.kyGet(route);
            if (result.success && result.data) {
                // Convertit les données seulement si elles existent et la requête a réussi
                cleanwalksTab.value = result.data as unknown as Cleanwalk[];
            } else {
                // Log une erreur si la requête a échoué
                console.error('Failed to fetch cleanwalks:', result.data);
            }
        } catch (error) {
            // Gestion des erreurs de la requête elle-même
            console.error('Request failed:', error);
        }
        return cleanwalksTab.value;
    }

    async function getCleanwalkById(id: number, userId?:number): Promise<SingleCleanwalk|undefined> {
        let url = route + '/' + id;
        if(userId) {
            url += '?user_id=' + userId;
        }
        const result = await apiService.kyGet(url);
        if(result.success && result.data) {
            return result.data as unknown as SingleCleanwalk;
        }
        return undefined;
    }

    async function createCleanwalk(cleanwalk: CleanwalkCreation): Promise<CleanwalkCreation|undefined> {
        const token = getToken();
        if (token === undefined) {
            router.push('/login');
            return undefined;
        }
        const result = await apiService.kyPost(route, cleanwalk as unknown as Record<string, unknown>, token);
        if(result != undefined) {
            return result.data as unknown as CleanwalkCreation;
        }
        return undefined;
    }

    async function updateCleanwalk(cleanwalk: Cleanwalk, token:string): Promise<Cleanwalk|undefined> {
        const result = await apiService.kyPut(route + '/' + cleanwalk.id, cleanwalk as unknown as Record<string, unknown>, token);
        if(result != undefined) {
            return result.data as unknown as Cleanwalk;
        }
        return undefined;
    }

    async function joinCleanwalk(cleanwalkId: number, token:string, nb_participants:number, user_id:number): Promise<boolean> {
        const result = await apiService.kyPost(route + '/join', {
            cleanwalk_id: cleanwalkId,
            user_id: user_id,
            nb_person: nb_participants
        }, token);
        if(result != undefined) {
            return result.success;
        }
        return false;
    }

    async function leaveCleanwalk(cleanwalkId: number, token:string, user_id:number): Promise<boolean> {
        const result = await apiService.kyDelete(route + '/leave', {
            cleanwalk_id: cleanwalkId,
            user_id: user_id
        }, token);
        if(result != undefined) {
            return result.success;
        }
        return false;
    }

    return {getAllCleanwalks, cleanwalksTab, getCleanwalkById, createCleanwalk, joinCleanwalk, leaveCleanwalk}
   
});