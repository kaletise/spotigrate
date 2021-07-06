<template>
    <div class="login">
        <template v-if="!loading">
            <a class="button" role="button" href="https://accounts.spotify.com/authorize?client_id=4fbb1a9192cc4c3fada8a35993aff0d0&response_type=code&redirect_uri=https://spotigrate.ru/callback&scope=user-read-currently-playing,user-read-playback-state">LOG IN WITH SPOTIFY</a>
        </template>
        <template v-else>
            <h3>Загрузка...</h3>
        </template>
    </div>
</template>

<script>
import VueCookies from 'vue-cookies';

export default {
    data() {
        return {
            loading: true
        }
    },
    created() {
        if (VueCookies.isKey('session_id')) {
            window.location.href = '/dashboard';
        } else {
            this.loading = false;
        }
    }
}
</script>

<style scoped>
.login {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    margin-top: 60px;
}

.button {
    display: inline-block;
    font-weight: 700;
    text-align: center;
    cursor: pointer;
    border: 1px solid transparent;
    line-height: 1.5;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    transition-duration: .3s;
    border-width: 0;
    letter-spacing: 2px;
    min-width: 160px;
    text-transform: uppercase;
    white-space: normal;
    font-size: 16px;
    border-radius: 500px;
    padding: 19px 56px 21px;
    text-decoration: none;
    color: #ffffff;
    background-color: #1db954;
}

.button:hover {
    background-color: #1ed760;
    color: #ffffff;
}
</style>
