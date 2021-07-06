export const routes = [
    { path: '/', component: () => import('@/auth/Login')},
    { path: '/callback', component: () => import('@/auth/Callback')},
    { path: '/dashboard', component: () => import('@/dashboard/Dashboard')}
];