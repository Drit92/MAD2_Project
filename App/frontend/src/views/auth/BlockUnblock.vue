<template>
    <div class="container">
      <div class="row">
        <!-- First column for blocking users -->
        <div class="col-md-6">
          <h2>Block Users</h2>
          <ul>
            <li v-for="user in users" :key="user.user_id">
              {{ user.user_mail }}
              <button @click="blockUser(user.user_id)">Block</button>
            </li>
          </ul>
        </div>
        <!-- Second column for unblocking users -->
        <div class="col-md-6">
          <h2>Unblock Users</h2>
          <ul>
            <li v-for="user in blockedUsers" :key="user.user_id">
              {{ user.user_mail }}
              <button @click="unblockUser(user.user_id)">Unblock</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'; 
  import refreshAccessToken from '@/utils/refreshToken'; 
  
  export default {
    data() {
      return {
        users: [],
        blockedUsers: []
      };
    },
    mounted() {
      // Fetch all users
      this.fetchAllUsers();
    },
    methods: {
      fetchAllUsers() {
        axios.get('http://127.0.0.1:8081/api/users')
          .then(response => {
            // Filter users based on their roles
            this.users = response.data.filter(user => !user.roles.includes('blocked'));
            this.blockedUsers = response.data.filter(user => user.roles.includes('blocked'));
          })
          .catch(error => {
            console.error('Error fetching users:', error);
          });
      },
      async blockUser(userId) {
        try {
          await this.refreshTokenAndCall(() => {
            return axios.post('http://127.0.0.1:8081/api/block', { user_id: userId });
          }, () => {
            this.fetchAllUsers(); // Refresh user list
          });
        } catch (error) {
          console.error('Error blocking user:', error);
        }
      },
      async unblockUser(userId) {
        try {
          await this.refreshTokenAndCall(() => {
            return axios.post('http://127.0.0.1:8081/api/unblock', { user_id: userId });
          }, () => {
            this.fetchAllUsers(); // Refresh user list
          });
        } catch (error) {
          console.error('Error unblocking user:', error);
        }
      },
      async refreshTokenAndCall(apiCall, successCallback) {
        try {
          let access_token = localStorage.getItem('access_token');
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
          await apiCall();
          successCallback();
        } catch (error) {
          if (error.response && error.response.status === 401) {
            await refreshAccessToken();
            await this.refreshTokenAndCall(apiCall, successCallback);
          } else if (error.response) {
            console.error("An error occurred while calling API:", error.response);
            throw error;
          }
        }
      }
    }
  };
  </script>
  
  
  <style scoped>
 
  </style>
  