<template>
  <v-app>
    
    <v-navigation-drawer
      v-model="drawer"
      v-if="isEditMode && $route.name != 'Login'"
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
    >
      <v-list dense>
        <template v-for="item in items">
          <v-list-group
            v-if="item.children"
            :key="item.text"
            v-model="item.model"
            :prepend-icon="item.icon"
            append-icon="demo-icon icon-down-open-mini "
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.text }}
                </v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item
              v-for="(child, i) in item.children"
              :key="i"
              link
            >
              <v-list-item-action v-if="child.icon" class="ml-0">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-item-action>
              <router-link tag="a" style="margin-left:0;" :to='child.link'>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ child.text }}
                  </v-list-item-title>
                </v-list-item-content>
              </router-link>
              
            </v-list-item>
          </v-list-group>
          <v-list-item
            v-else
            :key="item.text"
            link
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      app
      color="deep-orange darken-3"
      dark
      v-if="isEditMode && $route.name != 'Login'"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title
        style="width: 100px"
        class="ml-0 pl-4"
      >
        <span class="hidden-sm-and-down">HI-BI</span>
      </v-toolbar-title>
      <v-text-field
        flat
        solo-inverted
        hide-details
        prepend-inner-icon="demo-icon icon-search-8"
        label="Search"
        class="hidden-sm-and-down"
      ></v-text-field>
      <v-chip
      class="ma-2"
      color="transparent"
      text-color="white"
      >
      <template v-if="connected">
        Connected
        <v-avatar right>
          <v-icon>mdi-checkbox-marked-circle</v-icon>
        </v-avatar>
      </template>
      <template v-else>
        <v-avatar right>
          <v-icon>demo-icon icon-window-close-o</v-icon>
        </v-avatar>
      </template>
      
    </v-chip>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>demo-icon icon-bell-5</v-icon>
      </v-btn>
        <v-btn text @click="dialog = !dialog">
          <v-icon>demo-icon icon-user-1</v-icon>
          <span>{{ isAuthenticated }}</span>
        </v-btn>
    </v-app-bar>
    <v-content style="width:100%;height:100%;">
      <router-view :key="$route.fullPath"></router-view>
    </v-content>
  </v-app>
</template>

<script>
/* const axios = require('axios'); */
  export default {
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
      connected: false,
      uid:0,
      items: [
        {
          icon: 'demo-icon icon-tools',
          connected: false,
          text: 'Reports',
          model: false,
          children: [
            { icon: 'demo-icon icon-plus-circled', text: 'New Report',link: '/new' },
            { icon: 'demo-icon icon-th-list', text: 'Reports', link: '/reports' },
          ],
        },
        {
          icon: 'demo-icon icon-back-in-time',
          text: 'Scheduler Tasks',
          model: false,
          children: [
            { icon: 'demo-icon icon-plus-circled', text: 'Set a Scheduler', link: '/set-a-task' },
            { icon: 'demo-icon icon-calendar-2', text: 'View Tasks', link: '/tasks' },
          ],
        },
        {
          icon: 'demo-icon icon-cog-3',
          text: 'Settings',
          model: false,
          children: [
            { icon: 'demo-icon icon-plus-circled', text: 'Personal', link: '/profile' },
            { icon: 'demo-icon icon-calendar-2', text: 'Application', link: '/settings' },
          ],
          },
      ],
      isAuthenticated: false,
    }),
    computed: {
        dialog: {
          get: function (){
            return false;
          },
          set: function (newValue){
            return newValue;
          }
        },
        isEditMode: function(){
          return (this.$route.name != 'New' && this.$route.name != 'Edit')
        },
    },
    mounted() {
    },
    created() {
      //this.isAuthenticated = !!localStorage.getItem('token');
      this.isAuthenticated = this.$store.getters.isAuthenticated;
    },
    components: {
      
    },
    methods: {
      
    }
  }
</script>

<style>
@import './assets/font/css/fontello.css';
.v-list-group--active > .v-list-group__header > .v-list-group__header__append-icon .v-icon{
  transform-origin: 8px;
}
</style>
