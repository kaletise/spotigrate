<template>
    <div>
        <div class="callback" v-if="loading">
            <h3>Загрузка...</h3>
        </div>
        <div class="dashboard" v-else>
            <div class="wrapper d-flex">
                <nav id="sidebar" :class="{ active: sidebarToggle }">
                    <ul class="list-unstyled components">
                        <li class="active">
                            <a @click="page = 1" href="javascript:void(0);"><i class="las la-info-circle"></i><span>Статус</span></a>
                        </li>
                        <li class="active">
                            <a @click="page = 2" href="javascript:void(0);"><i class="lab la-vk"></i><span>Аккаунты ВКонтакте</span></a>
                        </li>
                        <li class="active">
                            <a @click="page = 3" href="javascript:void(0);"><i class="las la-cog"></i><span>Настройки</span></a>
                        </li>
                        <li class="active">
                            <a @click="logout();" href="javascript:void(0);"><i class="las la-sign-out-alt"></i><span>Выйти из аккаунта</span></a>
                        </li>
                    </ul>
                </nav>
                <div class="content">
                    <nav class="navbar">
                        <i class="las la-bars" @click="sidebarToggle = !sidebarToggle;"></i>
                        <span class="navbar-brand">Spotigrate</span>
                        <div class="ml-auto"></div>
                        <ul class="navbar-nav ml-auto">
                            <li class="nav-item nav-account">
                                <img class="profile-picture" :src="user.image"><span class="name">{{ user.display_name }}</span>
                            </li>
                        </ul>
                    </nav>
                    <div class="page">
                        <template v-if="page == 1">
                            <h3>Статус</h3>
                            <template v-if="user.accounts.length < 1">
                                <p class="error">Чтобы начать использовать сервис, Вам необходимо добавить по крайней мере один аккаунт в разделе <a href="javascript:void(0);" @click="page = 2">Аккаунты ВКонтакте</a></p>
                            </template>
                            Текущий статус трансляции:
                            <template v-if="status.reason == 0">
                                сейчас ничего не играет
                            </template>
                            <template v-else-if="status.reason == 1">
                                трансляция выключена в <a href="javascript:void(0);" @click="page = 3">настройках</a>
                            </template>
                            <template v-else-if="status.reason == 2">
                                ни один из аккаунтов не онлайн (активный режим)
                            </template>
                            <template v-else-if="status.reason == 4">
                                ни один <a href="javascript:void(0);" @click="page = 2">аккаунт ВКонтакте</a> не добавлен
                            </template>
                            <template v-else-if="status.reason == 5">
                                песня транслируется в статус ВКонтакте
                            </template>
                            <br><br>
                            <template v-if="status.song != ''">
                                Сейчас играет:
                                <div class="large-text">
                                    <i class="las la-play"></i>{{ status.song }}
                                </div>
                            </template>
                        </template>
                        <template v-if="page == 2">
                            <h3>Аккаунты ВКонтакте</h3>
                            <a class="button" role="button" href="javascript:void(0);" @click="page = 4"><i class="las la-plus"></i> Добавить аккаунт</a>
                            <template v-if="user.accounts.length > 0">
                                <br><br>
                                <h4>Привязанные аккаунты:</h4>
                                <table>
                                    <tr v-for="account in user.accounts">
                                        <td><a :href="'https://vk.com/id' + account.user_id"><img :src="account.photo" class="profile-photo">{{ account.first_name }} {{ account.last_name }}</a><a href="javascript:void(0);" @click="removeAccount(account.user_id);"><i class="las la-times"></i></a></td>
                                    </tr>
                                </table>
                            </template>
                        </template>
                        <template v-if="page == 3">
                            <h3>Настройки</h3>
                            <template v-if="user.accounts.length < 1">
                                <p class="error">Чтобы начать использовать сервис, Вам необходимо добавить по крайней мере один аккаунт в разделе <a href="javascript:void(0);" @click="page = 2">Аккаунты ВКонтакте</a></p>
                            </template>

                            <div :class="{ inactive: user.accounts.length < 1 }">
                                <p>Трансляция музыки в статус:</p>
                                <label class="radio-container disabled">
                                    Включена
                                    <input type="radio" :value="true" v-model="user.settings.enabled">
                                    <span class="checkmark"></span>
                                </label>
                                <label class="radio-container disabled">
                                    Выключена
                                    <input type="radio" :value="false" v-model="user.settings.enabled">
                                    <span class="checkmark"></span>
                                </label><br>

                                <p>Выберите режим работы:</p>
                                <label class="radio-container disabled">
                                    Форсированный
                                    <div class="tooltip-custom">
                                        (?)
                                        <span class="tooltip-custom-text">Spotigrate будет поддерживать Вас онлайн при трансляции музыки в статус</span>
                                    </div>
                                    <input type="radio" :value="1" v-model="user.settings.mode">
                                    <span class="checkmark"></span>
                                </label>
                                <label class="radio-container disabled">
                                    Активный
                                    <div class="tooltip-custom">
                                        (?)
                                        <span class="tooltip-custom-text">Spotigrate будет транслировать музыку в статус только когда Вы онлайн</span>
                                    </div>
                                    <input type="radio" :value="2" v-model="user.settings.mode">
                                    <span class="checkmark"></span>
                                </label>
                                <label class="radio-container disabled">
                                    Пассивный
                                    <div class="tooltip-custom">
                                        (?)
                                        <span class="tooltip-custom-text">Spotigrate будет транслировать музыку в статус независимо от Вашего онлайна</span>
                                    </div>
                                    <input type="radio" :value="3" v-model="user.settings.mode">
                                    <span class="checkmark"></span>
                                </label>
                            </div>
                        </template>
                        <template v-if="page == 4">
                            <h3>Аккаунты ВКонтакте</h3>
                            Добавить аккаунт<br><br>
                            <div class="input-container" :class="{'invalid' : addError}">
                                <input spellcheck="false" v-model.trim="access_token">
                                <label for="username" class="login-form-color-cover">Ваш токен</label>
                                <label for="username">Ваш токен</label>
                                <i class="las la-key"></i>
                                <span class="input-error" v-if="addError">Не удалось добавить аккаунт. Скорее всего, токен, который Вы ввели, недействителен</span>
                            </div>
                            <a class="button" role="button" href="javascript:void(0);" @click="addAccount();"><i class="las la-plus"></i> Добавить аккаунт</a><br><br>
                            <p>Инструкция по добавлению аккаунта ВКонтакте:</p>
                            1. Откройте следующую ссылку: <a href="https://oauth.vk.com/authorize?client_id=6146827&scope=66568&redirect_uri=https://api.vk.com/&display=page&response_type=token&revoke=1">https://oauth.vk.com/authorize?client_id=6146827&scope=66568&redirect_uri=https://api.vk.com/&display=page&response_type=token&revoke=1</a><br>
                            2. Авторизуйтесь под аккаунтом ВКонтакте, который Вы хотите привязать (если требуется) и нажмите <b>Разрешить</b><br>
                            3. Скопируйте значение параметра access_token из адресной строки браузера (это безопасно!), вставьте в поле <b>Ваш токен</b> и нажмите <b>Добавить аккаунт</b><br><br>
                            Пример токена: <a href="javascript:void(0);">8d15cd3e7f230301697c6ebf3a34fd2f6474d950c8b7582e0157003ed57fd1dbcd9497db922da519a0d12</a>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import VueCookies from 'vue-cookies';

