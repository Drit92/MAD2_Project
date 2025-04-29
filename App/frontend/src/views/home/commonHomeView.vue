<template>
  <div>
    <div>
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <a class="navbar-brand" href="/home">Home Page</a>
          
          
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            
            <span class="navbar-toggler-icon"></span>
          </button>
        
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">{{ user_mail }}</a>
              </li>
              <li class="nav-item">
                <a class="btn btn-primary" href="#" @click="logoutUser">Logout</a>
              </li>
            </ul>
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="/regis_Create">Register as Creator</a>
              </li>
            </ul>
            <div class="nav-item">
                <a class="btn " href="/trending" >Trending</a>
            </div>
            
            <form class="d-flex" @submit.prevent="search">
  <input v-model="searchTerm" class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
  <button class="btn btn-outline-success" type="submit">Search</button>
</form>

          </div>
        </div>
      </nav>
    </div>
    --
    <div>
      <div class="container text-center">
        <div class="row">
          <div class="col column">
          <h2>Songs :</h2>

          <div v-for="li in all_lists" :key="li.song_id">
              <div class="card float-start" style="width: 20rem; margin:10px;">
  <img src="" class="card-img-top" alt="">
  <div class="card-body">
    <h5 class="card-title">{{li.song_name}}</h5>
    <p class="card-text">{{li.song_artist}} <br><span style="color: #FFD700;">&#9733;</span>{{ li.song_avg_review.toFixed(2) }}<audio controls>
    
  <source :src="base_url+li.song_path" type="audio/mpeg">
</audio>

</p>
    
<a :href="`/song_rate/${li.song_id}`" class="btn btn-primary">Give Ratings</a>


   
  </div>
</div>
            --</div>
          

          </div>
          <div class="col column">
            <h2>Albums :</h2>

            <div v-for="list in alb_lists" :key="list.album_id">--
              <div class="card float-start" style="width: 25rem; margin:10px;">
  <img src="" class="card-img-top" alt="">
  <div class="card-body">
    <h5 class="card-title">{{list.album_name}}</h5>
    <p class="card-text">{{list.song_artist}}</p>
    <a :href="`/album/${list.album_id}`" class="btn btn-primary">View Album</a>
  </div>
</div>
            --</div>

            
          </div>
          
            

         




          <div class="col column"> 
            

            <h2>Your Playlists</h2>
    


    <div v-for="playlist in playlists" :key="playlist.playlist_id">-
              <div class="card float-start" style="width: 25rem; margin:10px;">
  <img src="" class="card-img-top" alt="">
  <div class="card-body">
    <h5 class="card-title">{{playlist.playlist_name}}</h5>
    <p class="card-text"></p>
    <a :href="`/view_play/${playlist.playlist_id}`" class="btn btn-primary mr-2">View Playlist</a><span style="margin-right: 6px;"></span>
    <a :href="`/add_del_son_playlist/${playlist.playlist_id}`" class="btn btn-primary">Add/Delete Songs</a>
  </div>
</div>
            -</div>


      

            
           <router-link to="/add_playlist"> <button type="button" class="btn btn-secondary btn-lg rr" @click="handleButtonClick">+</button></router-link>
          
          
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refreshToken';

export default {
  name: "HomeView",
  data() {
    return {
      user_mail: "",
      user_id: "",
      roles: "",
      all_lists: [],
      alb_lists: [],
      playlists: [],
      base_url: "http://localhost:8081",
      searchTerm: ""
    };
  },
  async created() {
    await this.allList();
    await this.albumList();
    await this.fetchPlaylists();
    
  },
  methods: {
    async allList() {
      try {
        this.user_mail = localStorage.getItem("user_mail");
        this.user_id = localStorage.getItem("user_id");
        let access_token = localStorage.getItem('access_token');
        this.roles = localStorage.getItem('roles');

        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const response = await axios.get("http://127.0.0.1:8081/api/songs");
        console.log(response.data);
        this.all_lists = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.allList();
        } else if (error.response) {
          alert("An error occurred while fetching songs data");
        }
      }
    },

    async fetchPlaylists() {
  try {
    
    
      this.user_mail = localStorage.getItem("user_mail");
      this.user_id = localStorage.getItem("user_id");
      let access_token = localStorage.getItem('access_token');
      this.roles = localStorage.getItem('roles');
      console.log("User ID:", this.user_id);

      axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
    const response = await axios.get(`http://127.0.0.1:8081/api/${this.user_id}/get_user_playlists`);

    console.log(response.data);
    this.playlists = response.data.playlists;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      await refreshAccessToken();
      await this.fetchPlaylists();
    } else if (error.response) {
      alert("An error occurred while fetching playlists data");
    }
  }
},




    async albumList() {
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const response = await axios.get("http://127.0.0.1:8081/api/albums");
        console.log(response.data);
        this.alb_lists = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.albumList();
        } else if (error.response) {
          alert("An error occurred while fetching albums data");
        }
      }
    },




    async search() {
  try {
    let access_token = localStorage.getItem('access_token');
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

    const response = await axios.post("http://127.0.0.1:8081/api/search", {
      q: this.searchTerm
    });

    const searchResults = response.data;
    // Redirect user to search result page
    this.$router.push({ path: '/search_result', query: { results: JSON.stringify(searchResults) } });
  } catch (error) {
    console.error("An error occurred while searching:", error);
    if (error.response && error.response.status === 401) {
      await refreshAccessToken();
      await this.search();
    } else {
     console.log(error);
      

    }
  }
},

async logoutUser() {
            try {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_mail');

                alert('User Successfully logged out !!');
                this.$router.push('/login');
            }
            catch (error) {
                console.log(error);
            }
        },


    

    handleButtonClick() {
     
      console.log("Button clicked");
    },
  },
};
</script>


<style scoped>
nav {
  background-color: aqua;

card{
 width: fit-content;
}
}
.rr {
  font-size: large;
  border-radius: 40px;
}



  .column {
    padding: 20px; 
    border: 1px solid #ccc; 
    border-radius: 10px; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
    background-color: #f9f9f9; 
    margin-left: 6px;
    overflow-y: scroll;
  }
</style>
