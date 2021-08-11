<template>
  <div class="text-center">
    <v-dialog
      v-model="$store.getters.loader"
      persistent
      overlay-color="white"
      width="300"
    >
      <v-card
        color="deep-orange darken-3"
        dark
      >
        <v-card-text class="text-center">
          Loading..
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {
    name: "Loader",
    data () {
      return {
      }
    },

    watch: {
      dialog (val) {
        if (!val) return

        setTimeout(() => (this.dialog = false), 4000)
      },
    },
    props: {
      dialog: Boolean,
      overlay: Boolean
    }
  }
</script>


