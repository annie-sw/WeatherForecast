import axios from 'axios'
// import consts from '@/constants'

const WebResult = {
  Success: Symbol(''),
  ServerError: Symbol(''),
  InvalidRequest: Symbol('')
}

const client = axios.create({
  xsrfHeaderName: 'X-CSRF-Token'
  // withCredentials: true   // @TODO: CORS でエラーになるので一旦外す、 CSRF は別途実装
})

client.interceptors.response.use((response) => {
  return Promise.resolve({
    data: response.data
  })
}, (error) => {
  return Promise.resolve({
    error: error.response
  })
})

const send = async (method, path, data) => {
  // return method(consts.api_url + path, data)
  return method(path, data)
}

const get = async (path) => {
  return send(client.get, path)
}
const post = async (path, data) => {
  return send(client.post, path, data)
}

export default {
  WebResult,

  async loadTextData() {
    return get('/static/data/lang_text.na.json')
  },
  // async getPosts (query) {
    // return get('/media/list')
  // },

  // async postMediaData (form) {
    // return post('/media/create', form)
  // }
}
