<template>
  <div>
    <h1>Delete Playlist</h1>
    <select v-model="selectedPlaylistId">
      <option v-for="playlist in filteredPlaylists" :key="playlist.playlist_id" :value="playlist.playlist_id">
        {{ playlist.playlist_name }}
      </option>
    </select>
    <button @click="deletePlaylist">Delete Playlist</button>
  </div>
</template>

<script>
import axios from 'axios';
import refreshAccessToken from '@/utils/refreshToken';

export default {
  data() {
    return {
      playlists: [],
      selectedPlaylistId: null,
      user_id: localStorage.getItem('user_id')
    }
  },
  mounted() {
    this.fetchPlaylists();
  },
  computed: {
    filteredPlaylists() {
      // Filter playlists based on user_id
      return this.playlists.filter(playlist => playlist.user_id == this.user_id);
    }
  },
  methods: {
    fetchPlaylists() {
      axios.get('http://127.0.0.1:8081/api/allplay')
        .then(response => {
          this.playlists = response.data;
        })
        .catch(error => {
          console.error('There was a problem fetching playlists:', error);
        });
    },
    async deletePlaylist() {
  if (!this.selectedPlaylistId) {
    alert('Please select a playlist to delete.');
    return;
  }

  let access_token = localStorage.getItem('access_token');
  if (!access_token) {
    alert('Authentication token not found. Please log in.');
    return;
  }

  try {
    const response = await axios.delete(`http://127.0.0.1:8081/api/playlist/${this.selectedPlaylistId}`, {
      headers: {
        Authorization: 'Bearer ' + access_token
      }
    });
    console.log('Playlist deleted successfully:', response.data);
    
    this.playlists = this.playlists.filter(playlist => playlist.playlist_id !== this.selectedPlaylistId);
    this.selectedPlaylistId = null; // Reset selected playlist
  } catch (error) {
    if (error.response && error.response.status === 401) {
      await refreshAccessToken();
      await this.deletePlaylist(); // Retry deletePlaylist after refreshing token
    } else {
      console.error('There was a problem deleting the playlist:', error);
    }
  }
},


  }
}
</script>

<style>

</style>
