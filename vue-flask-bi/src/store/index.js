import Vue from "vue";
import Vuex from "vuex";
import { isValidJwt, EventBus } from '@/auth'
import { authenticate, register } from '@/auth/functions.js'
Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        addModal: false,
        addTextModal: false,
        addImageModal: false,
        loader: false,
        graphList: [],
        currentGraph: '',
        graphs: [],
        htmlList: [],
        texts: [],
        htmls: [],
        editJson: {},
        server: 'http://localhost:5000',
        user: {},
        jwt: '',
    },
    mutations: {
        change(state, addModal) {
            state.addModal = addModal
        },
        changeLoader(state, loader) {
            state.loader = loader
        },
        changeText(state, addTextModal) {
            state.addTextModal = addTextModal
        },
        changeImage(state, addImageModal) {
            state.addImageModal = addImageModal
        },
        listChange(state, newList) {
            state.graphList = newList;
        },
        listCreate(state, list) {
            state.graphList = list
        },
        currentGraphSet(state, newCurrent) {
            state.currentGraph = newCurrent;
        },
        changeGraphList(state, newList) {
            state.graphs = (newList);
        },
        changePosition(state, newPosition) {
            console.log(newPosition)
            state.graphs[newPosition['i']].coords = newPosition;
        },
        changePositionInDrag(state, newPosition) {
            console.log(newPosition)
            state.graphs[newPosition['i']].coords['x'] = newPosition['x'];
            state.graphs[newPosition['i']].coords['y'] = newPosition['y'];
        },
        htmlListChange(state, newHtmlList) {
            state.htmlList = newHtmlList;
        },
        changeHTMLList(state, newList) {
            state.texts = (newList);
        },
        changeHTMLPosition(state, newPosition) {
            console.log(newPosition)
            state.texts[newPosition['i']].coords = newPosition;
        },
        changeHTMLPositionInDrag(state, newPosition) {
            state.texts[newPosition['i']].coords['x'] = newPosition['x'];
            state.texts[newPosition['i']].coords['y'] = newPosition['y'];
        },
        editJson(state, neww) {
            state.editJson = neww;
        },
        setUserData(state, payload) {
            console.log('setUserData payload = ', payload)
            state.userData = payload.userData
        },
        setJwtToken(state, payload) {
            console.log('setJwtToken payload = ', payload)
            localStorage.token = payload.jwt.token
            state.jwt = payload.jwt
        }
    },
    getters: {
        addModal: state => state.addModal,
        addTextModal: state => state.addTextModal,
        addImageModal: state => state.addImageModal,
        graphList: state => (state.graphList),
        currentGraph: state => state.currentGraph,
        graphs: state => state.graphs,
        htmlList: state => (state.htmlList),
        texts: state => state.texts,
        htmls: state => state.htmls,
        loader: state => state.loader,
        editJson: state => state.editJson,
        server: state => state.server,
        isAuthenticated(state) {
            return isValidJwt(state.jwt.token);
        }
    },
    actions: {
        login(context, userData) {
            context.commit('setUserData', { userData })
            return authenticate(userData)
                .then(response => context.commit('setJwtToken', { jwt: response.data }))
                .catch(error => {
                    console.log('Error Authenticating: ', error)
                    EventBus.$emit('failedAuthentication', error)
                })
        },
        register(context, userData) {
            context.commit('setUserData', { userData })
            return register(userData)
                .then(context.dispatch('login', userData))
                .catch(error => {
                    console.log('Error Registering: ', error)
                    EventBus.$emit('failedRegistering: ', error)
                })
        },
    }
});