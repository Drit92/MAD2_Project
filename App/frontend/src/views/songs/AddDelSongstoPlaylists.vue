<template>
  <div class="container">
    <div class="row">
      <!-- First column for adding songs to playlist -->
      <div class="col-md-6">
        <h2>Add Songs to Playlist</h2>
        <ul>
          <li v-for="song in availableSongs" :key="song.song_id">
            {{ song.song_name }}
            <button @click="addToPlaylist(song.song_id)">Add</button>
          </li>
        </ul>
      </div>
      <!-- Second column for deleting songs from playlist -->
      <div class="col-md-6">
        <h2>Delete Songs from Playlist</h2>
        <ul>
          <li v-for="song in playlistSongs" :key="song.song_id">
            {{ song.song_name }}
            <button @click="removeFromPlaylist(song.song_id)">Remove</button>
          </li>
        </ul>
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
      availableSongs: [],
      playlistSongs: [],
      playlistId: null 
    };
  },
  mounted() {
    // Fetch playlistId from router parameter
    this.playlistId = this.$route.params.playlistId;
    // Fetch available songs not in playlist
    this.fetchAvailableSongs();
    // Fetch songs in playlist
    this.fetchPlaylistSongs();
  },
  watch: {
    // Watch for changes in route params
    '$route.params.playlistId': function(newPlaylistId) {
      this.playlistId = newPlaylistId;
      // Re-fetch data when playlistId changes
      this.fetchAvailableSongs();
      this.fetchPlaylistSongs();
    }
  },
  methods: {
    async fetchAvailableSongs() {
      try {
        await this.refreshTokenAndFetch(() => {
          return axios.get(`http://127.0.0.1:8081/api/avail_songs/${this.playlistId}`);
        }, (response) => {
          this.availableSongs = response.data.available_songs;
        });
      } catch (error) {
        console.error(error);
      }
    },
    async fetchPlaylistSongs() {
      try {
        await this.refreshTokenAndFetch(() => {
          return axios.get(`http://127.0.0.1:8081/api/playlist/${this.playlistId}/song`);
        }, (response) => {
          this.playlistSongs = response.data;
        });
      } catch (error) {
        console.error(error);
      }
    },
    async addToPlaylist(songId) {
      try {
        await this.refreshTokenAndFetch(() => {
          return axios.post(`http://127.0.0.1:8081/api/playlist/${this.playlistId}/song/${songId}`);
        }, () => {
          this.fetchPlaylistSongs();
          this.fetchAvailableSongs();
        });
      } catch (error) {
        console.error(error);
      }
    },
    async removeFromPlaylist(songId) {
      try {
        await this.refreshTokenAndFetch(() => {
          return axios.delete(`http://127.0.0.1:8081/api/playlist/${this.playlistId}/song/${songId}`);
        }, () => {
          this.fetchPlaylistSongs();
          this.fetchAvailableSongs(); 
        });
      } catch (error) {
        console.error(error);
      }
    },
    async refreshTokenAndFetch(apiCall, successCallback) {
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        const response = await apiCall();
        successCallback(response);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.refreshTokenAndFetch(apiCall, successCallback);
        } else if (error.response) {
          console.error("An error occurred while fetching data:", error.response);
          throw error;
        }
      }
    }
  }
};
</script>

<style scoped>

</style>
