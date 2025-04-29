<template>
  <div>
    <h1>Songs Not in Playlist</h1>
    <ul>
      <li v-for="song in songsNotInPlaylist" :key="song.song_id">
        {{ song.song_name }} - {{ song.song_artist }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allSongs: [],
      playlistSongs: [],
      songsNotInPlaylist: [],
      playlistId: 1 
    };
  },
  mounted() {
    this.fetchAllSongs();
    this.fetchPlaylistSongs(this.playlistId);
  },
  methods: {
    fetchAllSongs() {
      fetch('/api/songs')
        .then(response => response.json())
        .then(data => {
          this.allSongs = data;
        })
        .catch(error => {
          console.error('Error fetching all songs:', error);
        });
    },
    fetchPlaylistSongs(playlistId) {
      fetch(`/api/playlist/${playlistId}/song`)
        .then(response => response.json())
        .then(data => {
          this.playlistSongs = data;
          this.calculateSongsNotInPlaylist();
        })
        .catch(error => {
          console.error('Error fetching playlist songs:', error);
        });
    },
    calculateSongsNotInPlaylist() {
      const playlistSongIds = this.playlistSongs.map(song => song.song_id);
      this.songsNotInPlaylist = this.allSongs.filter(song => !playlistSongIds.includes(song.song_id));
    },
    addToPlaylist(songId) {
      
      console.log('Adding song with ID', songId, 'to playlist');
    },
    removeFromPlaylist(songId) {
      
      console.log('Removing song with ID', songId, 'from playlist');
    }
  }
};
</script>

<style scoped>

</style>
