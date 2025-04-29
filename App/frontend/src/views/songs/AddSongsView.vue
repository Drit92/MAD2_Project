<template>
  <div class="container text-center">
    <div class="row">
      <div class="col-4"></div>
      <div class="col">
        <br /><br />
        <p>To add a new Song<br /> Fill this form</p>
        <form @submit.prevent="addSong">
          <div class="mb-3">
            <input type="text" class="form-control" v-model="song.song_name" required placeholder="Song Name" />
          </div>
          <div class="mb-3">
            <input type="text" class="form-control" v-model="song.song_artist" required placeholder="Artist Name" />
          </div>
          <div class="mb-3">
            <input type="file" class="form-control" @change="onFileSelected" accept=".mp3,.wav,.oog" required />
          </div>
          <button type="submit" class="btn btn-primary">Add Song</button>
        </form>
      </div>
      <div class="col-4"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import refreshAccessToken from '@/utils/refreshToken';

export default {
  name: "AddSong",
  data() {
    return {
      song: {
        song_name :'',
        song_artist: '',
        
      },
      file: null,
    };
  },
  methods: {
    async addSong() {
      if (!this.song.song_name || !this.song.song_artist ) {
        alert("All fields are required!");
        return;
      }

      let formData = new FormData();
      formData.append('data',JSON.stringify(this.song))
      formData.append('file', this.file);

      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        await axios.post("http://127.0.0.1:8081/api/songs", formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.$router.push("/chome");
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.addSong();
        } else {
          console.error('Error adding song:', error);
          alert('An error occurred while adding song.', error);
        }
      }
    },
    onFileSelected(event) {
      this.file = event.target.files[0];
    }
  }
};
</script>

<style scoped>

</style>
