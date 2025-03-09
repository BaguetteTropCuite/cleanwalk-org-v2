<script setup lang="ts">
import iconAdd from '@/components/icons/icon-add.vue';
import iconDiscover from '@/components/icons/icon-discover.vue';
import iconMap from '@/components/icons/icon-map.vue';
import iconBurger from '@/components/icons/icon-burger.vue';
import { useAccountStore } from '@/stores/AccountStore';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useDevice } from '@/composables/useDevice';

const currentPage = ref('');
const route = useRoute();
let discoverPageName:string = '';
const { isMobile } = useDevice(); // Utilisation du composable pour détecter mobile/desktop
const user = useAccountStore().CurrentUser;

//local storage
onMounted(() => {
    currentPage.value = route.name as string;
    discoverPageName = localStorage.getItem('discoverPage') ?? 'associations';
});


</script>
<template>
    <nav class="nav" v-if="isMobile">
        <ul class="container" :class="{ 'shadow': currentPage !== 'home'}">
            <li :class="{ 'active': currentPage === 'home' || currentPage === 'cleanwalk'}">
                <router-link to="/" class="redirect">
                    <iconMap />
                    <div>Carte</div>
                </router-link>
            </li>
            <li :class="{ 'active': currentPage.includes('add')}">
                <router-link to="/add/cleanwalk" class="redirect">
                    <iconAdd />
                    <div>Ajouter</div>
                </router-link>
            </li>
            <li :class="{ 'active': currentPage === 'associations' || currentPage === 'associations'}">
                <router-link :to="'/'+ discoverPageName" class="redirect">
                    <iconDiscover />
                    <div>Découvrir</div>
                </router-link>
            </li>
            <li :class="{ 'active': currentPage.includes('menu')}" >
                <router-link to='/menu' class="redirect">
                    <iconBurger />
                    <div>Menu</div>
                </router-link>
            </li>
        </ul>
    </nav>
    <nav class="nav-desktop" v-else>
        <img src="../assets/logo.svg" alt="logo cleanwalk.org" class="logo">
        <div class="links">
            <router-link class="link" to="/" :class="{ 'active': currentPage === 'home' || currentPage === 'cleanwalk'}">Accueil</router-link>
            <router-link class="link" to="/add/cleanwalk" :class="{ 'active': currentPage.includes('add')}">Ajouter cleanwalk</router-link>
            <router-link class="link" :to="'/'+ discoverPageName" :class="{ 'active': currentPage === 'associations' || currentPage === 'associations'}">Découvrir</router-link>
            <router-link class="link" to='/menu' :class="{ 'active': currentPage.includes('menu')}">Menu</router-link>
        </div>
        <div v-if="user">
            <router-link to="/menu/profile" class="account">
                <div>{{ user.name }}</div>
                <img :src="user.profile_picture" alt="profile_picture">
            </router-link>
        </div>
        <div class="infos"v-else>
            <router-link to="/login">Se connecter</router-link>
            <router-link to="/signup">S'inscrire</router-link>
        </div>

    </nav>

</template>

<style scoped lang="scss">
    @use '@/assets/main.scss';
    .nav {
        position: fixed;
        bottom: 0;
        width: 100%;
        font-size: 12px;
        font-weight: 500;
        z-index: 999;
        background-color: var(--color-nav-bg);
        font-family: "Roboto", sans-serif;

        .container {
            display: flex;
            justify-content: space-around;
            padding: 0.5rem;

            &.shadow {
                box-shadow: 0px -10px 100px rgba(194, 194, 194, 0.2);
            }

            li {
                list-style: none;
                stroke: var(--text-color-nav);
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                color: var(--text-color-nav);
                
                width: 100%;
                
                .redirect {
                    background: none;
                    padding: 0.3rem 0;
                    border-radius: 12px;
                    text-decoration: none;
                    color: inherit;
                    width: 100%;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;

                    .pp {
                        width: 26px;
                        height: 26px;
                        border-radius: 999px;
                        border: 2px solid #111; 
                    }
                }

                &.active {
                    stroke: var(--text-color-nav-active);
                    fill: var(--text-color-nav-active);
                    color: var(--text-color-nav-active);
                    
                    .redirect {
                        background-color: var(--color-primary);
                    }
                }
            }
        }
    }

    .nav-desktop {
            display: flex;
            justify-content: space-between;
            background-color: var(--color-primary);
            width: 100vw;
            color: #fff;
            position: fixed;
            top: 0;
            left: 0;
            height: 5.5rem;
            width: 100%;
            align-items: center;
            padding: 0 2rem;
            z-index: 9998;
        

        .link {
            font-weight: 700;
            margin: 0 1px;
            padding: 0.5rem 1rem;
            border-radius: 8px;

            &.active {
                background-color: #fff;
                color: var(--text-color-primary);
            }

        }

        .account {
            display: flex;
            gap: 1rem;
            align-items: center;

            img {
                width: 46px;
                height: 46px;
                border-radius: 999px;
                border: 1px solid #fff;
            }
            div {
                font-weight: 700;
            }
        }

        .infos {
            display: flex;
            gap: 1rem;

            div {
                font-weight: 700;
            }
        }
        
        
    }
</style>