<template>
  <v-row>
    <v-col cols="11" sm="5">
      <v-dialog
        ref="dialog"
        v-model="modal2"
        :return-value.sync="color"
        width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            v-model="$data.color"
            label="Picker in dialog"
            prepend-icon="demo-icon icon-brush"
            readonly
            v-on="on"
          ></v-text-field>
        </template>
        
        <v-color-picker
          v-if="modal2"
          v-model="color"
        >
        </v-color-picker>
        <v-btn text color="primary" @click="modal2 = false">Cancel</v-btn>
        <v-btn text color="primary" @click="$refs.dialog.save(color)">OK</v-btn>
      </v-dialog>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "Styling",
  data() {
    return {
      color: '',
      modal2: false,
    }
  },
  props: {
  }
};
</script>
