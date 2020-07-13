<template>
<nav>
    <v-toolbar class="secondary lighten-4">
    <v-layout align-center>
        <v-toolbar-title>
          <div class="d-inline"><v-img @click="goHome" src="/static/reaktor-logo.png" height="50px" contain></v-img></div>
        </v-toolbar-title>
          <div class="font-weight-light text-uppercase ml-4 mt-2 d-inline">cashdesk</div>
        <v-spacer></v-spacer>

        <v-btn icon :to="{ name: 'Settings'}">
          <v-icon>mdi-cog</v-icon>
        </v-btn>
    </v-layout>
    </v-toolbar>
</nav>
</template>

<script>
export default {
    methods: {
        goHome() {
            return this.$router.push("/").catch(()=>{});
        }
    }
}
</script>
