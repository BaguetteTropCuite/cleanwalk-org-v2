<script setup lang="ts">
import iconMiniMap from '../icons/icon-mini-map.vue';
import iconClock from '../icons/icon-clock.vue';
import type { Cleanwalk } from '@/interfaces/cleanwalkInterface';
import dateService from '@/services/dateService';
// Get cleanwalk from props
const { cleanwalk } = defineProps<{ cleanwalk: Cleanwalk }>()

const defaultCover = '/src/assets/default_cover.webp'


</script>

<template>
    <div class="cleanwalk">
        <div class="left">
            <div class="title">{{ cleanwalk.name }}</div>

            <div class="date-location"> 
                <div>
                    <icon-clock />
                    <div>{{ dateService.getCleanwalkWrittenDate(new Date(cleanwalk.date_begin), cleanwalk.duration) }}</div>
                </div>
                <div>
                    <iconMiniMap />
                    <div>{{ cleanwalk.address }}</div>
                </div>
            </div>
            <div class="author">
                {{ cleanwalk.host!.name }}

            </div>
        </div>
        <img :src="cleanwalk.img_url ?? defaultCover" alt="cleanwalk">
    </div>
</template>

<style lang="scss" scoped>
.cleanwalk {
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    padding: 10px;
    background-color: #fff;
    width: 100%;
    stroke: #65707F;
    color: #65707F;
    display: flex;
    justify-content: space-between;

    .left {
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;

        .title {
            font-size: 16px;
            font-style: normal;
            font-weight: 500;
            color: #373646;
        }
    
        .date-location {
            display: flex;
            flex-direction: column;
            div {
                display: flex;
                align-items: center;
                gap: 5px;
            }
        }

        .author {
            background-color: #F2F2F2;
            width: fit-content;
            padding: 0 0.75rem;
            border-radius: 999px;
        }
    }


    img {
        width: 136px;
        height: 136px;
        border-radius: 8px;
        margin-left: 10px;
        object-fit: cover;
    }

}

</style>