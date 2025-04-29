<template>
    <div>
        <div class="container ">
            <div class="row">
                <div class="col-4"></div>
                <div class="col">
                    <br><br>
                    <p>Update Song</p>
                    <form @submit.prevent="updateSong">
                        <div class="mb-3">
                            <label for="song">Select Song:</label>
                            <select v-model="selectedSong" class="form-select" required>
                                <option v-for="song in songs" :key="song.song_id" :value="song.song_id">{{ song.song_name }}</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="newTitle">New Song Title:</label>
                            <input type="text" v-model="newTitle" class="form-control" :placeholder="selectedSong ? getSelectedSongName() : 'Select a song first'">
                        </div>
                        <div class="mb-3">
                            <label for="newArtist">New Artist Name:</label>
                            <input type="text" v-model="newArtist" class="form-control" :placeholder="selectedSong ? getSelectedSongArtist() : 'Select a song first'" >
                        </div>
                        <button type="submit" class="btn btn-primary">Update Song</button>
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
import { refreshPage } from '@/utils/refreshpage';

export default {
    name: "UpdateSong",
    data() {
        return {
            song_id:this.$route.params.id,
            selectedSong: null,
            newTitle: '',
            newArtist: '',
            songs: []
        }
    },
    async mounted() {
        await this.fetchSongs();
    },
    methods: {
        async fetchSongs() {
            try {
                let response = await axios.get("http://127.0.0.1:8081/api/songs");
                this.songs = response.data;
            } catch (error) {
                console.error('Error fetching songs:', error);
            }
        },
        async updateSong() {
            

            try {
                let access_token = localStorage.getItem('access_token');
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

                await axios.put(`http://127.0.0.1:8081/api/song/${this.selectedSong}`, {
                    song_name: this.newTitle,
                    song_artist: this.newArtist
                });

                alert('Song updated successfully.');
                this.fetchSongs();
                
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.updateSong();
                    refreshPage();
                } else {
                    console.error('Error updating song:', error);
                    alert('An error occurred while updating song.');
                }
            }
        },
        getSelectedSongName() {
            const selectedSong = this.songs.find(song => song.song_id === this.selectedSong);
            return selectedSong ? selectedSong.song_name : '';
        },
        getSelectedSongArtist() {
            const selectedSong = this.songs.find(song => song.song_id === this.selectedSong);
            return selectedSong ? selectedSong.song_artist : '';
        }
    }
}
</script>

<style scoped>

</style>
