<template>
<v-row justify="center" @click="addTextModalClose">
    
    <v-dialog v-model="$store.getters.addTextModal" v-if="$store.getters.addTextModal" max-width="900px" min-height="400px" persistent>

        <v-card class="pt-20">
            <v-card-text class="pt-20">
              <div class="d-flex flex-row-reverse">
                <v-btn v-if="!previewMode" class="mt-2" small color="primary" @click="previewMode=!previewMode">Preview</v-btn>
                <v-btn v-if="previewMode" class="mt-2" small color="primary" @click="previewMode=!previewMode">Edit Mode</v-btn>
              </div>
              <quill-editor
              class="editor"
              ref="myTextEditor"
              :value="content"
              :options="editorOption"
              @change="onEditorChange"
              @blur="onEditorBlur($event)"
              @focus="onEditorFocus($event)"
              @ready="onEditorReady($event)"
              v-model="text.html"
              v-if="!previewMode"
              />
              
              <div v-if="previewMode" class="output ql-snow">
                  <div class="ql-editor" v-html="content"></div>
              </div>
              <div class="d-flex flex-row-reverse">
                <v-btn class="mt-4" color="error" @click="addTextModalClose">Close</v-btn>
                <v-btn class="ma-4" color="primary" @click="submitHTML">SAVE</v-btn>
              </div>
            </v-card-text>
        </v-card>
        
    </v-dialog>
    </v-row>
</template>

<script>
const axios = require('axios');
  import debounce from 'lodash/debounce'
  import { quillEditor } from 'vue-quill-editor'

  // import theme style
  import 'quill/dist/quill.core.css'
  import 'quill/dist/quill.snow.css'

  export default {
    name: 'quill-example-snow',
    title: 'Theme: snow',
    components: {
      quillEditor
    },
    data() {
      return {
        editorOption: {
          modules: {
            toolbar: [
              ['bold', 'italic', 'underline', 'strike'],
              [{ 'header': 1 }, { 'header': 2 }],
              [{ 'list': 'ordered' }, { 'list': 'bullet' }],
              [{ 'script': 'sub' }, { 'script': 'super' }],
              [{ 'indent': '-1' }, { 'indent': '+1' }],
              [{ 'direction': 'rtl' }],
              [{ 'size': ['small', false, 'large', 'huge'] }],
              [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
              [{ 'font': [] }],
              [{ 'color': [] }, { 'background': [] }],
              [{ 'align': [] }],
              ['clean'],
              ['link', 'image', 'video']
            ]
          }
        },
        uid:-1,
        content:'',
        text: {
            html: '',
            id:'',
            coords:{x:0,y:0,w:"auto",h:"auto"},
        },
        texts: [],
        previewMode: false,
      }
    },
    methods: {
      onEditorChange: debounce(function(value) {
        this.content = value.html
      }, 466),
      onEditorBlur(editor) {
        console.log('editor blur!', editor)
      },
      onEditorFocus(editor) {
        console.log('editor focus!', editor)
      },
      onEditorReady(editor) {
        console.log('editor ready!', editor)
      },
      addTextModalClose: function(){
        this.$store.commit('changeText', false);
      },
      submitHTML: function() {
        this.text.id = 'text_'+Math.random().toString(32).substring(2);
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
            app.$store.commit('changeText', false);
            //app.success(response.data);
            app.text.html = '';
            app.content = '';
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
    },
    created() {
      if("html" in this.$store.getters.editJson){
        this.text = this.$store.getters.editJson;
      }
      const app = this;
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
      console.log('this is Quill instance:', this.editor)
    }
  }
</script>


  <style scoped>
  .example {
    display: flex;
    flex-direction: column;
    height:200px;
  }

    .editor {
      min-height: 300px;
      overflow-y: auto;
      padding-top: 20px;
    }

    .output {
      width: 100%;
      margin: 20px auto;
      border: 1px solid #ccc;
      overflow-y: auto;
      resize: vertical;
    }
      .output.code {
        height: 300px;
      }

      .output.ql-snow {
          height: 320px;
      }
    .ql-snow .ql-tooltip{
        width: 320px;
        top: -15px !important;
        left: 240px !important;
    }
  
</style>
<style>
.ql-snow .ql-tooltip{
        width: 320px;
        top: -10px !important;
        left: 240px !important;
    }
    .ql-container{
        height:280px;
    }
</style>