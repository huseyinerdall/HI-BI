<template>
  <v-app id="inspire">
    <v-content>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>HI-BI</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    class="text-center"
                    label="Login"
                    name="login"
                    v-model="username"
                    prepend-icon="mdi-account"
                    type="text"
                  ></v-text-field>

                  <v-text-field
                    id="password"
                    label="Password"
                    name="password"
                    prepend-icon="mdi-lock"
                    type="password"
                    v-model="password"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="authenticate">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { EventBus } from '@/auth'
  export default {
    data () {
      return {
        username: '',
        password: '',
        errorMsg: ''
      }
    },
    methods: {
      authenticate () {
        this.$store.dispatch('login', { username: this.username, password: this.password })
          .then(() => this.$router.push('/'))
      },
    },
    mounted () {
      EventBus.$on('failedRegistering', (msg) => {
        this.errorMsg = msg
      })
      EventBus.$on('failedAuthentication', (msg) => {
        this.errorMsg = msg
      })
    },
    beforeDestroy () {
      EventBus.$off('failedRegistering')
      EventBus.$off('failedAuthentication')
    },
    props: {
      source: String,
    },
  }
</script>