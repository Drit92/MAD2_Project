<template>
    <div>
      <h1>Delete Song</h1>
      <div>
        <label for="selectedSong">Select Song:</label>
        <select v-model="selectedSong" id="selectedSong">
          <option v-for="song in songs" :key="song.song_id" :value="song.song_id">{{ song.song_name }}</option>
        </select>
        <button @click="deleteSong">Delete Song</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        selectedSong: null,
        songs: []
      };
    },
    created() {
      this.fetchSongs();
    },
    methods: {
      async fetchSongs() {
        try {
          const response = await axios.get('http://127.0.0.1:8081/api/songs');
          this.songs = response.data;
        } catch (error) {
          console.error('Error fetching songs:', error);
        }
      },
      async deleteSong() {
        if (!this.selectedSong) {
          alert('Please select a song to delete.');
          return;
        }
        try {
          await axios.delete(`http://127.0.0.1:8081/api/song/${this.selectedSong}`);
          alert('Song deleted successfully.');
          this.fetchSongs(); // Refresh song list after deletion
        } catch (error) {
          console.error('Error deleting song:', error);
          alert('An error occurred while deleting the song.');
        }
      }
    }
  };
  </script>
  
  <style scoped>
 
  </style>