<template>
    <div>
      <h2>Albums:</h2>
      <div v-for="album in albums" :key="album.album_id">
        <div class="card float-start" style="width: 25rem; margin: 10px;">
          <img src="" class="card-img-top" alt="">
          <div class="card-body">
            <h5 class="card-title">{{ album.album_name }}</h5>
            <p class="card-text">{{ album.song_artist }}</p>
            <router-link :to="'/addDel_son_alb/' + album.album_id" class="btn btn-primary">Add/Delete Songs</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import refreshAccessToken from '@/utils/refreshToken'; 
  
  export default {
    data() {
      return {
        selectedAlbum: null,
        albums: []
      };
    },
    created() {
      this.fetchAlbums();
    },
    methods: {
      async fetchAlbums() {
        try {
          const accessToken = localStorage.getItem('access_token');
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;
          const response = await axios.get('http://127.0.0.1:8081/api/albums');
          this.albums = response.data;
        } catch (error) {
          if (error.response && error.response.status === 401) {
            try {
              await refreshAccessToken(); 
              await this.fetchAlbums(); 
            } catch (refreshError) {
              console.error('Error refreshing access token:', refreshError);
              alert('An error occurred while refreshing access token.');
              
            }
          } else {
            console.error('Error fetching albums:', error);
            alert('An error occurred while fetching albums.');
          }
        }
      }
    }
  };
  </script>
  
  
  <style scoped>
  
  </style>
  