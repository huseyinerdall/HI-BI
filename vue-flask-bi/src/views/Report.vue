<template>
  <div class="reports" justify="center">
    <v-sheet
      elevation="6"
      class="mx-auto mt-6 mb-6"
      height="27cm"
      width="21cm"
    >
      <vue-draggable-resizable
      v-for="graph in $store.getters.graphs"
      :resizable="false" :draggable="false" :parent="true"
      :x="graph.coords.x*0.6" :y="graph.coords.y*0.6" :w="graph.coords.w*0.6" :h="graph.coords.h*0.6"
      :key="graph.options.chart.id">
        <apexchart :type="graph.options.chart.type" :options="graph.options"
        :style="{width:(graph.coords.w-2)*0.6+'px' ,height:(graph.coords.h-2)*0.6+'px'}"
        :series="graph.options.chart.type == 'donut' || graph.options.chart.type == 'pie' ? graph.series[0]['data'] : graph.series"></apexchart>
      </vue-draggable-resizable>

      <template v-if="$store.getters.texts.length">
        <vue-draggable-resizable
        v-for="(html) in $store.getters.texts"
        :resizable="false" :draggable="false" :parent="true"
        :x="html.coords.x*0.6" :y="html.coords.y*0.6" :w="html.coords.w*0.6" :h="html.coords.h*0.6"
        :key="html.id">
          <div v-html="html.html" class="html"
        :style="{width:((html.coords.w)-2)*0.6+'px' ,height:(html.coords.h)*0.6+'px'}"></div>
        </vue-draggable-resizable>
      </template>
    </v-sheet>
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
      graphs:[]
    }
  },
  methods: {
    getReport: function(){
      const app = this;
      axios.post('http://localhost:5000/getReport', {
        id: this.$route.params.id
      })
      .then(function (response) {
        app.$store.commit('changeGraphList',JSON.parse(response.data.graphs));
        app.$store.commit('changeHTMLList',JSON.parse(response.data.htmls));
      })
      .catch(function (error) {
        console.log(error);
      });
    },
  },
  created() {
    this.getReport();
  },
  mounted() {
  },
  components: {
    Loader,
  }
};
</script>
<style scoped>
.vdr{
  border:none;
}
</style>