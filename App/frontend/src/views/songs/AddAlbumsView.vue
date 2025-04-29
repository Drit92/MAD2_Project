<template>
    <div>
        <div class="container ">
        <div class="row">
            <div class="col-4"></div>
            <div class="col">
                <br><br>
                <p>To add new Album<br> Fill this form</p>
                <form @submit.prevent="addAlbum">
                    <div class="mb-3">
                        <input type="text" class="form-control" v-model="album.album_name" required placeholder="Album Name">
                    </div>
                    <div class="mb-3">
                        <input type="text" class="form-control" v-model="album.song_artist" required placeholder="Artist Name">
                    </div>
                    <div class="mb-3">
                        <input type="text" class="form-control" v-model="album.album_genere" required placeholder="Album Genre">
                    </div>
                    <button type="submit" class="btn btn-primary">Add Album</button>
                </form>
            </div>
            <div class="col-4"></div>
        </div>
    </div>
    </div>
    
</template>

<script>
import axios from 'axios';
import refreshAccessToken from '@/utils/refreshToken';

export default {
    name: "AddAlbum",
    data() {
        return {
            album: {
                album_name: '',
                song_artist: '',
                album_genere: ''
            }
        }
    },
    methods: {
        async addAlbum() {
            if (!this.album.album_name || !this.album.song_artist || !this.album.album_genere) {
                alert("All fields are required!");
                return;
            }

            try {
                let access_token = localStorage.getItem('access_token');
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
               
               
                await axios.post("http://127.0.0.1:8081/api/albums", this.album);
               
                this.$router.push("/chome");
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.addAlbum();
                } else {
                    console.error('Error adding album:', error);
                    alert('An error occurred while adding album.');
                }
            }
        }
    }
}
</script>

<style scoped>

</style>