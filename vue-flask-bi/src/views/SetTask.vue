<template>
  <v-container>
      <v-form
        ref="form"
        v-model="valid"
        lazy-validation
      >
          <v-alert dense type="info" class="mb-4 mt-4">If you wish running only one time, you should use <strong>Once</strong> option.</v-alert>
          <v-container>
            <v-row>
              <v-col cols="6">
                <v-combobox
                  v-model="reportName"
                  :items="reports"
                  label="Choose a report"
                  single-line
                  outlined
                  dense
                  required
                  :rules="[rules.required]"
                ></v-combobox>
              </v-col>
              <v-col cols="6">
                <v-combobox
                  v-model="type"
                  :items="taskTypes"
                  label="Task"
                  single-line
                  outlined
                  dense
                  required
                  :rules="[rules.required]"
                ></v-combobox>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12">
                <v-combobox
                  v-model="selectedDays"
                  :items="days"
                  label="Days"
                  multiple
                  single-line
                  outlined
                  dense
                  required
                  :rules="[rules.counter]"
                ></v-combobox>
              </v-col>
            </v-row>
            <v-row align="center" justify="center">
              <v-col cols="12">
                <v-combobox
                  v-model="selectedMonth"
                  :items="months"
                  label="Months"
                  multiple
                  outlined
                  dense
                  required
                  :rules="[rules.counter]"
                ></v-combobox>
              </v-col>
            </v-row>

            <v-row align="center" justify="center">
              <v-col cols="12">
                <v-menu
                  ref="menu"
                  v-model="menu2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="time"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="time"
                      label="Time"
                      readonly outlined dense
                      v-on="on"
                      required
                      :rules="[rules.required]"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-if="menu2"
                    v-model="time"
                    full-width
                    format="24hr"
                    @click:minute="$refs.menu.save(time)"
                  ></v-time-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
    <v-btn color="primary" @click="confirmF({title:'Setting Task?',text:'Your task customization is: <br><b>'+crontabForHuman[0]+'<br>'+crontabForHuman[1]+'<br>'+ crontabForHuman[2] + '</b>',callback:setTask})">Set task</v-btn>

    <v-row justify="center">
      <v-dialog v-model="confirm" max-width="400">
        <v-card>
          <v-card-title class="headline">{{confirmO.title}}</v-card-title>
          <v-card-text v-html="confirmO.text"></v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="confirm = false">Cancel</v-btn>
            <v-btn color="green darken-1" text @click="confirmO.callback">Agree</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <Loader></Loader>
  </v-container>
</template>

<script>
const axios = require('axios');
import Loader from '@/components/Loader'
  export default {
    name: "SetTask",
    data: () => ({
      valid: true,
      time: '',
      menu2: false,
      menu1: false,
      menu3: false,
      selectedDays: [],
      days:["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"],
      selectedMonth: [],
      months:["January","February","March","April","May","June","July", "August","September","October","November","December"],
      dateS:'',
      dateF:'',
      crontab: {
        minute:'*',
        hour: '*',
        dayOfMonth: '*',
        month: '*',
        dayOfWeek: '*'
      },
      crontabForHuman: [],
      confirm: false,
      confirmO: {},
      reports: [],
      reportsIDs: [],
      task: { type: '', report: '' },
      taskTypes: ['Emailing','Download locally'],
      rules: {
        required: value => value.length>0 || 'Required.',
        counter: value => value.length!=0 || 'You must choose any option',
      },
      type: '',
      reportName: '',
      selectedID: '',
      taskColors: {
        whatsapp: '#075e54',
        telegram: '#0088cc',
        emailing: '#d44638',
        download: '#E60023',
      }
    }),
    computed: {
    },
    methods: {
      trimFirstZero: function(str){
        if(str[0] == '0'){
          return str.substring(1);
        }
        return str;
      },
      getAllIndexes: function(parent, ch,int=0){
        var indexes = [];
        for (let i = 0; i < ch.length; i++) {
          indexes.push(+parent.indexOf(ch[i])+int);
        }
        return indexes;
      },
      confirmF: function(options){
        this.confirmO = options;
        this.confirm = true;
      },
      setTask(){
        this.$store.commit('changeLoader',true);
        const taskColor = this.taskColors[this.type.split(' ')[0].toLowerCase()]
        const app = this;
        this.$refs.form.validate();
        const crontabArray = this.crontab;
        axios.post('http://localhost:5000/setTask', {
          crontab: crontabArray,
          task: this.type,
          report: this.reportName,
          color: taskColor,
          report_id: app.selectedID
        })
        .then(function (response) {
          console.log(response.data);
          app.$router.go();
        })
        .catch(function (error) {
          console.log(error);
        });
        this.confirm = false;
      },
      getReportInfos: function(){
        const app = this;
        axios.get('http://localhost:5000/getReportInfos')
        .then(function (response) {
          console.log(response.data)
          for (let i = 0; i < response.data.length; i++) {
            app.reports.push(response.data[i].name);
            app.reportsIDs.push(response.data[i].id);
          }
        })
        .catch(function (error) {
          console.log(error);
        })
      },
    },
    components: {
      Loader,
    },
    created() {
      this.getReportInfos();
    },
    watch: {
      selectedDays: function(n,o){
        console.log(n,o);
        this.crontab.dayOfWeek = this.getAllIndexes(this.days,n).length == 7 ? '*' : this.getAllIndexes(this.days,n).join();
        this.crontabForHuman[1] = n.length == 7 ? 'Everyday ' :'On ' + n.join(' ,');
      },
      selectedMonth: function(n,o){
        console.log(n,o);
        this.crontab.month = this.getAllIndexes(this.months,n).length == 12 ? '*' : this.getAllIndexes(this.months,n,1).join();
        this.crontabForHuman[2] = n.length == 12 ? 'Every month ' : 'In ' + n.join(' ,');
      },
      time: function(n,o){
        console.log(n,o);
        const splitedTime = n.split(':');
        this.crontab.hour = this.trimFirstZero(splitedTime[0]);
        this.crontab.minute = this.trimFirstZero(splitedTime[1]);
        this.crontabForHuman[0] = 'At ' + n;
      },
      reportName: function(n,o){
        console.log(n,o);
        this.selectedID = this.reportsIDs[this.reports.indexOf(n)];
        console.log(this.selectedID)
      }

    }
  }
</script>
<style scoped>
.controls {
  position: relative;
}
</style>