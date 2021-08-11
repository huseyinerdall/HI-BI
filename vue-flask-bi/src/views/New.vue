<template>
  <div class="home" id="graphs" style="width:100%;height:100%">
    <v-toolbar dense height="34">
      <router-link to="/reports" tag="span">
        <v-btn icon>
          <v-icon>demo-icon icon-left-bold</v-icon>
        </v-btn>
      </router-link>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" text small>New</v-btn>
        </template>
        <v-list class="pa-0">
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="addModalOpen"><v-icon>demo-icon icon-chart-bar-4</v-icon>Add graph</v-list-item-title>
          </v-list-item>
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="addTextModalOpen"><v-icon>demo-icon icon-doc-text</v-icon>Add text</v-list-item-title>
          </v-list-item>
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="addImageModalOpen"><v-icon>demo-icon icon-file-image</v-icon>Add image</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" text small><v-icon>demo-icon icon-export-1</v-icon>Export</v-btn>
        </template>
        <v-list class="pa-0">
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="sendHTML"><v-icon>demo-icon icon-file-pdf</v-icon>Export as PDF</v-list-item-title>
          </v-list-item>
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="addTextModalOpen"><v-icon>demo-icon icon-doc-text</v-icon>Export as PDF(zipped)</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" text small><v-icon>demo-icon icon-share-1</v-icon>Share</v-btn>
        </template>
        <v-list class="pa-0">
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="sendHTML"><v-icon>demo-icon icon-email</v-icon>Share via email</v-list-item-title>
          </v-list-item>
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="addTextModalOpen"><v-icon>demo-icon  icon-whatsapp</v-icon>Share via whatsapp</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" text small><v-icon>demo-icon icon-cog</v-icon>Settings</v-btn>
        </template>
        <v-list class="pa-0">
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="isRulerOpen = !isRulerOpen"><v-icon>demo-icon icon-email</v-icon>Open Ruler</v-list-item-title>

          </v-list-item>
          <v-list-item style="cursor:pointer" dense>
            <v-list-item-title v-on:click="addTextModalOpen"><v-icon>demo-icon  icon-whatsapp</v-icon>Share via whatsapp</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn text small @click="saveReport">
        <v-icon>demo-icon icon-ok-1</v-icon>Save
      </v-btn>
      <v-btn text small>
        <v-icon>demo-icon icon-help</v-icon>Help
      </v-btn>
      <v-spacer></v-spacer>
      <v-chip
        class="ma-2"
        color="orange darken-3"
        outlined
      >
        <v-icon left>demo-icon icon-ok-6</v-icon>
        Current Report : <span>{{reportname}}</span>
      </v-chip>
    </v-toolbar>
    <div id="report-output" style="min-width:100vw;min-height:100vh;"
     @contextmenu.prevent="contextMenu($event)">
      <vue-draggable-resizable
      v-for="(graph,i) in $store.getters.graphs"
      :resizable="true"
      :parent="true"
      :x="graph.coords.x" :y="graph.coords.y" :w="graph.coords.w" :h="graph.coords.h"
      @resizing="onResize" @dragging="onDrag" @activated="onActivated(i)" @deactivated="onDeactivated(i)"
      :data-id="graph.options.chart.id"
      :key="graph.options.chart.id"
      class="hibi-one-graph"
      :hibi-report-style="'top:'+graph.coords.y+'px;left:'+graph.coords.x+'px;position:absolute;'"
      :style="{width:(graph.coords.w)+'px' ,height:(graph.coords.h)+'px'}">
        <apexchart width="100%" height="100%" :type="graph.options.chart.type" :options="graph.options"
        :style="{width:(graph.coords.w-2)+'px' ,height:(graph.coords.h-2)+'px'}"
        :series="graph.options.chart.type == 'donut' || graph.options.chart.type == 'pie' ? graph.series[0]['data'] : graph.series"></apexchart>
      </vue-draggable-resizable>

      <template v-if="$store.getters.texts.length">
        <vue-draggable-resizable
        v-for="(html,i) in $store.getters.texts"
        :resizable="true"
        :parent="true"
        :x="html.coords.x" :y="html.coords.y" :w="html.coords.w" :h="html.coords.h"
        :hibi-report-style="'top:'+html.coords.y+'px;left:'+html.coords.x+'px;position:absolute;'"
        @resizing="onResizeHTML" @dragging="onDragHTML" @activated="onActivatedHTML(i)"
        :key="html.id">
          <div v-html="html.html" class="html"
        :style="{width:(html.coords.w)-2+'px' ,height:(html.coords.h)+'px'}"></div>
        </vue-draggable-resizable>
      </template>
    </div>
    <v-btn-toggle
          v-model="toggle_exclusive"
          v-if="active"
          style="position:absolute;transition:none;"
          :style="{top:y+'px',left:x+'px'}"
          mandatory
        >
          <v-btn>
            <v-icon>demo-icon icon-edit</v-icon>
          </v-btn>
          <v-btn>
            <v-icon>demo-icon icon-trash-empty</v-icon>
          </v-btn>
        </v-btn-toggle>
        <v-list>
        <v-list-item v-if="contextMenuStatu">
          <v-list-item-title @click="deleteGraph">Delete</v-list-item-title>
          <v-list-item-title @click="editGraph">Edit</v-list-item-title>
        </v-list-item>
      </v-list>

    <v-row justify="center">
      <v-dialog v-model="reportNameDialog" persistent max-width="400" v-if="!$store.getters.loader">
        <v-card>
          <v-card-title class="headline">Report Name?</v-card-title>
          <v-card-text>You should type a unique name to seperate other reports</v-card-text>
          <v-col cols="11" class="ml-2">
            <v-text-field label="Report name" placeholder="Report name" outlined dense v-model="reportname" :value="'report_'+uid"></v-text-field>
          </v-col>
          <v-card-actions>
            <v-spacer></v-spacer>
            <router-link to="/reports" tag="span">
              <v-btn color="green darken-1" text @click="reportNameDialog = false">Cancel</v-btn>
            </router-link>
            <v-btn color="green darken-1" text @click="setReportName">OK</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>

    <v-btn-toggle
      v-model="toggle_exclusive"
      v-if="active"
      style="position:absolute;transition:none;"
      :style="{top:y+'px',left:x+'px'}"
      mandatory
      >
      <v-btn>
        <v-icon>demo-icon icon-edit</v-icon>
      </v-btn>
      <v-btn>
        <v-icon>demo-icon icon-trash-empty</v-icon>
      </v-btn>
    </v-btn-toggle>

      <div id="toolsMenu"
      v-if="tools"
      :style="{top:toolsT+'px' ,left:toolsL+'px'}">
        <v-row>
          <v-btn-toggle v-model="toggle_exclusive" dense>
          <v-btn small @click="confirmF({title:'Delete operation?',text:'Are you sure delete this element?',callback:removeItem})">
            <v-icon>demo-icon icon-trash-4</v-icon>
          </v-btn>

          <v-btn small @click="editItem">
            <v-icon>demo-icon icon-edit-2</v-icon>
          </v-btn>
        </v-btn-toggle>
        </v-row>
      </div>

    <v-row justify="center">
      <v-dialog v-model="confirm" max-width="290">
        <v-card>
          <v-card-title class="headline">{{confirmO.title}}</v-card-title>
          <v-card-text>{{confirmO.text}}</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="confirm = false">Cancel</v-btn>
            <v-btn color="green darken-1" text @click="confirmO.callback">Agree</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>

    <Ruler v-if="isRulerOpen"></Ruler>
    <Loader></Loader>
    <Add></Add>
    <AddText></AddText>
    <AddImage></AddImage>
  </div>
