<template>
  <div ref="wrapperRef" class="input-wrapper autocomplete-container">
    <label v-if="label" :for="uniqueId" class="label">{{ label }}</label>
    <form class="autocomplete-form">
      <div class="autocomplete-input-wrapper">
        <input
          ref="inputRef"
          v-model="inputValue"
          type="text"
          :id="uniqueId"
          :placeholder="placeholder"
          @click="displayOptionsList"
          @keyup="handleKeyNavigation"
        />
      </div>
      <hr class="autocomplete-divider" role="none" />
      <button
        tabIndex="0"
        type="button"
        class="autocomplete-button"
        @click="handleOnSearchClick"
      >
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
        </svg>
      </button>
    </form>
    <div :class="['autocomplete-list-wrapper', { active: isActive }]">
      <ul role="menu" class="autocomplete-options">
        <li
          v-if="loading"
          role="menuitem"
          class="loading-item"
        >
          Chargement...
        </li>
        <template v-else>
          <li
            v-for="option in filteredOptions"
            :key="option.place_id"
            role="menuitem"
            :class="{ selected: isSelected(option) }"
            @click="handleOnSelectOption(option)"
            @keydown.enter="handleOnSelectOption(option)"
            tabindex="0"
          >
            {{ formatSuggestion(option) }}
          </li>
          <li
            v-if="filteredOptions.length === 0 && debouncedValue.length > 0"
            role="menuitem"
            class="no-results"
          >
            {{ noOptionName }}
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, computed } from 'vue';

// Interface for location suggestions
interface Suggestion {
  place_id: number;
  osm_id: number;
  display_name: string;
  lat: string;
  lon: string;
  type: string;
  class: string;
  osm_type: string;
  licence: string;
  importance: number;
  boundingbox: string[];
  address?: {
    house_number?: string;
    road?: string;
    city?: string;
    town?: string;
    village?: string;
    postcode?: string;
    public_building?: string;
    [key: string]: string | undefined;
  };
}

// Props definition
const props = defineProps({
  value: {
    type: Object as () => Suggestion | null,
    default: null
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: "Saisissez l'adresse"
  },
  noOptionName: {
    type: String,
    default: "Aucune adresse trouvée"
  },
  openStreetMapUrl: {
    type: String,
    default: "https://nominatim.openstreetmap.org"
  },
  language: {
    type: String,
    default: "fr"
  },
  debounce: {
    type: Number,
    default: 300
  },
  countrycodes: {
    type: String,
    default: "fr,be"
  },
  name: {
    type: String,
    default: 'autocomplete-address'
  }
});

// Generate a unique ID for the input
const uniqueId = computed(() => `${props.name}-${Math.random().toString(36).substr(2, 9)}`);

const emit = defineEmits(['update:value', 'select-suggestion']);

// Component state
const inputValue = ref('');
const options = ref<Suggestion[]>([]);
const isActive = ref(false);
const loading = ref(false);
const selectedOption = ref<Suggestion | null>(null);
const debouncedValue = ref('');
const inputRef = ref<HTMLInputElement | null>(null);
const wrapperRef = ref<HTMLElement | null>(null);
let debounceTimeout: number | null = null;

// Filter out duplicate suggestions
const filteredOptions = computed(() => {
  return options.value.filter(
    (location, index, array) => 
      array.findIndex(
        (innerLocation) => innerLocation.display_name === location.display_name
      ) === index
  );
});

// Format suggestion for display
const formatSuggestion = (suggestion: Suggestion) => {
  if (suggestion.address) {
    const address = suggestion.address;
    const parts = [];
    if (address.house_number) parts.push(address.house_number);
    if (address.road) parts.push(address.road);
    if (address.public_building) parts.push(address.public_building);
    if (address.city || address.town || address.village) 
      parts.push(address.city || address.town || address.village);
    if (address.postcode) parts.push(address.postcode);
    return parts.join(', ');
  }
  return suggestion.display_name;
};

// Check if a suggestion is currently selected
const isSelected = (option: Suggestion) => {
  return selectedOption.value?.place_id === option.place_id;
};

// UI event handlers
const displayOptionsList = () => {
  isActive.value = true;
};

const hideOptionsList = () => {
  isActive.value = false;
};

