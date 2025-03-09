<template>
    <section class="section">
        <img src="../../assets/coquelicots.webp" alt="banner" class="img">
        <div class="container">
            <slot></slot>
        </div>
    </section>
</template>


<style lang="scss" scoped>
.section {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.img {
    display: none;
}

.container {
    width: 100%;
}

@media (min-width: 1024px) {

    .img {
        display: block;
        height: 100vh;
        width: 50vw;
        object-fit: cover;
    }

    .container {
        width: 50vw;
    }

}
</style>