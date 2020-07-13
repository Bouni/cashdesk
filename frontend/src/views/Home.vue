<template>
  <div class="home">
    <v-container>
      <v-row>
        <v-col v-for="account in accounts" :key="account.id" cols="12" sm="12" md="3">
          <v-card :to="{ name: 'Account', params: { owner: account.owner } }">    
            <v-card-title class="justify-center">
              {{ account.owner }}
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="12" class="d-flex justify-center">
                  <v-avatar color="grey" size="128" >
                    <img :src="`/media/owners/${account.owner}.svg`">    
                  </v-avatar>
                </v-col>
                <v-col cols="12" sm="12" :class="[balanceColor(account.balance), 'd-flex justify-center balance']" >
                  Guthaben {{ account.balance | euro }}
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style scoped>
.balance {
    font-size: 180%;
}
</style>

<script>
export default {
  name: "Home",
  data: () => ({
    accounts: []  
  }),
  filters: {
    euro(v) {
      return Number.parseFloat(v).toFixed(2) + ' €'
    }
  },
  methods: {
    balanceColor(v) {
      if(v > 0) {
        return "green--text" ;
      } else if( v == 0 ) {
        return "amber--text";
      } else {
        return "red--text";
      }
    }
  },
  mounted() {
    fetch("api/accounts/")
        .then(response => response.json())
        .then(data => {
          this.accounts = data;
        });
  }
};</script>
