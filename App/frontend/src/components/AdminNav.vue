<template>
    <div>
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Admin Page</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="/chome">Homepage</a>
              </li>
              <li class="nav-item">
                <router-link to="/creatorpage" class="nav-link active" aria-current="page" >Creator Page</router-link>
              </li>
              <li class="nav-item">
                <a class="btn btn-primary" href="#" @click="logoutUser">Logout</a>
              </li>
              
            </ul>
            <form class="d-flex" @submit.prevent="search">
  <input v-model="searchTerm" class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
  <button class="btn btn-outline-success" type="submit">Search</button>
</form>

          </div>
        </div>
      </nav>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'adminNav',
    data() {
    return {
      searchTerm: ""
    };
  },
    

    methods: {
        async logoutAdmin() {
            try {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user_mail')

                alert('Admin Successfully logged out !!')
                this.$router.push('/login')
            }
            catch (error) {
                console.log(error)
            }
        },
        async search() {
  try {
    const response = await axios.post("http://127.0.0.1:8081/api/search", {
      q: this.searchTerm
    });

    const searchResults = response.data;
    
    this.$router.push({ path: '/search_result', query: { results: JSON.stringify(searchResults) } });
  } catch (error) {
    console.error("An error occurred while searching:", error);
   
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
    }
}

</script>

<style scoped>

nav{
    background-color: aqua;
}



#outer_div {
    border: 1px solid black;
}

.col-2 {
    margin: 0;
    padding: 0;
}

.col-2 .col {
    margin: 0;
    padding: 0;
}

.col-4 {
    margin: 0;
    padding: 5px 0 0 0;
}

img {
    margin: 0;
    height: 35px;
    width: 120.5px;
}

#Admin_blink {
    animation: animate 3s linear infinite;
}

@keyframes animate {
    0% {
        opacity: 0.3;
    }

    50% {
        opacity: 0.7;
    }

    100% {
        opacity: 1;
    }
}


#links:hover {
    color: rgb(250, 250, 252);
    font-weight: bolder;
}

#link_logout:hover {
    color: red;
    font-weight: bolder;
}
</style>