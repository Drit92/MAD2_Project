<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6" style="padding: 10px;">
        <button @click="goBack" class="btn btn-primary">Go Back</button>
      </div>
    </div>
    <h1>{{ albumName }}</h1>
    <h2>{{ song_artist }}</h2>
    <div class="row">
      <div class="col-md-6" style="padding: 10px;">
        <h2>Remove Songs from Album</h2>
        <ul v-if="albumSongs && albumSongs.length > 0">
          <li v-for="song in albumSongs" :key="song.song_id">
            {{ song.song_name }}
            <button @click="removeFromAlbum(song.song_id)" class="btn btn-danger">Remove</button>
          </li>
        </ul>
        <p v-else>No songs added to this album</p>
      </div>
      <div class="col-md-6" style="padding: 10px;">
        <h2>Add Songs to Album</h2>
        <ul v-if="availableSongs.length > 0">
          <li v-for="song in availableSongs" :key="song.song_id">
            {{ song.song_name }}
            <button @click="addToAlbum(song.song_id)" class="btn btn-success">Add</button>
          </li>
        </ul>
        <p v-else>No available songs</p>
      </div>
    </div>
    <div v-if="loading" class="text-center mt-3">
      <span>Loading...</span>
    </div>
    <div v-if="error" class="text-center text-danger mt-3">
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import refreshAccessToken from '@/utils/refreshToken';
import { refreshPage } from '@/utils/refreshpage';

export default {
  data() {
    return {
      albumId: null,
      albumName: '',
      song_artist: '',
      albumSongs: [],
      availableSongs: [],
      loading: false,
      error: null
    };
  },
  mounted() {
    this.albumId = this.$route.params.albumId;
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const response = await axios.get(`http://127.0.0.1:8081/api/album/${this.albumId}/songs`);

        this.albumName = response.data.album_name;
        this.song_artist = response.data.song_artist;
        this.albumSongs = response.data.songs;
        
        // Fetch all songs separately
        const allSongsResponse = await axios.get('http://127.0.0.1:8081/api/songs');
        const allSongs = allSongsResponse.data;
        
        // Filter available songs by the same artist as the album
        this.availableSongs = allSongs.filter(song => song.song_artist === this.song_artist && song.album_id===null );
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.fetchData();
        } else {
          this.error = 'Error fetching data';
          console.error('Error fetching data:', error);
        }
      } finally {
        this.loading = false;
      }
    },

    async addToAlbum(songId) {
      this.loading = true;
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const requestData = {
          album_id: this.albumId,
          song_id: songId
        };

        await axios.post('http://127.0.0.1:8081/api/add_del_song_to_album', requestData);
        await this.fetchData();
        this.fetchData();
        refreshPage();
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.addToAlbum(songId);
          this.fetchData();
        } else {
          //this.error = 'Error adding song to album';
          console.error('Error adding song to album:', error);
          this.fetchData();
        }
      } finally {
        this.loading = false;
      }
    },

    async removeFromAlbum(songId) {
      this.loading = true;
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        await axios.delete(`http://127.0.0.1:8081/api/add_del_song_to_album`, {
          data: {
            album_id: this.albumId,
            song_id: songId
          }
        });
        await this.fetchData();
        this.fetchData();
        refreshPage();
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.removeFromAlbum(songId);
        } else {
          //this.error = 'Error removing song from album';
          console.error('Error removing song from album:', error);
          this.fetchData();
        }
      } finally {
        this.loading = false;
      }
    },

    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>

</style>
