<script setup lang="ts">
import type { Association } from '@/interfaces/userInterface';
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
// Import your Organization interface


const props = defineProps<{
  organization: Association;
}>();

// Create structured data for the Organization
const structuredData = computed(() => {
  if (!props.organization) return {};
  
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': props.organization.name,
    'description': props.organization.description,
    'url': `${window.location.origin}/associations/${props.organization.id}`,
    'logo': props.organization.profile_picture,
    'image': props.organization.banner_img || props.organization.profile_picture,
    '@id': `${window.location.origin}/associations/${props.organization.id}#organization`
  };
});

// Handle script tag injection
const scriptEl = ref<HTMLScriptElement | null>(null);

// Use lifecycle hooks to manage the script element
onMounted(() => {
  // Create script element
  scriptEl.value = document.createElement('script');
  scriptEl.value.setAttribute('type', 'application/ld+json');
  scriptEl.value.textContent = JSON.stringify(structuredData.value);
  
  // Add to document head
  document.head.appendChild(scriptEl.value);
});

// Watch for changes to structured data
watch(() => structuredData.value, (newValue) => {
  if (scriptEl.value) {
    scriptEl.value.textContent = JSON.stringify(newValue);
  }
}, { deep: true });

// Clean up on component unmount
onUnmounted(() => {
  if (scriptEl.value && document.head.contains(scriptEl.value)) {
    document.head.removeChild(scriptEl.value);
  }
});
</script>

<template>
  <!-- JSON-LD data is injected via script in the document head -->
  <div style="display: none;"></div>
</template>