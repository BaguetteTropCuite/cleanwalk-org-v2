import { createRouter, createWebHistory, type NavigationGuardNext, type RouteLocationNormalized } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAccountStore } from '@/stores/AccountStore';

const router = createRouter({
  history: createWebHistory((import.meta as any).env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Cleanwalk.org - Événements de Nettoyage Citoyen',
        description: 'Rejoignez Cleanwalk.org pour organiser et participer à des événements de nettoyage citoyen. Faites un impact environnemental positif dans votre région.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/cleanwalk/:id',
      name: 'cleanwalk',
      component: () => import('../views/SingleCleanwalkView.vue'),
      meta: {
        title: 'Détails de l\'Événement Cleanwalk | Cleanwalk.org',
        description: 'Détails sur un événement de nettoyage citoyen. Rejoignez une cleanwalk près de chez vous et aidez à faire la différence.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/add/cleanwalk',
      name: 'addCleanwalk',
      component: () => import('../views/AddCleanwalkView.vue'),
      meta: {
        title: 'Créer un Événement Cleanwalk | Cleanwalk.org',
        description: 'Organisez votre propre événement de nettoyage citoyen. Créez une cleanwalk et invitez les autres à rejoindre.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/associations',
      name: 'associations',
      component: () => import('../views/AssoListView.vue'),
      meta: {
        title: 'Organizations Environnementales | Cleanwalk.org',
        description: 'Découvrez des organizations et associations environnementales organisant des événements cleanwalk dans votre région.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/associations/:id',
      name: 'association',
      component: () => import('../views/PublicProfileAssoView.vue'),
      meta: {
        title: 'Profil de l\'Organization | Cleanwalk.org',
        description: 'Découvrez cette organization environnementale et leurs initiatives de nettoyage.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/menu',
      name: 'menu',
      component: () => import('../views/MenuView.vue'),
      meta: {
        title: 'Menu | Cleanwalk.org',
        description: 'Naviguez à travers les fonctionnalités et options de Cleanwalk.org.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/menu/profile',
      name: 'menuProfile',
      component: () => import('../views/ProfileView.vue'),
      meta: {
        title: 'Votre Profil | Cleanwalk.org',
        description: 'Gérez votre profil et vos préférences sur Cleanwalk.org.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: 'Connexion | Cleanwalk.org',
        description: 'Connectez-vous à votre compte Cleanwalk.org pour rejoindre ou créer des événements de nettoyage.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupChoiceView.vue'),
      meta: {
        title: 'Inscription | Cleanwalk.org',
        description: 'Créez un compte sur Cleanwalk.org pour participer à des événements de nettoyage citoyen.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/signup/asso',
      name: 'signupAsso',
      component: () => import('../views/SignupAssoView.vue'),
      meta: {
        title: 'Inscription Organization | Cleanwalk.org',
        description: 'Enregistrez votre organization environnementale sur Cleanwalk.org pour organiser des événements de nettoyage.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/signup/perso',
      name: 'signupPerso',
      component: () => import('../views/SignupView.vue'),
      meta: {
        title: 'Inscription Personnelle | Cleanwalk.org',
        description: 'Créez un compte personnel sur Cleanwalk.org pour rejoindre des événements de nettoyage citoyen.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('../views/SignupView.vue'),
      meta: {
        title: 'Déconnexion | Cleanwalk.org',
        description: 'Déconnectez-vous en toute sécurité de votre compte Cleanwalk.org.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/:catchAll(.*)',
      name: 'NotFound',
      component: () => import('../views/404.vue'),
      meta: {
        title: 'Page Non Trouvée | Cleanwalk.org',
        description: 'La page que vous recherchez n\'a pas été trouvée sur Cleanwalk.org.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/cleanwalk/edit/:id',
      name: 'editCleanwalk',
      component: () => import('../views/EditCleanwalkView.vue'),
      meta: {
        title: 'Modifier Cleanwalk | Cleanwalk.org',
        description: 'Mettez à jour les détails de votre événement de nettoyage citoyen.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/reset-password/:token',
      name: 'resetPassword',
      component: () => import('../views/ResetPasswordView.vue'),
      meta: {
        title: 'Réinitialiser le Mot de Passe | Cleanwalk.org',
        description: 'Créez un nouveau mot de passe pour votre compte Cleanwalk.org.',
        ogImage: '/default-banner.svg'
      }
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: () => import('../views/ForgotPasswordView.vue'),
      meta: {
        title: 'Mot de Passe Oublié | Cleanwalk.org',
        description: 'Demandez une réinitialisation de mot de passe pour votre compte Cleanwalk.org.',
        ogImage: '/default-banner.svg'
      }
    },
  ]
  
})

const routesRequiringAuth = ['profile', 'addCleanwalk'];

// SEO - Update meta tags based on route
router.beforeEach(async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
  // Authentication logic
  if(!useAccountStore().isLoggedIn) {
    await useAccountStore().tokenLogin();
  }
  if (routesRequiringAuth.includes(to.name as string) && !useAccountStore().isLoggedIn) {
    next({ name: 'login' });
  } else {
    // Update meta tags for SEO
    const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);
    const nearestWithDescription = to.matched.slice().reverse().find(r => r.meta && r.meta.description);
    const nearestWithOgImage = to.matched.slice().reverse().find(r => r.meta && r.meta.ogImage);

    // Update document title
    if(nearestWithTitle) {
      document.title = nearestWithTitle.meta.title as string;
    }

    // Update meta description
    const metaDescription = document.querySelector('meta[name="description"]');
    if(metaDescription && nearestWithDescription) {
      metaDescription.setAttribute('content', nearestWithDescription.meta.description as string);
    }

    // Update Open Graph meta tags
    const ogTitle = document.querySelector('meta[property="og:title"]');
    if(ogTitle && nearestWithTitle) {
      ogTitle.setAttribute('content', nearestWithTitle.meta.title as string);
    }

    const ogDescription = document.querySelector('meta[property="og:description"]');
    if(ogDescription && nearestWithDescription) {
      ogDescription.setAttribute('content', nearestWithDescription.meta.description as string);
    }

    const ogImage = document.querySelector('meta[property="og:image"]');
    if(ogImage && nearestWithOgImage) {
      const baseUrl = window.location.origin;
      ogImage.setAttribute('content', `${baseUrl}${nearestWithOgImage.meta.ogImage}`);
    }

    next();
  }
});

export default router
