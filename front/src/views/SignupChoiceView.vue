<script setup lang="ts">
import AuthTemplate from '@/components/auth/authTemplate.vue';
import SignupChoice from '@/components/auth/signupChoice.vue';

</script>
<template>
    <!-- <SwithChoice categorie1="particulier" categorie2="associations/Organization" route1="signup" route2="signup/Organization" :activeCategory="true" /> -->
    <main>
        <AuthTemplate>
            <SignupChoice />
        </AuthTemplate>
    </main>
</template>