<template>
  <v-row class="pa-12" direction="column">
    <v-switch v-model="switch1" flat :label="`Switch 1: ${switch1.toString()}`"></v-switch>
    <v-switch v-model="switch2" flat :label="`Switch 2: ${switch2.toString()}`"></v-switch>
  </v-row>
</template>

<script>
export default {
  name: "Styling",
  data() {
    return {
      switch1: true,
      switch2: false,
    }
  },
  props: {
  }
};
</script>
