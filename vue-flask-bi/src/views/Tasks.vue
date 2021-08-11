<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="tasks"
      sort-by="calories"
      dense
      hide-default-footer
      class="elevation-1"
    >
      <template v-slot:item.actions="{  }">
        <v-icon
          small
          @click="confirmF({title:'Delete operation?',text:'Are you sure delete this report?',callback:shutdownTask,arg:task.id})"
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        There is not any task.
      </template>
    </v-data-table>
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
  </v-container>
</template>


<script>
import Loader from '@/components/Loader'
const axios = require('axios');
  export default {
    data: () => ({
      headers: [
        {
          text: 'Task ID',
          align: 'start',
          sortable: false,
          value: 'id',
        },
        { text: 'Task', value: 'type' },
        { text: 'Report', value: 'report' },
        { text: 'Next Run Date', value: 'nextRunDate' },
        { text: 'Date(Create)', value: 'date' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      tasks: [],
      confirm: false,
      confirmO: {},
    }),

    created () {
      this.getTasks();
    },

    methods: {
      getTasks: function(){
        const app = this;
        axios.get('http://localhost:5000/getTasks')
        .then(function (response) {
          console.log(response.data);
          app.tasks = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      shutdownTask (id) {
        const app = this;
        axios.post('http://localhost:5000/shutdownTask', {
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
    components: {
      Loader,
    },
  }
</script>