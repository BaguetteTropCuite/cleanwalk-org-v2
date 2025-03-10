<script setup lang="ts">
import SingleCleanwalk from '@/components/SingleCleanwalk.vue';
import navBar from '@/components/NavBar.vue';
import JsonLdEvent from '@/components/SEO/JsonLdEvent.vue';
import { onMounted, watch, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCleanwalkStore } from '@/stores/CleanwalkStore';
import { useAccountStore } from '@/stores/AccountStore';
import type { SingleCleanwalk as CleanwalkType } from '@/interfaces/cleanwalkInterface';

const route = useRoute();
const router = useRouter();
const cleanwalkStore = useCleanwalkStore();
const currentCleanwalk = ref<CleanwalkType | undefined>(undefined);
const currenUserId = ref(useAccountStore().CurrentUser?.id);

// Update meta tags when cleanwalk data is loaded 2
const updateMetaTags = (cleanwalk: CleanwalkType) => {
  if (!cleanwalk) return;
  
  // Create descriptive title and description
  const title = `${cleanwalk.name} | Cleanwalk.org`;
  const description = cleanwalk.description ? 
    `${cleanwalk.description.substring(0, 150)}${cleanwalk.description.length > 150 ? '...' : ''}` : 
    `Join this cleanwalk event in ${cleanwalk.address} organized by ${cleanwalk.host.name}`;
  
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
  if (cleanwalk.img_url) {
    const ogImage = document.querySelector('meta[property="og:image"]');
    if (ogImage) {
      ogImage.setAttribute('content', cleanwalk.img_url);
    }
  }
  // Update canonical URL
  let canonicalUrl = document.querySelector('link[rel="canonical"]');
  if (!canonicalUrl) {
    canonicalUrl = document.createElement('link');
    canonicalUrl.setAttribute('rel', 'canonical');
    document.head.appendChild(canonicalUrl);
  }
  canonicalUrl.setAttribute('href', `${window.location.origin}/cleanwalk/${cleanwalk.id}`);
}

const fetchCleanwalkData = async (id: number) => {
  if (isNaN(id)) {
    router.push('/404');
    return;
  }
  
  try {
    currentCleanwalk.value = await cleanwalkStore.getCleanwalkById(id, currenUserId.value);
    
    if (currentCleanwalk.value) {
      updateMetaTags(currentCleanwalk.value);
    } else {
      router.push('/404');
    }
  } catch (error) {
    console.error("Failed to load cleanwalk data:", error);
    router.push('/404');
  }
};

onMounted(async () => {
  const id = +route.params.id;
  await fetchCleanwalkData(id);
});

// Watch for route changes to update meta tags when navigating between different cleanwalk pages
watch(() => route.params.id, async (newId) => {
  const id = +newId;
  await fetchCleanwalkData(id);
});
</script>

<template>
  <!-- Use v-model to create two-way binding -->
  <SingleCleanwalk v-if="currentCleanwalk" v-model="currentCleanwalk" />
  <navBar />
  <!-- Add structured data JSON-LD for events -->
  <JsonLdEvent v-if="currentCleanwalk" :cleanwalk="currentCleanwalk" />
</template>