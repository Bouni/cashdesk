import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Account from "../views/Account.vue"
import Settings from "../views/Settings.vue"
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/account/:owner",
    name: "Account",
    component: Account,
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
  },
  {
  // will match everything
    path: '*',
    component: Home
  }
];

const router = new VueRouter({
  routes
});

router.beforeEach((to, from, next) => {
  document.title = "CASHDESK"
  next()
})

export default router;
