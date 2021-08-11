<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <Loader></Loader>
  </div>
</template>

<script>
// @ is an alias to /src
import Loader from '@/components/Loader'

export default {
  name: "Home",
  methods: {
    loaderStop: function() {
      setTimeout(()=>{
        this.$store.commit('changeLoader', false);
      },1500)
    },
  },
  mounted() {
  },
  components: {
    Loader,
  }
};
</script>
