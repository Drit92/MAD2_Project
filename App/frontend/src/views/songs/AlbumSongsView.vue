<template>
  <div class="container text-center">
    <h1>{{ albumName }}</h1>
    <div class="row">
      <div class="col column">
        <h2>Songs:</h2>
        <div v-for="song in songs" :key="song.song_id">
          <div class="card float-start" style="width: 20rem; margin:10px;">
            <div class="card-body">
              <h5 class="card-title">{{ song.song_name }}</h5>
              <p class="card-text">{{ song.song_artist }} <br><span style="color: #FFD700;">&#9733;</span> {{ song.song_avg_review.toFixed(2) }}</p>
              <audio controls>
                <source :src="base_url + song.song_path" type="audio/mpeg">
              </audio>
              <a :href="`/song_rate/${song.song_id}`" class="btn btn-primary">Give Ratings</a>
            </div>
          </div>
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
      albumName: '',
      songs: [],
      base_url: "http://localhost:8081", 
    };
  },
  async mounted() {
    const albumId = this.$route.params.albumId; 
    console.log('Album ID:', albumId); 
    await this.fetchAlbumData(albumId);
},

  methods: {
    async fetchAlbumData(albumId) {
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        const response = await axios.get(`http://127.0.0.1:8081/api/album/${albumId}`);
        this.albumName = response.data.album_name; 
        this.songs = response.data.songs;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // If the error is 401 (Unauthorized), attempt to refresh the access token
          try {
            await refreshAccessToken(); // Refresh the access token
            // Retry fetching the album data after refreshing the token
            await this.fetchAlbumData(albumId);
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            alert('Failed to refresh access token. Please login again.');
            // Redirect to login page or handle authentication failure as needed
          }
        } else {
          console.error('Error fetching album data:', error);
        
        }
      }
    },
  },
};
</script>

<style>

</style>
