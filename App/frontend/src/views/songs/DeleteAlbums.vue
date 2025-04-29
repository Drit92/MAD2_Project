<template>
  <div>
    <h1>Delete Album</h1>
    <div>
      <label for="selectedAlbum">Select Album:</label>
      <select v-model="selectedAlbum" id="selectedAlbum">
        <option v-for="album in albums" :key="album.album_id" :value="album.album_id">{{ album.album_name }}</option>
      </select>
      <button @click="deleteAlbum">Delete Album</button>
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
            await refreshAccessToken(); // Refresh the access token
            await this.fetchAlbums(); // Retry fetching albums
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            alert('An error occurred while refreshing access token.');
          }
        } else {
          console.error('Error fetching albums:', error);
          alert('An error occurred while fetching albums.');
        }
      }
    },
    async deleteAlbum() {
      if (!this.selectedAlbum) {
        alert('Please select an album to delete.');
        return;
      }
      try {
        const accessToken = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;

        const requestData = {
          album_id: this.selectedAlbum
        };

        await axios.delete(`http://localhost:8081/api/album/${this.selectedAlbum}`, { data: requestData });
        alert('Album deleted successfully.');
        this.fetchAlbums(); // Refresh album list after deletion
      } catch (error) {
        if (error.response && error.response.status === 401) {
          try {
            await refreshAccessToken(); // Refresh the access token
            await this.deleteAlbum(); // Retry deleting the album
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            alert('An error occurred while refreshing access token.');
          }
        } else {
          console.error('Error deleting album:', error);
          alert('An error occurred while deleting the album.');
        }
      }
    }
  }
};
</script>

<style scoped>

</style>
