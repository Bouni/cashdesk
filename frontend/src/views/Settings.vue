<template>
  <div class="settings">
    <v-container>
      <v-card>
         <v-card-title class="justify-center">
           Getränke
         </v-card-title>
         <v-card-text>
         <v-row v-for="item in items" :key="item.id" align="center" justify="center">
            <v-col cols="12" xs="12" sm="12" md="2">
			    <v-img contain max-height="5em" :src="item.image" v-if="item.stock"></v-img>
			    <v-img contain max-height="5em" :src="item.image" v-else style="filter: grayscale(100%);"></v-img>
            </v-col>
            <v-col cols="12" xs="12" sm="12" md="6" :class="[item.stock ? '' : 'grey--text', 'headline']">
              {{ item.brand }} {{item.name }}
            </v-col>
            <v-col cols="12" xs="12" sm="6" md="2" :class="[item.stock ? '' : 'grey--text', 'headline']">
              {{ item.price | euro }}
            </v-col>
            <v-col cols="12" xs="12" sm="6" md="2" class="text-center headline">
              <v-btn v-if="item.stock" @click="toggleStock(item)">
                <v-icon color="red darken-4">mdi-do-not-disturb</v-icon>
              </v-btn>
              <v-btn v-else @click="toggleStock(item)">
                <v-icon color="green darken-4">mdi-plus-circle</v-icon>
              </v-btn>
            </v-col>
         </v-row>
         </v-card-text>
      </v-card> 
    </v-container>
  </div>
</template>


<script>
export default {
  name: "Settings",
  data: () => ({
    items: [],
  }),

  filters: {
    euro(v) {
        return Number.parseFloat(v).toFixed(2) + ' €'
    }
  },

  methods: {
    textColor(v) {
      if(v) {
        return 'grey--text'
      }
    },
    toggleStock(item) {
      fetch("api/items/" + item.id + "/", {
        body: JSON.stringify({ stock : !item.stock}),
        method: "PATCH",
        headers: {
          "X-CSRFToken": this.$cookies.get('csrftoken'),
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
      })
      .then(() => {
        this.loadItems();
      }) 
    },
    loadItems() {
      fetch("api/items/")
        .then(response => response.json())
        .then(data => {
          this.items = data;
        });
	},
  },

  mounted() {	
	this.loadItems();
  }
}
</script>
