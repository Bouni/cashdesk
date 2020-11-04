<template>
  <div class="settings">
    <v-container>
      <v-card>
         <v-card-title class="justify-center">
            <v-btn @click="addItem()"><v-icon>mdi-plus</v-icon> New</v-btn>
            <v-spacer></v-spacer>
            <v-btn icon color="secondary" fab small :to="{ name: 'Home'}">
              <v-icon dark>mdi-close</v-icon>
            </v-btn>
         </v-card-title>
         <v-card-text>
         <v-row v-for="item in items" :key="item.id" align="center" justify="center">
            <v-col cols="12" xs="12" sm="12" md="2">
                <v-img contain max-height="5em" :src="item.image" v-if="item.stock"></v-img>
                <v-img contain max-height="5em" :src="item.image" v-else style="filter: grayscale(100%);"></v-img>
            </v-col>
            <v-col cols="12" xs="12" sm="12" md="6" :class="[item.stock ? '' : 'grey--text']">
              <span class="headline">{{ item.brand }} {{item.name }}</span> <span class="">{{item.size}}</span>
            </v-col>
            <v-col :class="[item.stock ? '' : 'grey--text', 'headline']">
              {{ item.price | euro }}
            </v-col>
            <v-col>
              <v-switch :input-value="item.stock" @change="toggleStock(item.id, item.stock)" color="info" :label="item.stock ? 'verfügbar' : 'nicht verfügbar'"></v-switch>
            </v-col>
            <v-col>
             <v-row>
              <v-btn @click="editItem(item.id)" small fab class="mx-2 my-2" elevation="1"><v-icon>mdi-pencil</v-icon></v-btn>
              <v-btn @click="deleteItem(item.id)" small fab class="mx-2 my-2" elevation="1" color="red darken-4" dark><v-icon>mdi-trash-can</v-icon></v-btn>
              </v-row>
            </v-col>
            <v-col cols="12">
            <v-divider></v-divider>
            </v-col>
         </v-row>
         </v-card-text>
      </v-card> 

      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
        <v-card-title>
          <span class="headline">{{ dialogTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-if="item">
            <v-text-field v-model="item.brand" label="Marke" @blur="$v.item.brand.$touch()" :error-messages="brandErrors"></v-text-field>
            <v-text-field v-model="item.name" label="Produktname" @blur="$v.item.name.$touch()" :error-messages="nameErrors"></v-text-field>
            <v-text-field v-model="item.size" label="Grösse"></v-text-field>
            <v-text-field v-model="item.price" label="Preis" @blur="$v.item.price.$touch()" :error-messages="priceErrors"></v-text-field>
            <v-text-field v-model="item.image" label="Bild (URL)" @blur="$v.item.image.$touch()" :error-messages="imageErrors"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Abbrechen</v-btn>
          <v-btn color="green darken-1" text @click="saveItem(item.id)">Speichern</v-btn>
        </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="deleteDialog" max-width="600px">
        <v-card>
        <v-card-title>
          <span class="headline">Löschen?</span>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="deleteDialog = false">Abbrechen</v-btn>
          <v-btn color="red darken-1" text @click="deleteItem(item.id)">Löschen</v-btn>
        </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>


<script>

import { required, decimal, url, or } from 'vuelidate/lib/validators'

const localPath = function(p) {
  // Shit solution for check for local path 
  if(p.startsWith("/media/items/")) {
    return true;
  }
  return false;
}

export default {
  name: "Settings",
  data: () => ({
    dialog: false,
    dialogTitle: null,
    deleteDialog: false,
    item: null,
    items: [],

  }),

  validations: {
    item: {
        brand: {
          required,
        },
        name: {
          required,
        },
        price: {
          required,
          decimal
        },
        image: {
          required,
          urlOrPath: or(
            url, 
            localPath
          )
        }
    }
  },

  computed: {
    brandErrors() {
      const errors = []
      if (!this.$v.item.brand.$dirty) return errors
      !this.$v.item.brand.required && errors.push('Marke ist ein Pflichtfeld!')
      return errors
    },
    nameErrors() {
      const errors = []
      if (!this.$v.item.name.$dirty) return errors
      !this.$v.item.name.required && errors.push('Produktname ist ein Pflichtfeld!')
      return errors
    },
    priceErrors() {
      const errors = []
      if (!this.$v.item.price.$dirty) return errors
      !this.$v.item.price.required && errors.push('Preis ist ein Pflichtfeld!')
      !this.$v.item.price.decimal && errors.push('Preis muss eine Zahl sein!')
      return errors
    },
    imageErrors() {
      const errors = []
      if (!this.$v.item.image.$dirty) return errors
      !this.$v.item.image.required && errors.push('Bild ist ein Pflichtfeld!')
      !this.$v.item.image.urlOrPath && errors.push('Bild muss eine URL sein!')
      return errors
    }
  },

  filters: {
     euro(v) { return Number.parseFloat(v).toFixed(2) + ' €'}
  },

  methods: {
	deleteItem(id) {
      if(!this.deleteDialog) {
        this.item = Object.assign({},this.items.find(item => item.id == id));
        this.deleteDialog = true;
      } else {
        this.items.splice(this.items.findIndex(item => item.id == id), 1);
        fetch("api/items/" + id + "/", {
          method: "DELETE",
          headers: {
            "X-CSRFToken": this.$cookies.get('csrftoken'),
            "Accept": "application/json",
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          this.deleteDialog = false;
        })
      }
	},
    editItem(id) {
      this.dialogTitle = "Ändern";
      this.item = Object.assign({},this.items.find(item => item.id == id));
      this.dialog = true;
    },
    addItem() {
      this.dialogTitle = "Neu";
      this.item = {};
      this.dialog = true;
    },
	saveItem(id) {
      // trigger validation
      this.$v.$touch()
      console.log(this.item)
      // do not sumbit if invalid
      if(this.$v.$invalid) {
        return
      }
      if(this.dialogTitle == "Ändern") {
          this.items[this.items.findIndex(item => item.id == id)] = this.item;
          fetch("api/items/" + id + "/", {
            body: JSON.stringify(this.item),
            method: "PATCH",
            headers: {
              "X-CSRFToken": this.$cookies.get('csrftoken'),
              "Accept": "application/json",
              "Content-Type": "application/json",
            },
          })
          .then(() => {
            this.dialog = false;
          })
      } else {
          fetch("api/items/", {
            body: JSON.stringify(this.item),
            method: "POST",
            headers: {
              "X-CSRFToken": this.$cookies.get('csrftoken'),
              "Accept": "application/json",
              "Content-Type": "application/json",
            },
          })
          .then(() => {
            this.loadItems();
            this.dialog = false;
          }) 
      }
	},
    toggleStock(id, stock) {
      fetch("api/items/" + id + "/", {
        body: JSON.stringify({ "stock" : !stock}),
        method: "PATCH",
        headers: {
          "X-CSRFToken": this.$cookies.get('csrftoken'),
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
      })
      .then(() => {
		this.items[this.items.findIndex(item => item.id == id)].stock = !stock;
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
