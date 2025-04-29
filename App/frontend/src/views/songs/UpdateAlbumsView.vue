<template>
    <div>
      <div class="container">
        <div class="row">
          <div class="col">
            <h2>Update Album</h2>
            <form @submit.prevent="updateAlbum">
              <div class="mb-3">
                <label for="selectedAlbum">Select Album:</label>
                <select v-model="selectedAlbum" id="selectedAlbum" class="form-select">
                  <option v-for="album in albums" :key="album.album_id" :value="album.album_id">
                    {{ album.album_name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="updatedAlbumName">Updated Album Name:</label>
                <input type="text" v-model="updatedAlbum.album_name" id="updatedAlbumName" class="form-control">
              </div>
              <div class="mb-3">
                <label for="updatedArtistName">Updated Artist Name:</label>
                <input type="text" v-model="updatedAlbum.song_artist" id="updatedArtistName" class="form-control">
              </div>
              <div class="mb-3">
                <label for="updatedAlbumGenre">Updated Album Genre:</label>
                <input type="text" v-model="updatedAlbum.album_genere" id="updatedAlbumGenre" class="form-control">
              </div>
              <button type="submit" class="btn btn-primary">Update Album</button>
            </form>
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
        updatedAlbum: {
          album_name: '',
          song_artist: '',
          album_genere: '',
        },
        albums: [],
      };
    },
    async created() {
      await this.fetchAlbums();
    },
    watch: {
      selectedAlbum: 'fetchAlbumDetails', // Watch for changes in selectedAlbum and call fetchAlbumDetails
    },
    methods: {
      async fetchAlbums() {
        try {
          let access_token = localStorage.getItem('access_token');
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
          const response = await axios.get("http://127.0.0.1:8081/api/albums");
          this.albums = response.data;
        } catch (error) {
          if (error.response && error.response.status === 401) {
            await refreshAccessToken();
            await this.fetchAlbums();
          } else {
            console.error('Error fetching albums:', error);
            alert('An error occurred while fetching albums.');
          }
        }
      },
  
      async fetchAlbumDetails() {
        if (!this.selectedAlbum) return;
  
        try {
          let access_token = localStorage.getItem('access_token');
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
          const response = await axios.get(`http://127.0.0.1:8081/api/album/${this.selectedAlbum}`);
          this.updatedAlbum = response.data; // Update updatedAlbum with fetched data
          console.log(this.updatedAlbum);
        } catch (error) {
          if (error.response && error.response.status === 401) {
            await refreshAccessToken();
            await this.fetchAlbums();
          } else {
            console.error('Error fetching albums:', error);
            alert('An error occurred while fetching albums.');
          }
        }
      },
  
      async updateAlbum() {
        if (!this.selectedAlbum) {
          alert("Please select an album to update.");
          return;
        }
  
        try {
          let access_token = localStorage.getItem('access_token');
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
          await axios.put(`http://127.0.0.1:8081/api/album/${this.selectedAlbum}`, this.updatedAlbum);
          alert("Album updated successfully.");
          this.$router.push("/chome");
  
          this.updatedAlbum = {
            album_name: '',
            song_artist: '',
            album_genere: ''
          };
          await this.fetchAlbums();
        } catch (error) {
          if (error.response && error.response.status === 401) {
            await refreshAccessToken();
            await this.updateAlbum();
          } else {
            console.error('Error updating album:', error);
            alert('An error occurred while updating album.');
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  
  </style>
  