import * as api from '@/api';

export default {
    data() {
        return {
            loading: true,
            fullyLoaded: false,
            sidebarToggle: false,
            access_token: '',
            addError: false,
            page: 1,
            user: {
                accounts: [],
                image: 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
                settings: {
                    enabled: true,
                    mode: 1
                }
            },
            status: {
                song: '',
                broadcasting: false,
                reason: 0
            }
        }
    },
    watch: {
        'user.settings': {
            deep: true,
            handler () {
                if (this.fullyLoaded) {
                    api.call('user.updateSettings', {session_id: VueCookies.get('session_id'), settings: JSON.stringify(this.user.settings)});
                } else {
                    this.fullyLoaded = true;
                }
            }
        }
    },
    methods: {
        logout() {
            VueCookies.remove('session_id');
            window.location.href = '/';
        },
        getStatus() {
            api.call('user.getStatus', {session_id: VueCookies.get('session_id')}).then((response) => {
                if (response.data.status == 1) {
                    this.status = response.data.data;
                }
            });
        },
        addAccount() {
            this.addError = false;
            api.call('user.addAccount', {session_id: VueCookies.get('session_id'), access_token: this.access_token}).then((response) => {
                if (response.data.status == 0) {
                    this.addError = true;
                } else if (response.data.status == 1) {
                    this.page = 2;
                    this.access_token = '';
                    this.user.accounts.push(response.data.user);
                }
            }).catch(() => {
                this.addError = true;
            });
        },
        removeAccount(user_id) {
            api.call('user.removeAccount', {session_id: VueCookies.get('session_id'), user_id: user_id}).then((response) => {
                if (response.data.status == 1) {
                    this.page = 2;
                    this.user.accounts = this.user.accounts.filter(function(value, index, arr) { 
                        return value.user_id != user_id;
                    });
                }
            });
        },
        startStatusGetter() {
            this.getStatus();
            setInterval(() => {
                this.getStatus();
            }, 5000);
        }
    },
    mounted() {
        api.call('session.get', {session_id: VueCookies.get('session_id')}).then((response) => {
            if (response.data.status == 0) {
                VueCookies.remove('session_id');
                window.location.href = '/';
            } else if (response.data.status == 1) {
                this.user = response.data.user;
                this.loading = false;
                this.startStatusGetter();
            }
        });
    }
}
</script>