const handleOnSearchClick = () => {
  displayOptionsList();
  if (inputValue.value) {
    debouncedFetchSuggestions();
  }
};

const handleKeyNavigation = (event: KeyboardEvent) => {
  // Update the input value
  debouncedFetchSuggestions();
  
  // Handle keyboard navigation here
  if (event.key === 'Escape') {
    hideOptionsList();
  }
};

const handleOnSelectOption = (option: Suggestion) => {
  selectedOption.value = option;
  inputValue.value = formatSuggestion(option);
  emit('update:value', option);
  emit('select-suggestion', {
    address: formatSuggestion(option),
    lat: option.lat,
    lon: option.lon,
    city: option.address?.city || option.address?.town || option.address?.village || '',
    osm_id: option.osm_id,
    place_id: option.place_id
  });
  hideOptionsList();
};

// Debounce utility
const debouncedFetchSuggestions = () => {
  if (debounceTimeout) {
    clearTimeout(debounceTimeout);
  }
  
  debounceTimeout = window.setTimeout(() => {
    debouncedValue.value = inputValue.value;
    fetchSuggestions();
  }, props.debounce);
};

// Fetch suggestions from API
const fetchSuggestions = async () => {
  if (debouncedValue.value.length < 3) {
    options.value = [];
    return;
  }
  
  loading.value = true;
  
  try {
    const response = await fetch(
      `${props.openStreetMapUrl}/search?format=json&accept-language=${props.language}&addressdetails=1&limit=5&countrycodes=${props.countrycodes}&q=${encodeURIComponent(debouncedValue.value)}`
    );
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    const data = await response.json();
    options.value = data;
  } catch (error) {
    console.error('Error fetching suggestions:', error);
    options.value = [];
  } finally {
    loading.value = false;
  }
};

// Handle outside clicks to close the options list
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as Node;
  if (wrapperRef.value && !wrapperRef.value.contains(target)) {
    hideOptionsList();
  }
};

// Watch for changes to the value prop
watch(() => props.value, (newValue) => {
  if (newValue) {
    selectedOption.value = newValue;
    inputValue.value = formatSuggestion(newValue);
  }
}, { immediate: true });

// Setup and cleanup
onMounted(() => {
  document.addEventListener('click', handleClickOutside, true);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside, true);
  if (debounceTimeout) {
    clearTimeout(debounceTimeout);
  }
});
</script>

<style scoped lang="scss">
.input-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;

  .label {
    font-size: 12px;
    font-weight: 500;
    position: relative;
    margin-bottom: -18px;
    width: fit-content;
    margin-left: 13px;
    margin-top: 5px;
    color: #94A3B8;
    position: relative;
    z-index: 1;

    &::before { // line under the label for hide the input border
      content: '';
      background-color: #fff;
      width: 110%;
      height: 1px;
      position: absolute;
      bottom: 9px;
      left: -5%;
      z-index: -1;
    }
  }
}

.autocomplete-container {
  position: relative;
  width: 100%;
}

.autocomplete-form {
  display: flex;
  border: 1px solid #94A3B8;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.autocomplete-input-wrapper {
  flex: 1;

  input {
    border: none;
    padding: 12px;
    font-size: 14px;
    font-weight: 500;
    width: 100%;
    outline: none;

    &::placeholder {
      color: #94A3B8;
    }

    &:focus {
      outline: none;
    }
  }
}

.autocomplete-divider {
  width: 1px;
  height: auto;
  margin: 6px 0;
  background-color: #E2E8F0;
  border: none;
}

.autocomplete-button {
  background: none;
  border: none;
  padding: 0 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    fill: #64748B;
  }
}

.autocomplete-list-wrapper {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1000;
  display: none;
  margin-top: 4px;

  &.active {
    display: block;
  }
}

.autocomplete-options {
  list-style: none;
  padding: 0;
  margin: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  max-height: 250px;
  overflow-y: auto;

  li {
    padding: 10px 12px;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover,
    &.selected {
      background-color: #F1F5F9;
    }
  }

  .loading-item,
  .no-results {
    color: #94A3B8;
    font-style: italic;
    cursor: default;

    &:hover {
      background-color: transparent;
    }
  }
}
</style>