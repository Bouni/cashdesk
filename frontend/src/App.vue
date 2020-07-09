<template>
  <v-app>
    <Navigation/>
    <v-container>
      <router-view></router-view>
    </v-container>
  </v-app>
</template>

<script>
import Navigation from './components/Navigation'

export default {
  name: "App",

  components: {
    Navigation
  },

  data: () => ({
    //
  })
};
</script>
