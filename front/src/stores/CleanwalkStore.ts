import NominatimHelper from '@/helpers/NominatimHelper';
import databaseHelper from '@/helpers/databaseHelper';
import type { Cleanwalk } from '@/interfaces/cleanwalkInterface';
import { useAccountStore } from './AccountStore';
import router from '@/router';
import { defineStore } from 'pinia'
import {ref, computed} from 'vue';
import type {Ref} from 'vue';

const AccountStore = useAccountStore();

export const useCleanwalkStore = defineStore('cleanwalk', () => {

    const route:string = 'cleanwalks';

    const cleanwalks: Ref<Cleanwalk[]|undefined> = ref();


    async function getAllCleanwalks(): Promise<Cleanwalk[]|undefined> {
        const result = await databaseHelper.kyGet(route);
        if(result != undefined) {
            cleanwalks.value = result as Cleanwalk[];
        }
        return cleanwalks.value;
    }

    async function getCleanwalkById(id: number): Promise<Cleanwalk|undefined> {
        const result = await databaseHelper.kyGet(route + '/' + id);
        if(result != undefined) {
            return result as Cleanwalk;
        }
        return undefined;
    }

    async function createCleanwalk(cleanwalk: Cleanwalk, token:string): Promise<Cleanwalk|undefined> {
        const result = await databaseHelper.kyPost(route, cleanwalk, token);
        if(result != undefined) {
            return result as Cleanwalk;
        }
        return undefined;
    }

    async function updateCleanwalk(cleanwalk: Cleanwalk, token:string): Promise<Cleanwalk|undefined> {
        const result = await databaseHelper.kyPut(route + '/' + cleanwalk.id, cleanwalk, token);
        if(result != undefined) {
            return result as Cleanwalk;
        }
        return undefined;
    }

    return {getAllCleanwalks, cleanwalks}
   
});