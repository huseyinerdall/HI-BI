<template>
  <div class="reports">
    <v-container class="grey lighten-5" sm="12" md="12">
      <v-alert v-if="reports.length == 0">There is no report for showing.You can add new one</v-alert>
      <v-row
      class="mb-6"
    >
      <v-col
        v-for="report in reports"
        :key="report.id"
      >
      <v-card
      max-width="270" class="report-card"
      >

        <div style="overflow:hidden;background-color: rgba(0, 0, 0, .4);height:120px;">
          <v-img
            class="white--text align-end report-image"
            src="../assets/img/report.jpg"
            contain
          >
          <v-card-title></v-card-title>
          </v-img>
        </div>
        <v-card-subtitle class="pb-0">{{ report.name }}</v-card-subtitle>
        <v-card-subtitle class="pb-0">{{ report.date | dateFormat }}</v-card-subtitle>

      <v-card-text class="text--primary">
      <div></div>

    </v-card-text>

    <v-card-actions>
      <router-link
      tag="span"
      :to="'/edit/'+report.id">
        <v-btn
          color="primary"
          class="ma-2"
          small
        >
          Edit
        </v-btn>
      </router-link>
      <router-link
      tag="span"
      :to="'/report/'+report.id">
        <v-btn
          color="primary"
          class="ma-2"
          small
        >
           View
        </v-btn>
      </router-link>
        <v-btn
          color="error"
          class="ma-2"
          small
          @click="confirmF({title:'Delete operation?',text:'Are you sure delete this report?',callback:deleteReport,arg:report.id})"
        >
           delete
        </v-btn>

    </v-card-actions>
  </v-card>
  </v-col>
    </v-row>
    </v-container>

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

    <Loader></Loader>
  </div>
</template>

<script>
const axios = require('axios');
import Loader from '@/components/Loader'

export default {
  name: "Reports",
  data: function() {
    return {
      reports:[],
      reportProperties: [],
      confirm: false,
      confirmO: {},
    }
  },
  methods: {
    getReportInfos: function(){
      const app = this;
      axios.get('http://localhost:5000/getReportInfos')
      .then(function (response) {
        console.log(response.data)
        for (let i = 0; i < response.data.length; i++) {
          app.reports.push(response.data[i])
          app.reportProperties.push(JSON.parse(response.data[i]['content']))
        }
      })
      .catch(function (error) {
        console.log(error);
      })
    },
    deleteReport: function(id){
      const app = this;
        axios.post('http://localhost:5000/deleteReport', {
          id: id,
        })
        .then(function (response) {
          console.log(response.data);
        })
        .catch(function (error) {
          console.log(error);
        });
        for (let i = 0; i < app.reports.length; i++) {
          if(app.reports[i]['id'] == id){
            app.reports.splice(i,1);
          }
        }
        this.confirm = false;
    },
    confirmF: function(options){
      this.confirmO = options;
      this.confirm = true;
    },
  },
  created() {
    this.getReportInfos();
  },
  filters: {
    dateFormat: function(value){
      return (value+"").substring(0,16);
    }
  },
  components: {
    Loader,
  },
  computed: {
    reportJSON: function() {
      return JSON.parse(this.reports)
    }
  },
  mounted() {
  },
};
</script>

<style>
.report-image{
  transition: all 0.2s;
  height: 200px;
}
.report-card:hover .report-image{
  transform: rotate(0deg);
}
</style>