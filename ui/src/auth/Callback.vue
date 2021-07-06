<template>
    <div class="callback">
        <template v-if="error">
            <template v-if="error == 'access_denied'">
                <h3>Вы запретили доступ к своему Spotify аккаунту</h3>
            </template>
            <template v-else-if="error == 'connection_error'">
                <h3>Ошибка подключения к серверу</h3>
            </template>
            <template v-else>
                <h3>Неизвестная ошибка</h3>
            </template>
            <a href="/">Попробовать снова</a>
        </template>
        <template v-else>
            <h3>Загрузка...</h3>
        </template>
    </div>
</template>

<script>
import VueCookies from 'vue-cookies';

import * as api from '@/api';

export default {
    data() {
        return {
            error: this.$route.query.error,
            code: this.$route.query.code
        }
    },
    mounted() {
        if (!this.error) {
            api.call('session.open', {code: this.code}).then((response) => {
                if (response.data.status == 0) {
                    this.error = 'unknown_error';
                } else if (response.data.status == 1) {
                    VueCookies.set('session_id', response.data.session_id, '3650d');
                    window.location.href = '/dashboard';
                }
            }).catch(() => {
                this.error = 'connection_error';
            });
        }
    }
}
</script>

<style scoped>
.callback {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    margin-top: 60px;
}
</style>