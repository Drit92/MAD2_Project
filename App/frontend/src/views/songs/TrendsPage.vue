<template>
  <div>
  <div class="colrr">
  <div>
    <!-- Latest Songs -->
    <div class="latest-songs">
      <h2>Latest Songs</h2>
      <div class="song-list">
        <div v-for="latestSong in latestSongs" :key="latestSong.song_id" class="song-item">
          
          <div class="song-details">
            <h3>{{ latestSong.song_name }}</h3>
            <p>{{ latestSong.song_artist }}</p>
            <p>Rating: {{ latestSong.song_avg_review }}</p>
            <audio controls :src="base_url + latestSong.song_path"></audio>
          </div>
        </div>
      </div>
    </div>

    <hr class="blurry-divider">

    <!-- High Rate Trend Songs -->
    <div class="trend-songs">
      <h2>High Rate Trend Songs</h2>
      <div class="song-list">
        <div v-for="song in songs" :key="song.song_id" class="song-item">
          
          <div class="song-details">
            <h3>{{ song.song_name }}</h3>
            <p>{{ song.song_artist }}</p>
            <p>Rating: {{ song.song_avg_review }}</p>
            <audio controls :src="base_url + song.song_path"></audio>
            
          </div>
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
      latestSongs: [],
      songs: [],
      base_url: "http://localhost:8081"
    };
  },
  mounted() {
    this.fetchLatestSongs();
    this.fetchTrendSongs();
  },
  methods: {
    async fetchLatestSongs() {
      try {
        const response = await axios.get('http://127.0.0.1:8081/api/latest_songs', { headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') } });
        this.latestSongs = response.data;
      } catch (error) {
        this.handleAxiosError(error);
      }
    },
    async fetchTrendSongs() {
      try {
        const response = await axios.get('http://127.0.0.1:8081/api/trend_songs', { headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') } });
        this.songs = response.data;
      } catch (error) {
        this.handleAxiosError(error);
      }
    },
    async handleAxiosError(error) {
      if (error.response && error.response.status === 401) {
        try {
          await refreshAccessToken();
          // Retry fetching songs after refreshing token
          await this.fetchLatestSongs();
          await this.fetchTrendSongs();
        } catch (refreshError) {
          console.error('Error refreshing access token:', refreshError);
          alert('Failed to refresh access token. Please log in again.');
          // Redirect to login page or handle authentication failure as needed
        }
      } else {
        console.error('Axios Error:', error);
      }
    }
  }
};
</script>



<style scoped>

h2{
  color: #e7b718;
}
.trend-songs {
  padding: 20px;
}

.colrr{
  color: rgb(14, 39, 9);
  
}


.blurry-divider {
    border: none;
    height: 10px; 
    background: linear-gradient(to right, rgba(0,0,0,0.5), rgba(0,0,0,0.5), rgba(0,0,0,0)); 
  }

.song-list {
  display: flex;
  overflow-x: auto;
  gap: 20px;
}

.song-item {
  flex: 0 0 auto;
  width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
}

.song-item img {
  width: 100%;
  height: auto;
  border-radius: 5px;
}

.song-details {
  margin-top: 10px;
}

.latest-songs{
  overflow-x: scroll;
}

.trend-songs{
  overflow-x: scroll;
}
</style>