<style scoped>
.callback {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    margin-top: 60px;
}

.large-text {
    font-size: 22px;
    margin-bottom: 10px;
}

.large-text i {
    margin-right: 10px;
}

.input-container {
    position: relative;
    z-index: 1;
    padding: 10px 0;
}

.input-container input {
    padding-left: 45px;
    width: 100%;
    height: 50px;
    padding-right: 10px;
    border-radius: 4px;
    font-weight: 600;
}

.input-container .input-error {
    color: #cf1a2b;
    display: block;
    font-size: 12px;
}

.input-container.invalid > label {
    color: #cf1a2b;
}

.input-container.invalid > input {
    border: 1px solid #cf1a2b !important;
}

.input-container label {
    position: absolute;
    left: 38px;
    padding: 0 8px;
    font-size: 12px;
    transform: translateY(-50%);
}

.input-container label.login-form-color-cover {
    color: transparent !important;
}

.input-container i {
    position: absolute;
    top: 0;
    padding: 10px 8px;
    font-size: 28px;
    display: flex;
    height: 70px;
    align-items: center;
}

.input-container input:focus {
    outline: none;
}

.input-container label.login-form-color-cover:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50%;
    z-index: -10;
}

.input-container input {
    color: #0a0a0a;
    border: 1px solid #e3e3f3;
    background-color: #f8f8f8;
}

.input-container input:-webkit-autofill,
.input-container input:-webkit-autofill:hover, 
.input-container input:-webkit-autofill:focus {
    -webkit-text-fill-color: #0a0a0a;
    -webkit-box-shadow: 0 0 0px 1000px #f8f8f8 inset;
}

.input-container label {
    color: #000000;
}

.input-container label.login-form-color-cover {
    background-color: #f8f8f8;
}

.input-container label.login-form-color-cover:after {
    background-color: #f8f8f8;
}

.input-container i {
    color: #000000;
}

.tooltip-custom {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black;
}

.tooltip-custom .tooltip-custom-text {
    visibility: hidden;
    width: 220px;
    padding: 5px 10px;
    background-color: #555555;
    color: #ffffff;
    text-align: center;
    border-radius: 6px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -110px;
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip-custom .tooltip-custom-text::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #555555 transparent transparent transparent;
}

.tooltip-custom:hover .tooltip-custom-text {
    visibility: visible;
    opacity: 1;
}

