<template>
  <div>
    <div id="bx"><button @click="goBack" class="back-btn">Back</button></div>
    <h1>Create Playlist</h1>
    <form @submit.prevent="createPlaylist">
      <label for="playlistName">Playlist Name:</label>
      <input type="text" id="playlistName" v-model="playlistName" required>
      <button type="submit">Create Playlist</button>
    </form>

    <div v-if="playlists.length > 0" class="playlist-container">
      <h2>Your Playlists</h2>
      <div v-for="playlist in playlists" :key="playlist.playlist_id" class="playlist-card">
        <h3>{{ playlist.playlist_name }}</h3>
        <router-link :to="'/view_play/' + playlist.playlist_id"><button class="playlist-btn">View Playlist</button></router-link>
        <router-link :to="'/add_del_son_playlist/' + playlist.playlist_id"><button class="playlist-btn">Add/Delete Songs</button></router-link>
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
      playlistName: "",
      playlists: [],
      user_id: ""
    }
  },
  methods: {
    async createPlaylist() {
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        alert('User ID not found');
        return;
      }

      const data = {
        playlist_name: this.playlistName,
        user_id: parseInt(userId)
      };

      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        await axios.post('http://127.0.0.1:8081/api/allplay', data);
        this.$router.push("/chome");
      } catch (error) {
        if (error.response && error.response.status === 401) {
          try {
            await refreshAccessToken();
            await this.createPlaylist();
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            alert('An error occurred while refreshing access token.');
          }
        } else {
          console.error('There was a problem with the request:', error);
          alert('An error occurred while creating the playlist.');
        }
      }
    },
    goBack() {
      this.$router.go(-1); // Go back to the previous page
    },
    async fetchPlaylists() {
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        alert('User ID not found');
        return;
      }

      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        const response = await axios.get(`http://127.0.0.1:8081/api/${userId}/get_user_playlists`);
        this.playlists = response.data.playlists;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          try {
            await refreshAccessToken();
            await this.fetchPlaylists();
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            alert('An error occurred while refreshing access token.');
          }
        } else {
          console.error('Error fetching playlists:', error);
          alert('An error occurred while fetching playlists.');
        }
      }
    }
  },
  async mounted() {
    await this.fetchPlaylists();
  }
}

</script>

<style scoped>
.back-btn {
  position: absolute;
  top: 10px;
  left: 10px;
}
.playlist-container {
  margin-top: 20px;
}
.playlist-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
.playlist-btn {
  margin-right: 10px;
}

.bx{
  margin-bottom: 20px;

}

h1 {
  margin-top: 50px;
  margin-bottom: 20px; 
}
</style>
