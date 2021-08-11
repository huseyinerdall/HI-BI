<template>
    <v-container align="center">
        <v-row align="center">
            <v-col cols="6">
                <form>
                    <v-text-field
                    v-model="user.name"
                    class="mt-10"
                    label="Name"
                    outlined dense
                    ></v-text-field>

                    <v-text-field
                    v-model="user.email"
                    label="E-mail"
                    outlined dense
                    ></v-text-field>

                    <v-file-input
                        label="Profile photo"
                        filled outlined dense
                        prepend-icon=""
                        prepend-inner-icon="mdi-camera"
                        v-model="image"
                        id="profile-image"
                    ></v-file-input>

                    <v-select
                    v-model="user.department"
                    :items="positions"
                    label="Department"
                    outlined dense
                    ></v-select>

                    <v-btn color="primary" @click="saveUser" class="mr-4">save changes</v-btn>
                </form>
            </v-col>

            <v-col cols="6">
                <v-card
                    class="mx-auto"
                    max-width="434"
                    tile
                >
                    <v-img
                    height="100%"
                    src="https://www.masala.com/public/styles/fb_share_style_image/public/images/2019/06/21/57554.jpg?itok=eGK4KkqVg"
                    >
                    <v-row
                        align="end"
                        class="fill-height pl-4 pt-1"
                    >
                        <v-col
                        align-self="start"
                        class="pa-0"
                        cols="12"
                        >
                        <v-avatar
                            class="profile ml-4"
                            color="grey"
                            size="150"
                            tile
                            cover
                        >
                            <v-img :src="user.image"></v-img>
                        </v-avatar>
                        </v-col>
                        <v-col class="py-0">
                        <v-list-item
                            color="rgba(0, 0, 0, .4)"
                            dark
                        >
                            <v-list-item-content>
                            <v-list-item-title class="title">{{user.name}}</v-list-item-title>
                            <v-list-item-subtitle>{{user.department}}</v-list-item-subtitle>
                            <v-list-item-subtitle>{{user.email}}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                        </v-col>
                    </v-row>
                    </v-img>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
const axios = require('axios');
export default {
data: () => ({
    user: {
        name: 'Hüseyin ERDAL',
        email: 'huseyinerdal@protonmail.com',
        image: 'https://flyjazz.ca/wp-content/uploads/2017/01/dummy-user.jpg',
        department: 'Developer',
    },
    image : null,
      select: null,
      positions: [
        'Developer',
        'DB Admin',
      ],
    }),

    computed: {
    },
    created() {
        this.getUserInfos();
    },

    methods: {
        saveUser: function(){
            const app = this;
            axios.post('http://localhost:5000/saveUser', {
                user: app.user,
            })
            .then(function (response) {
                console.log(response.data);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        getUserInfos: function(){
            const app = this;
            axios.get('http://localhost:5000/getUserInfos')
            .then(function (response) {
                console.log(response.data)
                app.user = response.data[0];
            })
            .catch(function (error) {
                console.log(error);
            })
        },
    },
    watch: {
        image: function(n,o){
            if(!n){return;}
            const app = this;
            console.log(n,o);
            const file = document.querySelector('#profile-image').files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.addEventListener("load", function () {
                app.user.image = reader.result;
            }, false);
        }
    }
  }
</script>