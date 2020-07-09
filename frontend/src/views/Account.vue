<template>
  <div class="Account">
    <v-container>
      <v-row>
        <v-col cols="12" sm="12" class="d-flex justify-center">
        <v-btn x-large :to="{ name: 'Home'}">
        <v-icon>mdi-reply</v-icon>
          Back
        </v-btn>
        </v-col>
      </v-row>
    
      <v-row>
        <v-col cols="12" sm="12" md="6">
          <v-card>    
            <v-card-title class="justify-center">
            {{ account.owner }}
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="12" md="12" class="d-flex justify-center">
                  <v-avatar color="grey" size="128" >
                    <img :src="`https://avatars.dicebear.com/api/bottts/${account.owner}.svg`">
                  </v-avatar>
                </v-col>
                <v-col cols="12" sm="12" md="12" :class="[ balanceColor(account.balance), 'd-flex justify-center']">
                  <span class="balance">Guthaben {{ account.balance | euro }}</span>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
          <v-card class="mt-3">
            <div class="text-center">
              <div class="py-5">
                <v-btn x-large color="amber" @click="vendDialog = true" dark class="mt-3">
                <v-icon large class="mr-4">mdi-bottle-soda-classic-outline</v-icon> Getränk kaufen</v-btn>

                <v-dialog v-model="vendDialog" width="auto ">
                  <v-card>
                  <v-card-title>
                    <span class="headline">Getränk kaufen</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container>
                    <v-row dense>
                      <v-col cols="12" sm="12" md="4" v-for="item in items" :key="item.id">
			            <v-row dense>
			              <v-col cols="12">
			            	<v-card dark @click="vendItem(item)" v-if="item.stock">
			            	  <div class="d-flex flex-no-wrap justify-space-between">
			            		<div>
			            		  <v-card-title class="headline">{{ item.brand }}</v-card-title>
			            		  <v-card-subtitle>
                                  <div class="balance">{{ item.name }} <span class="ml-4 text-h6">{{ item.size }}</span></div>
                                  <div class="balance mt-3">{{ item.price | euro }}</div>
                                  </v-card-subtitle>
			            		</div>
			            		<v-avatar class="ma-3" size="7em" tile>
			            		  <v-img contain max-height="7em" :src="item.image"></v-img>
			            		</v-avatar>
			            	  </div>
			            	</v-card>
			            	<v-card class="grey lighten-3" v-else>
			            	  <div class="d-flex flex-no-wrap justify-space-between">
			            		<div>
			            		  <v-card-title class="headline grey--text">{{ item.brand }}</v-card-title>
			            		  <v-card-subtitle>
                                  <div class="balance grey--text">{{ item.name }} <span class="ml-4 text-h6">{{ item.size }}</span></div>
                                  <div class="balance mt-3 grey--text">{{ item.price | euro }}</div>
                                  </v-card-subtitle>
			            		</div>
			            		<v-avatar class="ma-3" size="7em" tile>
			            		  <v-img contain max-height="7em" :src="item.image" style="filter: grayscale(100%);"></v-img>
			            		</v-avatar>
			            	  </div>
			            	</v-card>
			              </v-col>
			            </v-row>
				  	</v-col>
				    </v-row>	
				    </v-container>
				  </v-card-text>
				  </v-card> 
                </v-dialog>

              </div>
              <div class="py-5">
                <v-btn x-large color="success" @click="depositDialog = true" dark class="mb-3">
                <v-icon large class="mr-4">mdi-cash-plus</v-icon> Konto aufladen</v-btn>
                
                <v-dialog v-model="depositDialog"  width="auto ">
                  <v-card>
                  <v-card-title>
                    <span class="headline">Konto aufladen</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container>
                    <v-row dense>
                      <v-col cols="12" sm="12" md="4" v-for="item in euros" :key="item.value">
                      <v-container>
			            <v-row dense>
			              <v-col cols="12">
			            	<v-card dark @click="depositCash(item.value)">
			            	  <div class="d-flex flex-no-wrap justify-space-between">
			            		<div>
			            		  <v-card-title class="headline">{{ item.value }}€</v-card-title>
			            		</div>
			            		<v-avatar class="ma-3" size="7em" tile>
			            		  <v-img contain max-height="7em" :src="item.image"></v-img>
			            		</v-avatar>
			            	  </div>
			            	</v-card>
			              </v-col>
			            </v-row>
			          </v-container>
				  	</v-col>
				    </v-row>	
				    </v-container>
				  </v-card-text>
				  </v-card> 
                </v-dialog>

              </div>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="12" md="6">
          <v-card>    
            <v-card-title class="justify-center">
            Buchungen
            </v-card-title>
            <v-card-text>
              <v-list two-line>
                <v-list-item v-for="transaction in account.transaction" :key="transaction.id" @click="askRevokeTransaction(transaction)">
                    <v-list-item-content>
                       <v-list-item-title :class="striked(transaction.revoked)" v-text="transaction.comment"></v-list-item-title>
                       <v-list-item-subtitle :class="striked(transaction.revoked)" >{{ transaction.timestamp | date }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-list-item-action-text :class="[balanceColor(transaction.value), striked(transaction.revoked)]" style="font-size: 150%">
                      {{ transaction.value | euro }}
                      </v-list-item-action-text>
                    </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
          <v-dialog v-model="revokeDialog"  max-width="500">
            <v-card>
            <v-card-title>
              <span class="headline">Transaktion streichen?</span>
            </v-card-title>
			<v-card-actions>
			  <v-spacer></v-spacer>
			  <v-btn color="red darken-1" @click="revokeDialog = false;revokeTarget = null;">
				Abbrechen
			  </v-btn>
			  <v-btn color="green darken-1"	@click="revokeTransaction">
				Streichen
			  </v-btn>
			</v-card-actions>
            </v-card>
          </v-dialog>
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
  name: "Account",

  props: [ 'owner' ],

  data: () => ({
    account: {
        owner: '',
        balance: 0
    },
    vendDialog: false,
    depositDialog: false,
    revokeDialog: false,
    revokeTarget: null,
	items: [],
    euros: [
      {
        value: 0.5,
        image: "/static/img/euro-0.5.png"
      },
      {
        value: 1.0,
        image: "/static/img/euro-1.png"
      },
      {
        value: 2.0,
        image: "/static/img/euro-2.png"
      },
      {
        value: 5.0,
        image: "/static/img/euro-5.png"
      },
      {
        value: 10.0,
        image: "/static/img/euro-10.png"
      },
      {
        value: 20.0,
        image: "/static/img/euro-20.png"
      },
      {
        value: 50.0,
        image: "/static/img/euro-50.png"
      },
    ]
  }),

  filters: {
    euro(v) {
        return Number.parseFloat(v).toFixed(2) + ' €'
    },
    date(d) {
        const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric'};
        return new Date(d).toLocaleDateString('de-DE', options)
    }
  },

  methods: {
    vendItem(i) {
      var d = {
        timestamp: new Date().toISOString(),
        value: i.price * -1,
        comment: i.brand + " " + i.name,
        type: "gui",
        account: this.account.id 
      };
      fetch("api/transactions/", {
        body: JSON.stringify(d),
        method: "POST",
        headers: {
          "X-CSRFToken": this.$cookies.get('csrftoken'),
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
      })
      .then(() => {
        this.loadAccount(this.account.owner);
        this.vendDialog = false;
      }) 
    },
    depositCash(v) {
      var d = {
        timestamp: new Date().toISOString(),
        value: v,
        comment: "Einzahlung",
        type: "gui",
        account: this.account.id 
      };
      fetch("api/transactions/", {
        body: JSON.stringify(d),
        method: "POST",
        headers: {
          "X-CSRFToken": this.$cookies.get('csrftoken'),
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
      })
      .then(() => {
        this.loadAccount(this.account.owner);
        this.depositDialog = false;
      }) 
    },
    askRevokeTransaction(t) {
        this.revokeTarget = t;
        this.revokeDialog = true;
    },
    revokeTransaction() {
      fetch("api/transactions/" + this.revokeTarget.id + "/", {
        body: JSON.stringify({ revoked : !this.revokeTarget.revoked}),
        method: "PATCH",
        headers: {
          "X-CSRFToken": this.$cookies.get('csrftoken'),
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
      })
      .then(() => {
        this.revokeTarget = null;
        this.revokeDialog = false;
        this.loadAccount(this.account.owner);
      }) 
    },
    loadAccount(owner) {
      fetch("api/accounts/" + owner + "/")
        .then(response => response.json())
        .then(data => {
          this.account = data;
        });
    },
    loadItems() {
      fetch("api/items/")
        .then(response => response.json())
        .then(data => {
          this.items = data;
        });
	},
    balanceColor(v) {
      if(v > 0) {
        return "green--text" ;
      } else if( v == 0 ) {
        return "amber--text";
      } else {
        return "red--text";
      }
    },
    striked(v) {
      return v ? 'text-decoration-line-through' : '';
    }
  },
  mounted() {	
    this.loadAccount(this.$route.params.owner);
    this.loadItems();
  }
};
</script>

