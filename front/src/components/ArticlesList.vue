<script setup lang="ts">
import { type Article } from '@/interfaces/articleInterface';
import SearchBar from './SearchBar.vue';

const articles: Article[] = [
  {
    id: 1,
    content: "Contenu de l'article 1",
    title: "Titre de l'article 1",
    imageUrl: "https://cdn2.thecatapi.com/images/b4q.jpg",
    createdAt: "2022-04-02"
  },
  {
    id: 2,
    content: "Contenu de l'article 2",
    title: "Titre de l'article 2",
    imageUrl: "https://cdn2.thecatapi.com/images/8jl.jpg",
    createdAt: "2022-01-02"
  },
  {
    id: 3,
    content: "Contenu de l'article 3",
    title: "Titre de l'article 3",
    imageUrl: "https://cdn2.thecatapi.com/images/a66.jpg",
    createdAt: "2022-01-03"
  },
  {
    id: 4,
    content: "Contenu de l'article 4",
    title: "Titre de l'article 4",
    imageUrl: "https://cdn2.thecatapi.com/images/a90.jpg",
    createdAt: "2022-01-04"
  },
  {
    id: 5,
    content: "Contenu de l'article 5",
    title: "Titre de l'article 5",
    imageUrl: "https://cdn2.thecatapi.com/images/a66.jpg",
    createdAt: "2022-01-05"
  },
  {
    id: 3,
    content: "Contenu de l'article 3",
    title: "Titre de l'article 3",
    imageUrl: "https://cdn2.thecatapi.com/images/a66.jpg",
    createdAt: "2022-01-03"
  },
  {
    id: 4,
    content: "Contenu de l'article 4",
    title: "Titre de l'article 4",
    imageUrl: "https://cdn2.thecatapi.com/images/a90.jpg",
    createdAt: "2022-01-04"
  },
  {
    id: 5,
    content: "Contenu de l'article 5",
    title: "Titre de l'article 5",
    imageUrl: "https://cdn2.thecatapi.com/images/a66.jpg",
    createdAt: "2022-01-05"
  }
];

</script>

<template>
    <SearchBar />
    <div class="container">
        <div v-for="article in articles" :key="article.id" class="card">
            <img :src="article.imageUrl" alt="article image" />
            <div class="right">
              <h2>{{ article.title }}</h2>
              <div class="creation-date">{{ article.createdAt }}</div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">

.container{
  padding-top: 8rem;
  overflow: auto;
  display: flex;
  flex-direction: column;
  .card {
      display: flex;
      padding: 25px 0px;
      margin: 0 30px;
      border-bottom: 1px solid #CBD5E1;
  
      img {
          width: 22vw;
          aspect-ratio: 1;
          object-fit: cover;
          border-radius: 8px;
      }
      .right {
          padding: 2px 0 2px 1rem;
          display: flex;
          flex-grow: 1;
          flex-direction: column;
          justify-content: space-between;
          h2 {
            font-size: 12px;
            font-weight: 700;
          }
          .creation-date {
              font-size: 1rem;
              font-size: 8px;
          }
      }
  
  }
}
</style>
