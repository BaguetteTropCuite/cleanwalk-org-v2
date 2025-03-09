<script setup lang="ts">
import PublicProfileAsso from '@/components/PublicProfileAsso.vue';
import TopBar from '@/components/TopBar.vue';
import JsonLdOrganization from '@/components/SEO/JsonLdOrganization.vue';
import { onMounted, watch, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/AccountStore';
import type { Association } from '@/interfaces/userInterface';

const route = useRoute();
const router = useRouter();
const accountStore = useAccountStore();
const association = ref<Association | undefined>(undefined);

// Update meta tags with organization information
const updateMetaTags = (asso: Association) => {
  if (!asso) return;
  
  // Create descriptive title and description
  const title = `${asso.name} | Cleanwalk.org`;
  const description = asso.description ? 
    `${asso.description.substring(0, 150)}${asso.description.length > 150 ? '...' : ''}` : 
    `Découvrez ${asso.name} et leurs initiatives de nettoyage environnemental sur Cleanwalk.org`;
  
  // Update document title
  document.title = title;
  
  // Update meta description
  const metaDescription = document.querySelector('meta[name="description"]');
  if (metaDescription) {
    metaDescription.setAttribute('content', description);
  }
  
  // Update Open Graph meta tags
  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) {
    ogTitle.setAttribute('content', title);
  }
  
  const ogDescription = document.querySelector('meta[property="og:description"]');
  if (ogDescription) {
    ogDescription.setAttribute('content', description);
  }
  
  // Update image if available
  if (asso.profile_picture) {
    const ogImage = document.querySelector('meta[property="og:image"]');
    if (ogImage) {
      ogImage.setAttribute('content', asso.profile_picture);
    }
  }

  // Update canonical URL
  let canonicalUrl = document.querySelector('link[rel="canonical"]');
  if (!canonicalUrl) {
    canonicalUrl = document.createElement('link');
    canonicalUrl.setAttribute('rel', 'canonical');
    document.head.appendChild(canonicalUrl);
  }
  canonicalUrl.setAttribute('href', `${window.location.origin}/associations/${asso.id}`);
}

onMounted(async () => {
  const id = +route.params.id;
  if (isNaN(id)) {
    router.push('/associations');
    return;
  }
  
  try {
    association.value = await accountStore.getOrganizationById(id);
    if (association.value) {
      updateMetaTags(association.value);
    } else {
      // Redirect to associations page if no association is found
      router.push('/associations');
    }
  } catch (error) {
    console.error("Failed to load association data for SEO:", error);
    // Redirect to associations page if there's an error loading the data
    router.push('/associations');
  }
});

// Watch for route changes to update meta tags
watch(() => route.params.id, async (newId) => {
  const id = +newId;
  if (isNaN(id)) return;
  
  try {
    association.value = await accountStore.getOrganizationById(id);
    if (association.value) {
      updateMetaTags(association.value);
    } else {
      // Redirect to associations page if no association is found
      router.push('/associations');
    }
  } catch (error) {
    console.error("Failed to load association data for SEO:", error);
    // Redirect to associations page if there's an error loading the data
    router.push('/associations');
  }
});
</script>

<template>
    <TopBar back-url="/associations" pageName="Association"/>
    <PublicProfileAsso v-if="association" :asso="association" />
    <!-- Add structured data JSON-LD for organizations -->
    <JsonLdOrganization v-if="association" :organization="association" />
</template>