</template>

<script>
const axios = require('axios');
import Loader from '@/components/Loader'
import Add from '@/components/Add'
import AddText from '@/components/AddText'
import AddImage from '@/components/AddImage'
import Ruler from '@/components/Ruler'
export default {
  name: "New",
  data: function() {
    return {
      loader: true,
      active: false,
      contextMenuStatu: false,
      htmls: [],
      text: {
        html: '<q style="color:red">aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</q>',
        id:'',
        coords:{x:0,y:0,w:300,h:200},
      },
      uid: -1,
      timeout: 3000,
      noti: false,
      notifytText: '',
      currentIndex: -1,
      currentHTMLIndex: -1,
      reportNameDialog: false,
      reportname: '',
      isRulerOpen: false,
      toolsL: 0,
      toolsT: 0,
      confirm: false,
      confirmO: {},
      editJson: {},
      prev:0,
      prevHTML:0,
      toolType:'',
      tools:false,
      toggle_exclusive: undefined,
      reportNameError: '',
    }
  }, 
  components: {
    Loader,
    Add,
    AddText,
    AddImage,
    Ruler,
  },
  methods: {
    addModalOpen: function(){
      this.$store.commit('editJson', {});
      this.$store.commit('change', true)
    },
    addTextModalOpen: function(){
      this.$store.commit('editJson', {});
      this.$store.commit('changeText', true)
    },
    addImageModalOpen: function(){
      this.$store.commit('changeImage', true);
    },
    onDrag(left, top) {
      let newPosition = {}
      this.toolsL = this.$store.getters.graphs[this.currentIndex].coords.x + this.$store.getters.graphs[this.currentIndex].coords.w - 90;
      this.toolsT = this.$store.getters.graphs[this.currentIndex].coords.y;

      newPosition.x = left
      newPosition.y = top
      newPosition.i = this.currentIndex
      this.$store.commit('changePositionInDrag',newPosition);
    },
    onResize(left, top, width=0, height=0) {
      let newPosition = {}

      this.toolsL = this.$store.getters.graphs[this.currentIndex].coords.x + this.$store.getters.graphs[this.currentIndex].coords.w - 90;
      this.toolsT = this.$store.getters.graphs[this.currentIndex].coords.y;

      newPosition.x = left;
      newPosition.y = top;
      newPosition.w = width;
      newPosition.h = height;
      newPosition.i = this.currentIndex;
      this.$store.commit('changePosition',newPosition);
    },
    onActivated (i) {
      this.currentIndex = i;
      this.toolType = 'graph';
      this.tools = true;
      this.toolsL = this.$store.getters.graphs[i].coords.x + this.$store.getters.graphs[i].coords.w - 90;
      this.toolsT = this.$store.getters.graphs[i].coords.y;
    },
    onDeactivated(i) {
      console.log('deactivated',i);
      this.prev = this.currentIndex;
      this.currentIndex = -1;
    },
    onDragHTML(left, top) {
      let newPosition = {}

      this.toolsL = this.$store.getters.texts[this.currentHTMLIndex].coords.x + this.$store.getters.texts[this.currentHTMLIndex].coords.w - 90;
      this.toolsT = this.$store.getters.texts[this.currentHTMLIndex].coords.y;

      newPosition.x = left
      newPosition.y = top
      newPosition.i = this.currentHTMLIndex
      this.$store.commit('changeHTMLPositionInDrag',newPosition);
    },
    onResizeHTML(left, top, width=0, height=0) {
      let newPosition = {}

      this.toolsL = this.$store.getters.texts[this.currentHTMLIndex].coords.x + this.$store.getters.texts[this.currentHTMLIndex].coords.w - 90;
      this.toolsT = this.$store.getters.texts[this.currentHTMLIndex].coords.y;

      newPosition.x = left
      newPosition.y = top
      newPosition.w = width
      newPosition.h = height
      newPosition.i = this.currentHTMLIndex
      this.$store.commit('changeHTMLPosition',newPosition);
    },
    onActivatedHTML(i) {
      this.tools = true;
      this.currentHTMLIndex = i;
      this.toolType = 'html';
      this.toolsL = this.$store.getters.texts[this.currentHTMLIndex].coords.x + this.$store.getters.texts[this.currentHTMLIndex].coords.w - 90;
      this.toolsT = this.$store.getters.texts[this.currentHTMLIndex].coords.y;
    },
    onDeactivatedHTML(i) {
      console.log('deactivated',i);
      this.prevHTML = this.currentHTMLIndex;
      this.currentIndex = -1;
    },
    success: function(msg) {
      this.noti = true;
      this.notifytText = msg;
    },
    saveReport: function(){
      const app = this;
      axios.post('http://localhost:5000/saveReport', {
        id: this.uid,
        graphList: this.$store.getters.graphs,
        htmlList: this.$store.getters.texts,
        name: app.reportname,
      })
      .then(function (response) {
        app.success(response.data);
        app.$router.push({path:`/edit/${app.uid}`})
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    sendHTML: function(){
      //const allEl = document.getElementsByClassName('.hibi-one-graph');
      const html = document.getElementById('report-output').outerHTML;
      //const html = document.getElementsByClassName('v-content__wrap')[0].innerHTML;
      console.log(html)
      axios.post('http://localhost:5000/getHTML', {
        aaaa: html 
      })
      .then(function (response) {
        console.log('alındı',response);
        const a = document.createElement('a');
        a.href = 'http://localhost:5000/reports/report.pdf';
        a.download = 'file.pdf';
        a.target = 'blank';
        a.dispatchEvent(new MouseEvent('click'));
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    setReportName: function(){
      if(this.reportname == ''){
        this.reportNameError = 'You have to enter a report name';
        return;
      }
      const app = this;
      axios.get('http://localhost:5000/getReportInfos')
      .then(function (response) {
        let reports = [];
        console.log(response.data)
        for (let i = 0; i < response.data.length; i++) {
          reports.push(response.data[i]['name']);
        }
        console.log(reports);
        if(reports.indexOf(app.reportname) > -1){
          console.log(reports.indexOf(app.reportname) > -1);
          return;
        }
      })
      .catch(function (error) {
        console.log(error);
      })
      this.$cookies.set('report_name',this.reportname);
      this.reportNameDialog = false;
    },
    contextMenu: function(e) {
      console.log(e.target.tagName == 'svg');
      console.log(e.clientX,e.clientY)
    },
    confirmF: function(options){
      this.confirmO = options;
      this.confirm = true;
    },
    removeItem: function() {
        if(this.toolType === 'graph'){
          const i = this.prev;
          const temp = this.$store.getters.graphs;
          temp.splice(i,1);
          this.$store.commit('changeGraphList',temp);
        }else if(this.toolType === 'html'){
          const i = this.prevHTML;
          const temp = this.$store.getters.texts;
          temp.splice(i,1);
          this.$store.commit('changeHTMLList',temp);
        }
      this.tools = false;
      this.confirm = false;
    },
    editItem: function() {
        if(this.toolType === 'graph'){
          const i = this.prev;
          const temp = this.$store.getters.graphs;
          this.editJson = temp[i];
          this.addModalOpen();
          this.$store.commit('editJson', this.editJson);
        }else if(this.toolType === 'html'){
          const i = this.prevHTML;
          const temp = this.$store.getters.texts;
          this.editJson = temp[i];
          this.addTextModalOpen();
          this.$store.commit('editJson', this.editJson);
        }
      this.tools = false;
    },
    keyShortcuts: function(e) {
      switch(e.key){
        case 'Delete':
          if(document.querySelector('.vdr.active')){
            let i = 0;
            const removeId = document.querySelector('.vdr.active').dataset.id;
            if(removeId.indexOf('text_')>-1){
              let temp = this.$store.getters.htmls;
              while(temp[i].id!=removeId){
                i++;
              }
              temp.splice(i,1);
              this.$store.commit('changeHTMLList',temp);
              const allHTMLDataStr = (this.$store.getters.htmlList);
              //const app = this;
                axios.post('http://localhost:5000/createHTML', {
                  html: allHTMLDataStr,
                  id: this.$route.name == 'New' ? this.uid : this.$route.params.id
                })
                .then(function () {
                  //app.success(response.data);
                  axios.get('http://localhost:5000/sendHTMLList')
                  .then(function (response) {
                    console.log(response.data);
                  })
                  .catch(function (error) {
                    console.log(error);
                  })
                })
                .catch(function (error) {
                  console.log(error);
                });
            }else{
              let temp = this.$store.getters.graphs;
              while(temp[i].options.chart.id!=removeId){
                i++;
              }
              temp.splice(i,1);
              this.$store.commit('changeGraphList',temp);
              const allGraphDataStr = (this.$store.getters.graphList);
              const app = this;
                axios.post('http://localhost:5000/createReport', {
                  graph: allGraphDataStr,
                  id: this.$route.name == 'New' ? this.uid : this.$route.params.id
                })
                .then(function (response) {
                  app.success(response.data);
                  axios.get('http://localhost:5000/sendGraphList')
                  .then(function (response) {
                    console.log(response.data);
                  })
                  .catch(function (error) {
                    console.log(error);
                  })
                })
                .catch(function (error) {
                  console.log(error);
                });
            }
            
          }
        break;
        default:
          console.log(e.key)
      }
      
    }
  },
  created() {
      const app = this;
      this.reportNameDialog = !!String(this.$cookies.get('report_name')).length;
      this.$store.commit('changeGraphList',[]);
      this.$store.commit('changeHTMLList',[]);
      this.reportname = this.$cookies.get('report_name');
      axios.get('http://localhost:5000/uniqueID')
        .then(function (response) {
          console.log(response.data)
          app.uid = response.data;
        })
        .catch(function (error) {
          console.log(error);
      });
      console.log(this.$store.getters.graphs);
      window.addEventListener('keypress', this.keyShortcuts);
      this.$cookies.remove('report_name');
  },
  beforeCreate() {
  },
  mounted() {
  },
  destroyed() {
    window.removeEventListener('keypress', this.keyShortcuts);
  },
};
</script>

<style>
.vdr{
  border-style: dotted;
  /* border-color:#fff; */
}
.vdr.active{
  border-color:black;
  z-index: 9999 !important;
}
.handle{
  box-sizing: border-box;
    background: #4af;
    border: 1px solid #fff;
    border-radius: 3px;
    z-index: 10;
}
.html-content{
  overflow-wrap: anywhere;
}
.html-content img,
.html-content *{
  width: 100%;
  height: 100%;
}
.ql-align-center{
  text-align: center;
}
.html{
  overflow-wrap: anywhere;
  overflow: hidden;
  position: relative;
}
.html img{
  width: 100%;
  max-height: 100%;
}
.html>*{
  width: 100%;
  max-height: 100%;
}
.v-list-item__title i{
  font-size: 16px;
}
#toolsMenu{
  position: absolute;
}
</style>