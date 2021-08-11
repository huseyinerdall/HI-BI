<template>
  <v-card class="mt-10 mx-auto" style="width:90%">
    <v-tabs vertical color="deep-orange darken-3" class="caption" dense min-height="300">
      <v-tab>
        <v-icon left>demo-icon icon-database-1</v-icon>
        Database Configuration
      </v-tab>

      <v-tab-item>
        <v-card flat>
          <v-card-text>
              <v-container>
                <div class="database-type">
                  <div><input type="radio" v-model="type" value="postgresql" id="postgresql" checked><label for="postgresql"></label></div>
                  <div><input type="radio" v-model="type" value="mysql" id="mysql"><label for="mysql"></label></div>
                  <div><input type="radio" v-model="type" value="oracle" id="oracle"><label for="oracle"></label></div>
                  <div><input type="radio" v-model="type" value="sqlite" id="sqlite"><label for="sqlite"></label></div>
                </div>
                <v-text-field style="width:25%;margin-top:40px;" label="Custom Port" placeholder="Custom Port" outlined dense v-model="customPort" @input="setPort"></v-text-field>
                
                <v-container>
                  <v-row>

                    <v-col cols="12" sm="6" md="3">
                      <v-text-field
                        label="Username"
                        outlined dense
                        v-model="database.user"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" sm="6" md="3">
                      <v-text-field
                        label="Password"
                        outlined dense
                        v-model="database.password"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" sm="6" md="3">
                      <v-text-field
                        label="Address"
                        outlined dense
                        v-model="database.address"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" sm="6" md="3">
                      <v-text-field
                        label="Database Name"
                        outlined dense
                        v-model="database.db_name"
                      ></v-text-field>
                    </v-col>

                  </v-row>
                </v-container>

                <v-btn color="primary" @click="setDatabase">
                  <v-icon>demo-icon icon-cog-outline</v-icon>Configure
                </v-btn>
              </v-container>
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs>
    <Loader></Loader>
    <v-row justify="center">
      <v-dialog v-model="confirm" max-width="290">
        <v-card>
          <v-card-title class="headline">{{confirmO.title}}</v-card-title>
          <v-card-text>{{confirmO.text}}</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="confirm = false">Cancel</v-btn>
            <v-btn color="green darken-1" text @click="confirmO.callback(confirmO.arg)">Agree</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-card>
</template>

<script>
const axios = require('axios');
import Loader from '@/components/Loader'
  export default {
    data: () => ({
      type: '',
      database: {
        type: '',
        port: '',
        user: '',
        password: '',
        db_name: '',
        address: ''
      },
      confirm: false,
      confirmO: {},
      customPort: '',
    }),

    created () {
      this.configuredDB();
    },

    methods: {
      confirmF: function(options){
        this.confirmO = options;
        this.confirm = true;
      },
      setPort: function(e){
        console.log(e);
        if(!isNaN(e)){
          this.database.port = this.customPort;
        }
      },
      setDatabase: function(){
        const app = this;
        axios.post('http://localhost:5000/configureDB', this.database)
        .then(function (response) {/* 
          app.$store.commit('changeGraphList',JSON.parse(response.data)); */
          app.$store.commit('changeGraphList',JSON.parse(response.data.graphs));
          app.$store.commit('changeHTMLList',JSON.parse(response.data.htmls));
          app.reportname = response.data.name;
        })
        .catch(function (error) {
          
          console.log(error);
        });
      },
      configuredDB: function(){
        const app = this;
        axios.get('http://localhost:5000/configuredDB')
        .then(function (response) {
          console.log(response.data);
          app.database = response.data;
          document.getElementById(app.database.type).click()
        })
        .catch(function (error) {
          console.log(error);
        })
      }
    },
    watch:{
      type: function(n,o){
        console.log(n,o);
        if(this.customPort){
          this.database.port = this.customPort;
          switch (n) {
            case 'postgresql':
              this.database.type = 'postgresql';
              break;
            case 'mysql':
              this.database.type = 'mysql';
              break;
            case 'oracle':
              this.database.type = 'oracle';
              break;
            case 'sqlite':
              this.database.type = 'sqlite';
              break;
            default:
              break;
          }
          return;
        }
        
        switch (n) {
          case 'postgresql':
            this.database.type = 'postgresql';
            this.database.port = '5432';
            break;
          case 'mysql':
            this.database.type = 'mysql';
            this.database.port = '1111';
            break;
          case 'oracle':
            this.database.type = 'oracle';
            this.database.port = '2222';
            break;
          case 'sqlite':
            this.database.type = 'sqlite';
            this.database.port = '3333';
            break;
          default:
            break;
        }
      }
    },
    components: {
      Loader,
    },
  }
</script>

<style scoped>
  .database-type>div:nth-child(1)>label{background-image: url('../assets/img/postgresql.png');}
  .database-type>div:nth-child(2)>label{background-image: url('../assets/img/mysql.png');}
  .database-type>div:nth-child(3)>label{background-image: url('../assets/img/oracle.png');}
  .database-type>div:nth-child(4)>label{background-image: url('../assets/img/sqlite.png');}
  .database-type{
    display: flex;
    margin: 0px 0 0 0;
    flex-direction: row;
}
.database-type>div{
    width:calc(100%/4);
    height: 100px;
}
.database-type>div>label{
    display: block;
    width: 100%;
    height: 114%;
    cursor: pointer;
    background-position: center center;
    background-size:40%;
    background-repeat: no-repeat;
    border-radius: 5px;
    transition: all 0.3s;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    padding-bottom: 4px;
}
.database-type input[type="radio"]{
    display:none;
}
.database-type input[type="radio"]:checked+label{
    border:4px solid rgb(216, 67, 21);
}
</style>