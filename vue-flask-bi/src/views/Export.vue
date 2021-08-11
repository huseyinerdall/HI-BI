<template>
  <div class="home" id="graphs" style="width:100%;height:100%" >
    <div id="report-output" style="min-width:100vw;min-height:100vh;">
      <vue-draggable-resizable
      v-for="(graph) in $store.getters.graphs"
      :parent="true" :draggable="false"
      :x="graph.coords.x" :y="graph.coords.y" :w="graph.coords.w" :h="graph.coords.h"
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
        v-for="(html) in $store.getters.texts"
        :parent="true" :draggable="false"
        :x="html.coords.x" :y="html.coords.y" :w="html.coords.w" :h="html.coords.h"
        :hibi-report-style="'top:'+html.coords.y+'px;left:'+html.coords.x+'px;position:absolute;'"
        :key="html.id">
          <div v-html="html.html" class="html"
        :style="{width:(html.coords.w)-2+'px' ,height:(html.coords.h)+'px'}"></div>
        </vue-draggable-resizable>
      </template>
    </div>
  </div>
</template>

<script>
const axios = require('axios');
export default {
  name: "New",
  data: function() {
    return {
      x:0,
      y:0,
      graphs: [],
      currentIndex: -1,
      currentHTMLIndex: -1,
      active: false,
      htmls: [],
      reportname: '',
    }
  },
  methods: {
    getReport: function(){
      const app = this;
      axios.post('http://localhost:5000/getReport', {
        id: this.$route.params.id
      })
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
    sendHTML: function(){
      //const allEl = document.getElementsByClassName('.hibi-one-graph');
      const html = document.getElementById('report-output').outerHTML;
      console.log(html)
      //const html = document.getElementsByClassName('v-content__wrap')[0].innerHTML;
      axios.post('http://localhost:5000/getHTML', {
        aaaa: html 
      })
      .then(function (response) {
        console.log('alındı',response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
  },
  created() {
    
    const app = this;
    new Promise(function(res,rej){
        console.log(rej)
        app.getReport();
        
        setTimeout(()=>{
            res(1);
        },1000)
    })
    .then(function(result){
        console.log(result);
        app.sendHTML();
    })
  },
  mounted() {
    
  }
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
</style>
