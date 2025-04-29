<template>
  <div>
    <h1>Search Results</h1>
    <div v-if="searchResults">
      <h2>{{ searchResults.search_word }}</h2>
      <div v-if="searchResults.songs.length > 0">
        <h3>Songs:</h3>
        <div class="container text-center">
          <div class="row">
            <div class="col column">
              <div v-for="song in searchResults.songs" :key="song.song_id">
                <div class="card float-start" style="width: 20rem; margin:10px;">
                  <img src="" class="card-img-top" alt="">
                  <div class="card-body">
                    <h5 class="card-title">{{ song.song_name }}</h5>
                    <p class="card-text">{{ song.song_artist }} <br><audio controls>
                      <source :src="base_url + song.song_path" type="audio/mpeg">
                    </audio></p>
                    <a :href="'/song_rate/' + song.song_id" class="btn btn-primary">Give Ratings</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="searchResults.albums.length > 0">
        <h3>Albums:</h3>
        <div class="container text-center">
          <div class="row">
            <div class="col column">
              <div v-for="album in searchResults.albums" :key="album.album_id">
                <div class="card float-start" style="width: 25rem; margin:10px;">
                  <img src="" class="card-img-top" alt="">
                  <div class="card-body">
                    <h5 class="card-title">{{ album.album_name }}</h5>
                    <p class="card-text">{{ album.song_artist }}</p>
                    <a :href="'/album/' + album.album_id" class="btn btn-primary">View Album</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="searchResults.songs.length === 0 && searchResults.albums.length === 0">
        <p>No results found.</p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'SearchResult',

  data() {
    return {
      searchResults: null,
      base_url: "http://localhost:8081"
      
    };
  },
  created() {
    this.searchResults = JSON.parse(this.$route.query.results);
  }
};
</script>
