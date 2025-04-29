<template>
  <div>
    <button @click="goBack" class="go-back-button">Go Back</button>

    <div class="playlist">
      <h1>{{ playlistName }}</h1>
      <div class="card-container">
        <div v-for="song in songs" :key="song.song_id" class="card song-card">
          <div class="card-body">
            <h5 class="card-title">{{ song.song_name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ song.song_artist }}</h6>
            <audio controls class="song-audio">
              <source :src="base_url + song.song_path" type="audio/mpeg">
            </audio>
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
  name: "PlaylistSongs",
  data() {
    return {
      songs: [],
      base_url: "http://localhost:8081",
      playlistName: ""
    };
  },
  async created() {
    await this.fetchPlaylist();
    await this.fetchSongs();
  },
  methods: {
    async fetchPlaylist() {
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        const response = await axios.get(`${this.base_url}/api/play/${this.$route.params.playlistId}`);

        this.playlistName = response.data.playlist_name;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.fetchPlaylist();
        } else if (error.response) {
          alert("An error occurred while fetching playlist data");
        }
      }
    },
    async fetchSongs() {
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        const response = await axios.get(`${this.base_url}/api/play/${this.$route.params.playlistId}/songs`);

        this.songs = response.data.songs;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.fetchSongs();
        } else if (error.response) {
          alert("An error occurred while fetching songs data");
        }
      }
    },
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.go-back-button {
  position: absolute;
  top: 10px;
  left: 10px;
}

.playlist {
  padding: 20px;
}

.card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.song-card {
  width: 600px; 
  margin-bottom: 20px; 
}

.song-audio {
  width: 100%;
}
</style>
