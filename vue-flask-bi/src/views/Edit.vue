<template>
  <div class="home" id="graphs" style="width:100%;height:100%" >
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
      <v-btn text small>
        <v-icon>demo-icon icon-cog</v-icon>Settings
      </v-btn>
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
        :style="{width:(graph.coords.w-2)+'px' ,height:(graph.coords.h-3)+'px'}"
        :series="graph.options.chart.type == 'donut' || graph.options.chart.type == 'pie' ? graph.series[0]['data'] : graph.series"></apexchart>
      </vue-draggable-resizable>
      <template v-if="$store.getters.texts.length">
        <vue-draggable-resizable
        v-for="(html,i) in $store.getters.texts"
        :resizable="true"
        :parent="true"
        :x="html.coords.x" :y="html.coords.y" :w="html.coords.w" :h="html.coords.h"
        :hibi-report-style="'top:'+html.coords.y+'px;left:'+html.coords.x+'px;position:absolute;'"
        @resizing="onResizeHTML" @dragging="onDragHTML" @activated="onActivatedHTML(i)" @deactivated="onDeactivatedHTML(i)"
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
export default {
  name: "New",
  data: function() {
    return {
      add: false,
      prev:0,
      prevHTML:0,
      toolType:'',
      tools:false,
      x:0,
      y:0,
      graphs: [],
      contextMenuStatu: false,
      currentIndex: -1,
      currentHTMLIndex: -1,
      active: false,
      toggle_exclusive: undefined,
      htmls: [],
      toolsL: 0,
      toolsT: 0,
      confirm: false,
      confirmO: {},
      editJson: {},
      reportname: '',
    }
  }, 
  components: {
    Loader,
    Add,
    AddText,
    AddImage
  },
  methods: {
    addModalOpen: function(){
      this.$store.commit('editJson', {});
      this.$store.commit('change', true);
    },
    addTextModalOpen: function(){
      this.$store.commit('editJson', {});
      this.$store.commit('changeText', true);
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

    getReport: function(){
      const app = this;
      axios.post('http://localhost:5000/getReport', {
        id: this.$route.params.id
      })
      .then(function (response) {/* 
        app.$store.commit('changeGraphList',JSON.parse(response.data)); */
        console.log(response.data)
        app.$store.commit('changeGraphList',JSON.parse(response.data.graphs));
        app.$store.commit('changeHTMLList',JSON.parse(response.data.htmls));
        app.reportname = response.data.name;
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    saveReport: function(){
      /* const app = this; */
      axios.post('http://localhost:5000/saveReport', {
        id: this.$route.params.id,
        graphList: this.$store.getters.graphs,
        htmlList: this.$store.getters.texts
      })
      .then(function (response) {
        console.log(response)
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
        a.dispatchEvent(new MouseEvent('click'));
      })
      .catch(function (error) {
        console.log(error);
      });
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
    contextMenu: function(e) {
      console.log(e);
    },
  },
  created() {
    this.getReport(); 
  },
  beforeCreate() {

  },
  mounted() {
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
