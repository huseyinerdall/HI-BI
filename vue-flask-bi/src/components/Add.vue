<template>

  <v-row justify="center" @click="addModalClose">

    <v-dialog v-model="$store.getters.addModal" v-if="$store.getters.addModal" max-width="900px" min-height="500px" persistent>
      <v-card>
        <v-tabs
          v-model="tab"
          background-color="transparent"
          height="30"
          grow
        >
          <v-tab
            v-for="(tab) in tabs"
            :key="tab"
          >
            {{ tab }}
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item
            v-for="(tab,n) in tabs"
            :key="tab"
          >
            <v-card flat>
              <v-card-text>
                <p v-show="false">{{ json='options' in $store.getters.editJson ? $store.getters.editJson : json}}</p>
                <template v-if="n == 0">
                  <div class="chart-type mb-5">
                        <div><input type="radio" v-model="json.options.chart.type" value="area" id="area" checked><label for="area">Area</label></div>
                        <div><input type="radio" v-model="json.options.chart.type" value="bar" id="vertical"><label for="vertical">Bar</label></div>
                        <div><input type="radio" v-model="json.options.chart.type" value="line" id="line"><label for="line">Line</label></div>
                        <div><input type="radio" v-model="json.options.chart.type" value="pie" id="pie"><label for="pie">Pie</label></div>
                        <div><input type="radio" v-model="json.options.chart.type" value="radar" id="radar"><label for="radar">Radar</label></div>
                        <div><input type="radio" v-model="json.options.chart.type" value="donut" id="donut"><label for="donut">Donut</label></div>
                      </div>
                      <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      label="Graph name"
                      placeholder="Graph name"
                      outlined
                      dense
                      v-model="json.graph_name"
                      @input="graphID"

                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      label="Graph title"
                      placeholder="Graph title"
                      outlined
                      dense
                      v-model="json.options.title.text"
                    ></v-text-field>
                  </v-col>
                  </v-row>
                  <v-row>
                  <v-col cols="12" sm="12">
                    <v-textarea
                      label="Description"
                      placeholder="Description"
                      dense
                      outlined
                      name="graph_desription"
                      rows="2"
                      v-model="json.graph_desription"
                    ></v-textarea>
                  </v-col>
                  </v-row>
                </template>
                <template v-if="n == 1">
                  <v-row>
                    <v-col col="8">

                      <v-list dense class="pt-0">
                          <v-subheader>TABLES</v-subheader>
                          <v-list-item-group color="primary"
                          class="draggable-list">
                            <v-list-item
                              v-for="(table, i) in tables"
                              :key="i"
                              class="draggable"
                              @drag="dragText"
                            >
                              <v-list-item-icon>
                                <v-icon>demo-icon icon-move-2</v-icon>
                              </v-list-item-icon>
                              <v-list-item-content data-target="table" draggable>
                                <v-list-item-title v-text="table"></v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                          </v-list-item-group>
                        </v-list>

                        <v-list dense class="pt-0">
                          <v-subheader>COLUMN NAMES</v-subheader>
                          <v-list-item-group color="primary"
                          class="draggable-list">
                            <v-list-item
                              v-for="(column, i) in columns"
                              :key="i"
                              class="draggable"
                              @drag="dragText"
                            >
                              <v-list-item-icon>
                                <v-icon>demo-icon icon-move-2</v-icon>
                              </v-list-item-icon>
                              <v-list-item-content data-target="x_axis" draggable>
                                <v-list-item-title v-text="column"></v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                          </v-list-item-group>
                        </v-list>

                        <v-list dense class="pt-0">
                          <v-subheader>COLUMN NAMES</v-subheader>
                          <v-list-item-group color="primary"
                          class="draggable-list">
                            <v-list-item
                              v-for="(column, i) in columns"
                              :key="i"
                              class="draggable"
                              @drag="dragText"
                            >
                              <v-list-item-icon>
                                <v-icon>demo-icon icon-move-2</v-icon>
                              </v-list-item-icon>
                              <v-list-item-content data-target="y_axis" draggable>
                                <v-list-item-title v-text="column"></v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                          </v-list-item-group>
                        </v-list>


                    </v-col>
                    <v-col col="4"
                    class="pt-10">
                    <v-alert type="info" dense style="font-size:14px">
                      Drop table name and column names
                    </v-alert>
                      <v-text-field
                        label="Choose a table and drop here"
                        single-line
                        outlined
                        name="table_name"
                        class="drop"
                        @drop="dropText"
                        v-on:dragover="allowDrop"
                        v-model="json.table_name"
                      ></v-text-field>
                      <v-text-field
                        label="Choose column and drop here"
                        single-line
                        outlined
                        name="x_axis"
                        class="drop"
                        @drop="dropText"
                        v-on:dragover="allowDrop"
                        v-model="json.x_axis"
                      ></v-text-field>
                      <v-text-field
                        label="Choose column and drop here"
                        single-line
                        outlined
                        name="y_axis"
                        @drop="dropText"
                        class="drop"
                        v-on:dragover="allowDrop"
                        v-model="json.y_axis"
                      ></v-text-field>
                    </v-col>
                    
                  </v-row>
                </template>
                <template v-if="n == 2">
                  <v-container>
                    <v-row>
                      <v-col
                      md="3">
                      
                      <v-text-field v-model="json.options.chart.background"
                      class="ma-0 pa-0"
                      outlined dense hide-details
                      :value="json.options.chart.background"
                      label="Background color"
                      placeholder="Background color">
                        <template v-slot:append>
                          <v-menu v-model="menuBack" top nudge-bottom="105" nudge-left="16" :close-on-content-click="false">
                            <template v-slot:activator="{ on }">
                              <div :style="swatchStyleBack" v-on="on" />
                            </template>
                            <v-card>
                              <v-card-text class="pa-0">
                                <v-color-picker v-model="json.options.chart.background" flat />
                              </v-card-text>
                            </v-card>
                          </v-menu>
                        </template>
                      </v-text-field>
                      
                      </v-col>

                      <v-col
                      md="3">
                      
                      <v-text-field v-model="json.options.chart.foreColor"
                      class="ma-0 pa-0"
                      outlined dense hide-details
                      :value="json.options.chart.foreColor"
                      label="Foreground color"
                      placeholder="Foreground color">
                        <template v-slot:append>
                          <v-menu v-model="menuFore" top nudge-bottom="105" nudge-left="16" :close-on-content-click="false">
                            <template v-slot:activator="{ on }">
                              <div :style="swatchStyleFore" v-on="on" />
                            </template>
                            <v-card>
                              <v-card-text class="pa-0">
                                <v-color-picker v-model="json.options.chart.foreColor" flat />
                              </v-card-text>
                            </v-card>
                          </v-menu>
                        </template>
                      </v-text-field>
                      
                      </v-col>
                      <v-col
                      md="3">
                        <v-select
                          :items="fontStyles"
                          label="Font family"
                          dense
                          outlined
                          placeholder="Choose a font family"
                          v-model="json.options.chart.fontFamily"
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-container>
                </template>
                <template v-if="n == 3">
                  <v-container class="mb-0 p-0">
                    <v-row>
                      <v-col
                        cols="12"
                        md="1"
                        class="pt-6 pb-0"
                      >
                      <h4>Legend</h4>
                      </v-col>
                      <v-col
                        cols="12"
                        md="1"
                        class="pb-0"
                      >
                      <v-checkbox value input-value="true" v-model="json.options.legend.show"></v-checkbox>
                      </v-col>
                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-select
                          :items="position"
                          label="Position"
                          placeholder="Position"
                          outlined
                          dense
                          v-model="json.options.legend.position"
                        ></v-select>
                      </v-col>

                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-select
                          :items="fontSizes"
                          label="Font Size"
                          placeholder="Font Size"
                          outlined
                          dense
                          v-model="json.options.legend.fontSize"
                        ></v-select>
                      </v-col>

                      <v-col
                        cols="12"
                        md="4"
                        class="pb-0"
                      >
                        <v-select
                          :items="fontStyles"
                          label="Font Family"
                          placeholder="Font Family"
                          outlined
                          dense
                          v-model="json.options.legend.fontFamily"
                        ></v-select>
                      </v-col>
                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-select
                          :items="fontWeights"
                          label="Font Weight"
                          placeholder="Font Weight"
                          outlined
                          dense
                          v-model="json.options.legend.fontWeight"
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-container>
                  <v-divider style="margin-top:-10px !important;" class="mb-4"></v-divider>
                  <v-container class="mb-0 p-0" style="padding:0 12px;">
                    <v-row>
                      <v-col
                        cols="12"
                        md="1"
                        class="pt-6 pb-0"
                      >
                      <h4>Title</h4>
                      </v-col>
                      <v-col
                        cols="12"
                        md="2"
                      >
                        <v-select
                          :items="aligns"
                          label="Position"
                          placeholder="Position"
                          outlined
                          dense
                          v-model="json.options.title.align"
                        ></v-select>
                      </v-col>

                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-select
                          :items="fontSizes"
                          label="Font Size"
                          placeholder="Font Size"
                          outlined
                          dense
                          v-model="json.options.title.style.fontSize"
                        ></v-select>
                      </v-col>

                      <v-col
                        cols="12"
                        md="4"
                        class="pb-0"
                      >
                        <v-select
                          :items="fontStyles"
                          label="Font Family"
                          placeholder="Font Family"
                          outlined
                          dense
                          v-model="json.options.title.style.fontFamily"
                        ></v-select>
                      </v-col>
                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-select
                          :items="fontWeights"
                          label="Font Weight"
                          placeholder="Font Weight"
                          outlined
                          dense
                          v-model="json.options.title.style.fontWeight"
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-container>
                  <v-divider style="margin-top:-10px !important;" class="mb-4"></v-divider>
                  <v-container class="mb-0 p-0" style="padding:0 12px;">
                    <v-row>
                      <v-col
                        cols="12"
                        md="1"
                        class="pt-6 pb-0"
                      >
                      <h4>Grid</h4>
                      </v-col>
                      <v-col
                        cols="12"
                        md="1"
                        class="pb-0"
                      >
                        <v-checkbox value input-value="true" v-model="json.options.grid.show"></v-checkbox>
                      </v-col>
                      <v-col
                        cols="12"
                        md="3"
                        class="pb-0"
                      >
                      <v-text-field v-model="json.options.grid.borderColor"
                        class="ma-0 pa-0"
                        outlined dense hide-details
                        :value="json.options.grid.borderColor"
                        label="Color"
                        placeholder="Color">
                          <template v-slot:append>
                            <v-menu v-model="menuBorderColor" top nudge-bottom="105" nudge-left="16" :close-on-content-click="false">
                              <template v-slot:activator="{ on }">
                                <div :style="swatchStyleBorder" v-on="on" />
                              </template>
                              <v-card>
                                <v-card-text class="pa-0">
                                  <v-color-picker v-model="json.options.grid.borderColor" flat />
                                </v-card-text>
                              </v-card>
                            </v-menu>
                          </template>
                        </v-text-field>
                      </v-col>

                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-checkbox value input-value="true" v-model="json.options.grid.xaxis.lines.show" label="X axis lines"></v-checkbox>
                      </v-col>

                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-checkbox value input-value="true" v-model="json.options.grid.yaxis.lines.show" label="Y axis lines"></v-checkbox>
                      </v-col>
                      <v-col
                        cols="12"
                        md="2"
                        class="pb-0"
                      >
                        <v-select
                          :items="paddings"
                          label="Padding"
                          placeholder="Padding"
                          outlined
                          dense
                          v-model="json.options.grid.padding"
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-container>

                </template>
              </v-card-text>
            </v-card>
            <div class="d-flex flex-row-reverse">
              <v-btn class="ma-4" color="error" @click="addModalClose">Close</v-btn>
              <v-btn class="ma-4" color="primary" @click="addModalClose" v-if="'options' in $store.getters.editJson">Edit</v-btn>
              <v-btn class="ma-4" color="primary" @click="submitGraph" v-if="n == 3 && !('options' in $store.getters.editJson)">SAVE</v-btn>
            </div>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-dialog>
            

    <v-snackbar
      v-model="noti"
      :timeout="timeout"
      success
    >
      {{ notifytText }}
      <v-btn
        color="blue"
        text
        @click="snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>
  </v-row>
