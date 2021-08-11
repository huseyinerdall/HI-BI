import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import store from "../store/index.js";

Vue.use(VueRouter);

const routes = [{
        path: "/",
        name: "Home",
        component: Home
    },
    {
        path: "/new",
        name: "New",
        component: () =>
            import ("../views/New.vue")
    },
    {
        path: "/edit/:id",
        name: "Edit",
        component: () =>
            import ("../views/Edit.vue")
    },
    {
        path: "/reports",
        name: "Reports",
        component: () =>
            import ("../views/Reports.vue")
    },
    {
        path: "/report/:id",
        name: "Report",
        component: () =>
            import ("../views/Report.vue")
    },
    {
        path: "/set-a-task",
        name: "New Task",
        component: () =>
            import ("../views/SetTask.vue")
    },
    {
        path: "/settings",
        name: "Settings",
        component: () =>
            import ("../views/Settings.vue")
    },
    {
        path: "/tasks",
        name: "Tasks",
        component: () =>
            import ("../views/Tasks.vue")
    },
    {
        path: "/login",
        name: "Login",
        component: () =>
            import ("../views/Login.vue")
    },
    {
        path: "/profile",
        name: "Profile",
        component: () =>
            import ("../views/Profile.vue")
    },
    {
        path: "/export/:id",
        name: "Export",
        component: () =>
            import ("../views/Export.vue")
    }
];

const router = new VueRouter({
    routes,
    store,
    mode: "history"
});



router.beforeEach((to, from, next) => {
    console.log(to, from, 'yesss');
    store.commit('changeLoader', true);
    next();
    /*
    if (!store.getters.isAuthenticated && to.name !== 'Login') {
        next('/login');
    } else {
        if (to.name === 'Login') {
            console.log('kldsdksld')
        }
        next();
    }
    */
});
router.afterEach(() => {
    setTimeout(() => {
        store.commit('changeLoader', false);
    }, 2000)

})
export default router;