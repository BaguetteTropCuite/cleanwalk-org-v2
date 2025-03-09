<script setup lang="ts">
import iconMiniMap from '../icons/icon-mini-map.vue';
import iconClock from '../icons/icon-clock.vue';
import type { Cleanwalk } from '@/interfaces/cleanwalkInterface';
import dateService from '@/services/dateService';
import IconExternalLink from '../icons/icon-external-link.vue';
import IconCross from '../icons/icon-cross.vue';

//define props
const props = defineProps<{
    cleanwalk: Cleanwalk,
    onClose: Function
}>()




const defaultCover = '/src/assets/default_cover.webp'

</script>

<template>
    <div class="solo-cw">
        <img :src="props.cleanwalk.img_url ?? defaultCover" alt="cleanwalk image">
        <div class="btn-container">
            <router-link class="btn" :to="{ name: 'cleanwalk', params: { id: props.cleanwalk.id } }">
                <IconExternalLink />
            </router-link>
            <button class="btn" @click="props.onClose()">
                <IconCross />
            </button>
        </div>
        <div class="container">
            
            <div class="content">
                <div class="title">{{ props.cleanwalk.name }}</div>
                <div class="date">
                    <icon-clock />
                    <div>{{ dateService.getCleanwalkWrittenDate(new Date(props.cleanwalk.date_begin), props.cleanwalk.duration) }}
                    </div>
                </div>
                <div>
                    <iconMiniMap />
                    <div>{{ props.cleanwalk.address }}</div>
                </div>
                <p>
                    {{ props.cleanwalk.description }}
                </p>
            </div>

            <div class="bot">
                <div class="organizer">
                    <div class="label">
                        Organisé par:
                    </div>
                    <h3>
                        {{ props.cleanwalk.host!.name }}
                    </h3>
                </div>
                <button class="action-button">
                    S'inscrire
                </button>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.solo-cw {
    position: fixed;
    transform: translateY(calc(50% + 2.75rem));
    background-color: #fff;
    z-index: 10000;
    bottom: 50%;
    left: 1rem;
    height: calc(100% - 9rem);
    border-radius: 8px;
    width: 30rem;
    overflow: hidden;
    stroke: #65707F;
    color: #65707F;
    font-size: 1.125rem;

    .btn-container {
        position: absolute;
        top:1rem;
        right: 1rem;
        z-index: 10001;
        display: flex;
        gap: 1.5rem;

        .btn {
            background-color: #E8E8E8;
            stroke: #363545;
            display: flex;
            width: 2.5rem;
            height: 2.5rem;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
        }
    }

    img {
        width: 100%;
        aspect-ratio: 21/9;
        object-fit: cover;
    }

    .container {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: calc(100% - 205px); // 205px = static height of the banner
    }

    
    .content {
        
        .title {
            padding-bottom: 1.5rem;
            color: #373646;
            font-size: 1.5625rem;
            font-weight: 700;
        }
        div {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        p {
            padding-top: 2.2rem;
        }
    }
    

    .bot {
        display: flex;
        flex-direction: column;
        padding-bottom: 0.7rem;
        gap:2rem;
    }
    .organizer {
        background-color: (var(--color-secondary));
        padding: 0.5rem;
        font-size: 1rem;
        border-radius: 8px;

        h3 {
            font-weight: 700;
            font-size: 1.25rem;
        }


    }

}
</style>