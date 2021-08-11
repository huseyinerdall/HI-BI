<template>
<div>

    <div class="chart-type mb-5">
                    <div><input type="radio" name="chart_type" v-model="chart_type" value="area" id="area"><label for="area">Area</label></div>
                    <div><input type="radio" name="chart_type" v-model="chart_type" value="horizantal" id="horizantal"><label for="horizantal">Horizantal</label></div>
                    <div><input type="radio" name="chart_type" v-model="chart_type" value="vertical" id="vertical"><label for="vertical">Vertical</label></div>
                    <div><input type="radio" name="chart_type" v-model="chart_type" value="line" id="line"><label for="line">Line</label></div>
                    <div><input type="radio" name="chart_type" v-model="chart_type" value="pie" id="pie"><label for="pie">Pie</label></div>
                    <div><input type="radio" name="chart_type" v-model="chart_type" value="stack" id="stack"><label for="stack">Stack</label></div>
                  </div>
  <v-col cols="12" sm="6">
          <v-text-field
            label="Graph name"
            single-line
            outlined
            name="graph_name"
            v-model="graph_name"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="12">
          <v-textarea
            label="Description"
            single-line
            outlined
            name="graph_desription"
            v-model="graph_desription"
          ></v-textarea>
        </v-col>
        {{$data | json}}
</div>
</template>

<script>
export default {
  name: "Styling",
  data() {
    return {
      chart_type: "area",
      graph_name: "Graph name",
      graph_desription: "Graph desription",
    }
  },
  props: {
  }
};
</script>

<style scoped>
  .chart-type>div:nth-child(1)>label{background-image: url('../assets/img/area.png');}
  .chart-type>div:nth-child(2)>label{background-image: url('../assets/img/horizantal.png');}
  .chart-type>div:nth-child(3)>label{background-image: url('../assets/img/vertical.png');}
  .chart-type>div:nth-child(4)>label{background-image: url('../assets/img/line.png');}
  .chart-type>div:nth-child(5)>label{background-image: url('../assets/img/pie.png');}
  .chart-type>div:nth-child(6)>label{background-image: url('../assets/img/area.png');}
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
</style>