</template>

<script>
const axios = require('axios');
  export default {
    name: 'Add',
    data: () => ({
      open: true,
      menuBack: false,
      menuFore: false,
      menuBorderColor:false,
       tab: null,
       loader: false,
        tabs: [
          'General', 'Dataset', 'Styling', 'Options',
        ],
        text: 'Lorem ipsum dolor sit amet, consectetur adip',
      editable: true,
      graphs:[],
      stepNames: ['General','Dataset','Styling','Options'],
      colorBack: '',
      colorFore: '',
      tables: [],
      columns: [],
      fontStyles: ['Georgia, serif','Arial, Helvetica','"Times New Roman", Times, serif','Verdana, Geneva, sans-serif','Courier New','Lucida Console'],
      position: ['bottom','top', 'right', 'left'],
      fontSizes: ['14px','15px', '16px', '17px','18px','20px','22px'],
      fontWeights: ['400','500', '600', '700','800','900'],
      aligns: ['left','center','right'],
      paddings: ['2px','4px','6px','8px','10px','12px'],
      modal2: false,
      currentDrag: '',
      currentGraph: '',
      uid: -1,
      timeout: 3000,
      noti: false,
      notifytText: '',
      json: {
        options: {
          chart: {
            type: "bar",
            id: '',
            background: "#FFFFFF",
            foreColor: '#373d3f',
            fontFamily: "Arial, Helvetica",
            toolbar: { show: false },
            selection: { enabled: false },
            zoom: { enabled: false },
          },
          color: '',
          legend: {
            show: true,
            position: "bottom",
            fontSize: "14px",
            fontFamily: 'Arial, Helvetica',
            fontWeight: 400
          },
          title: {
            text: '',
            align: 'left',
            style: {
              fontSize:  '14px',
              fontWeight:  400,
              fontFamily: 'Arial, Helvetica',
              color:  '#000000'
            },
            chartOptions: {
              labels: ['Apple', 'Mango', 'Orange', 'Watermelon']
            }
          },
          grid: {
            show: true,
            borderColor: '#FFFFFF',
            /* padding: {}, */
            xaxis: {
              categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
                lines: {
                    show: false
                }
            },   
            yaxis: {
                lines: {
                  categories: [30, 40, 45, 50, 49, 60, 70, 91],
                    show: false
                }
              }, 
            }
          },
          series: [{
            data: [30, 40, 45, 50, 49, 60, 70, 80]
          }],
          coords:{x:0,y:0,w:400,h:300},
          graph_name: "Graph name",
          graph_desription: "Graph desription",
          x_axis: '',
          y_axis: '',
          table_name:'',
      },
    }),
    methods: {
      addModalClose: function(){
        this.$store.commit('change', false);
      },
      tableNames() {
        const app = this;
        axios.get('http://localhost:5000/tableNames')
        .then(function (response) {
          console.log(response.data);
          app.tables = response.data;
        })
        .catch(function (error) {
          console.log(error);
        })
      },
      dragText(e) {
        this.currentDrag = e.target.dataset.target;
        this.dragValue = e.target.innerText;
      },
      dropText(e) {
        const app = this;
        e.target.parentElement.parentElement.parentElement.parentElement.classList.remove('v-input--is-focused');
        if(this.currentDrag == 'table' && e.target.name == 'table_name'){
          this.json.table_name = this.dragValue;
          axios.post('http://localhost:5000/columnNames', {
            table: this.dragValue
          })
          .then(function (response) {
            app.columns = response.data;
          })
          .catch(function (error) {
            console.log(error);
          });
        }else if(this.currentDrag == e.target.name ){
          this.json[e.target.name] = this.dragValue;
        }
      },
      toKebapCase(str){
        return str.replace(/([a-z])([A-Z])/g, "$1-$2")
             .replace(/\s+/g, '-')
             .toLowerCase();
      },
      graphID(e) {
        if(e != ''){
          this.json.options.chart.id = this.toKebapCase(e);
        }
      },
      allowDrop:function(e) {
        e.target.parentElement.parentElement.parentElement.parentElement.classList.add('v-input--is-focused');
        console.log(e.target.parentElement.parentElement)
        e.preventDefault();
      },
      success: function(msg){
        this.noti = true;
        this.notifytText = msg;
      },
      submitGraph: function() {
        this.json.options.chart.id = 'chart_'+Math.random().toString(32).substring(2)
        this.$store.commit('listChange',JSON.stringify(this.json));
        this.graphs = this.$store.getters.graphs;
        this.graphs.push(JSON.parse(this.$store.getters.graphList));
        this.$store.commit('changeGraphList',this.graphs);
        const allGraphDataStr = (this.$store.getters.graphList);
        console.log(allGraphDataStr)
        const app = this;
          axios.post('http://localhost:5000/createReport', {
            graph: allGraphDataStr,
            id: this.$route.name == 'New' ? this.uid : this.$route.params.id
          })
          .then(function (response) {
            app.$store.commit('change', false)
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
      },
      editMod: function() {
        if('options' in this.$store.getters.editJson){
          this.json = this.$store.getters.editJson;
        }
      }
    },
    computed: {
      swatchStyleBack() {
        const colorBack = this.json.options.chart.background
        return {
          backgroundColor: colorBack,
          cursor: 'pointer',
          height: '30px',
          width: '30px',
          marginTop: '-3px',
          transition: 'border-radius 200ms ease-in-out',
          borderWidth: '1px',
          borderColor: '#000',
          borderStyle: 'dashed',
          borderRadius: '4px',
        }
      },
      swatchStyleFore() {
        const colorFore = this.json.options.chart.foreColor
        return {
          backgroundColor: colorFore,
          cursor: 'pointer',
          height: '30px',
          width: '30px',
          marginTop: '-3px',
          transition: 'border-radius 200ms ease-in-out',
          borderWidth: '1px',
          borderColor: '#000',
          borderStyle: 'dashed',
          borderRadius: '4px',
        }
      },
      swatchStyleBorder() {
        const colorFore = this.json.options.grid.borderColor
        return {
          backgroundColor: colorFore,
          cursor: 'pointer',
          height: '30px',
          width: '30px',
          marginTop: '-3px',
          transition: 'border-radius 200ms ease-in-out',
          borderWidth: '1px',
          borderColor: '#000',
          borderStyle: 'dashed',
          borderRadius: '4px',
        }
      },
    },
    created() {
      this.tableNames();
      const app = this;
      axios.get('http://localhost:5000/uniqueID')
        .then(function (response) {
          app.uid = response.data;
        })
        .catch(function (error) {
          console.log(error);
      });
    },
    filters: {
      json(value) {
        return JSON.stringify(value)
      }
    },
  }
</script>

<style scoped>
  .chart-type>div:nth-child(1)>label{background-image: url('../assets/img/area.png');}
  .chart-type>div:nth-child(2)>label{background-image: url('../assets/img/vertical.png');}
  .chart-type>div:nth-child(3)>label{background-image: url('../assets/img/line.png');}
  .chart-type>div:nth-child(4)>label{background-image: url('../assets/img/pie.png');}
  .chart-type>div:nth-child(5)>label{background-image: url('../assets/img/radar.png');}
  .chart-type>div:nth-child(6)>label{background-image: url('../assets/img/donut.png');}
  .chart-type{
    display: flex;
    margin: 10px 0 0 0;
    flex-direction: row;
}
.chart-type>div{
    width:calc(100%/6);
    height: 100px;
}
.chart-type>div>label{
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
.chart-type input[type="radio"]{
    display:none;
}
.chart-type input[type="radio"]:checked+label{
    border:4px solid rgb(216, 67, 21);
}
.drop fieldset{
  border-style: dotted !important;
}
.drop{
  padding: 0 30px;
}
.draggable-list{
  height: 120px;
  border:2px solid #1976d2;
  overflow-y: auto;
}
.v-color-picker{
  box-shadow: none;
}
.v-input--selection-controls{
  margin-top: 5px;
}
</style>