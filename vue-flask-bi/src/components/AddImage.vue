<template>
<v-row justify="center" @click="addImageModalClose">
    
    <v-dialog v-model="$store.getters.addImageModal" v-if="$store.getters.addImageModal" max-width="900px" min-height="400px" persistent>
        <v-card class="pt-20">
            <v-card-text class="pt-20">
              
              <v-row class="pt-6">
                <v-col col="6">
                  <v-file-input
                    v-model="files"
                    color="primary"
                    counter
                    label="File input"
                    placeholder="Select image"
                    prepend-icon="demo-icon icon-upload "
                    outlined
                    :show-size="1000"
                    @change="uploadImage"
                    id="uploadInput"
                    dense
                  >
                    <template v-slot:selection="{ index, text }">
                      <v-chip
                        v-if="index < 2"
                        color="primary"
                        dark
                        label
                        small
                      >
                        {{ text }}
                      </v-chip>

                      <span
                        v-else-if="index === 2"
                        class="overline grey--text text--darken-3 mx-2"
                      >
                        +{{ files.length - 2 }} File(s)
                      </span>
                    </template>
                  </v-file-input>
                  <div class="cropper-wrapper">
                    <cropper
                    classname="cropper"
                    :src="img"
                    ref="cropper"
                    class="mt-4 mb-4"
                    ></cropper>
                    <v-btn @click="crop" color="primary" small>
                      <v-icon>demo-icon icon-crop</v-icon>Crop
                    </v-btn>
                  </div>
                  
                </v-col>
                <v-col col="6">
                  <h3>Preview</h3>
                  <div class="img-preview" v-html="text.html">
                  </div>
                </v-col>
              </v-row>
              <div class="d-flex flex-row-reverse">
                <v-btn class="mt-4" color="error" @click="addImageModalClose">Close</v-btn>
                <v-btn class="ma-4" color="primary" @click="submitImage">Add</v-btn>
              </div>
            </v-card-text>
        </v-card>
        
    </v-dialog>
    </v-row>
</template>

<script>
const axios = require('axios');
import { Cropper } from 'vue-advanced-cropper'
  export default {
    name: 'AddImage',
    data() {
      return {
        files: [],
        coordinates: {
          width: 0,
          height: 0,
          left: 0,
          top: 0
        },
        img: '',
        image: '',
        uid:-1,
        text: {
            html: '',
            id:'',
            coords:{x:0,y:0,w:"auto",h:"auto"},
        },
        texts: [],
      }
    },
    methods: {
      
      addImageModalClose: function(){
        this.$store.commit('changeImage', false);
      },
      submitImage: function() {
          if(!this.text.html){
            this.text.html = `<img src="${this.img}">`;
            this.$store.commit('changeImage', false);
          }
          
          this.$store.commit('htmlListChange',JSON.stringify(this.text));
          this.texts = this.$store.getters.texts;
          if(!Array.isArray(this.$store.getters.texts)){this.texts=[]}
          this.texts.push(JSON.parse(this.$store.getters.htmlList));
          this.$store.commit('changeHTMLList',this.texts);
          const allHTMLDataStr = (this.$store.getters.htmlList);
          const app = this;
          axios.post('http://localhost:5000/createHTML', {
            html: allHTMLDataStr,
            id: this.$route.name == 'New' ? this.uid : this.$route.params.id
          })
          .then(function () {
            app.$store.commit('changeImage', false);
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
      },
      crop() {
        const {coordinates, canvas} = this.$refs.cropper.getResult()
        this.coordinates = coordinates
        // You able to do different manipulations at a canvas
        // but there we just get a cropped image
        this.text.html = `<img src="${canvas.toDataURL()}">`;
        
      },
      uploadImage() {
        // Reference to the DOM input element
        var input = document.getElementById('uploadInput');
        // Ensure that you have a file before attempting to read it
        if (input.files && input.files[0]) {
            // create a new FileReader to read this image and convert to base64 format
            var reader = new FileReader();
            // Define a callback function to run, when FileReader finishes its job
            reader.onload = (e) => {
                // Note: arrow function used here, so that "this.imageData" refers to the imageData of Vue component
                // Read image as base64 and set to imageData
                this.img =  e.target.result;
                this.text.html = `<img style="height: 300px;" src="${this.img}">`;
            }
            // Start the reader job - read file as a data url (base64 format)
            reader.readAsDataURL(input.files[0]);
        }
      },
    },
    created() {
      const app = this;
      this.text.html = ``;
      axios.get('http://localhost:5000/uniqueID')
        .then(function (response) {
          app.uid = response.data;
        })
        .catch(function (error) {
          console.log(error);
      });
    },
    computed: {
    },
    mounted() {
    },
    components: {
      Cropper
    }
  }
</script>


<style scoped>
img{
  width: 90%;
}
.cropper {
	height:300px;
	background: #DDD;
}
.cropper-wrapper {
	position: relative;
	height: 300px;
	background: black;
}
.cropper-background {
	position: absolute;
	width: 100%;
	height: 100%;
	background-size: cover;
	background-position: 50%;
	filter: blur(5px);
	opacity: 0.25;
}
.img-preview{
  height: 300px;
  text-align: center;
  background-color: #DDD;
}
.img-preview img{
  height: 300px;
  width: auto;
  max-width: 50%;
}
.html img{
  width: 100%;
  height: 100%;
}
</style>