.inactive {
    opacity: 0.4;
    pointer-events: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.disabled {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.radio-container {
    display: block;
    position: relative;
    padding-left: 35px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 16px;
}

.radio-container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
}

.checkmark {
    position: absolute;
    top: 0;
    left: 0;
    height: 25px;
    width: 25px;
    background-color: #eee;
    border-radius: 50%;
}

.radio-container:hover input ~ .checkmark {
    background-color: #cccccc;
}

.radio-container input:checked ~ .checkmark {
    background-color: #428ee4;
}

.checkmark:after {
    content: "";
    position: absolute;
    display: none;
}

.radio-container input:checked ~ .checkmark:after {
    display: block;
}

.radio-container .checkmark:after {
    top: 9px;
    left: 9px;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: white;
}

@font-face {
    font-family: 'Gotham';
    src: url('/fonts/GothamMedium.otf');
}

.button {
    display: inline-block;
    font-weight: 700;
    text-align: center;
    cursor: pointer;
    border: 1px solid transparent;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    transition-duration: .3s;
    border-width: 0;
    letter-spacing: 2px;
    text-transform: uppercase;
    white-space: normal;
    font-size: 13px;
    border-radius: 500px;
    padding: 15px 50px;
    text-decoration: none;
    color: #ffffff;
    background-color: #428ee4;
    margin-top: 10px;
}

.error {
    color: #cf1a2b;
}

.dashboard {
    font-family: 'Gotham';
    height: 100%;
    overflow-x: hidden;
    background-color: #f8f8f8;
    color: #000000;
}

a {
    text-decoration: none;
}

a:hover {
    text-decoration: none;
}

span {
    font-size: 15px;
}

.name {
    font-size: 16px;
    font-weight: bold;
}

.page {
    padding: 20px;
}

.nav-account {
    position: relative;
    top: 0;
    left: 0;
}

.nav-cursor {
    cursor: pointer;
}

.navbar-brand {
    font-size: 20px;
}

.ml-auto, .mx-auto {
    margin-left: auto!important;
}

.profile-picture {
    width: 40px;
    height: 40px;
    position: relative;
    top: 0;
    left: 0;
    margin-right: 10px;
    border-radius: 50%;
}

.profile-photo {
    width: 50px;
    height: 50px;
    position: relative;
    top: 0;
    left: 0;
    margin-right: 10px;
    border-radius: 50%;
}

.la-times {
    margin-left: 10px;
    color: #cf1a2b;
}

.navbar {
    height: 62px;
    width: 100%;
    position: relative;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    padding: .5rem 1rem;
}

.content {
    width: 100%;
    min-height: 100vh;
    transition: all 0.3s;
}

.la-bars {
    font-size: 36px;
    margin-right: 10px;
}

.la-bars:hover {
    cursor: pointer;
}

.page {
    padding: 20px;
}

#sidebar {
    min-width: 270px;
    max-width: 270px;
    transition: all 0.3s;
}

#sidebar.active {
    min-width: 60px;
    max-width: 60px;
    text-align: center;
}

#sidebar ul.components li a i {
    font-size: 24px;
}

#sidebar.active ul.components li a {
    font-size: 14px;
    padding: 10px 0;
}

#sidebar.active ul.components li a i {
    margin-right: 0;
    display: block;
    font-size: 24px;
}

#sidebar ul li a {
    padding: 10px 30px;
    display: block;
    color: white;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

#sidebar ul li a:hover {
    text-decoration: none;
    transition: all 0.3s;
}

#sidebar ul li a i {
    margin-right: 15px;
    font-size: 20px;
}

#sidebar.active ul li a span {
    display: none;
}

@media (max-width: 992px) {
    #sidebar {
        min-width: 150px;
        max-width: 150px;
        text-align: center;
        margin-left: -150px !important;
    }

    #sidebar ul li a span {
        display: none;
    }

    #sidebar.active {
        margin-left: 0 !important;
    }
}

@media (max-width: 680px) {
    .navbar-brand {
        display: none;
    }
}

.navbar {
    background-color: #ffffff;
}

.la-bars:hover {
    color: #428ee4;
}

.navbar-brand {
    color: #000000;
}

.navbar-brand:hover {
    color: #000000;
}

#sidebar {
    background-color: #428ee4;
}

#sidebar ul li a:hover {
    background-color: #ffffff;
    color: #428ee4;
}
</style>