<template>
    <div>
        <div> <admin-nav></admin-nav>
            
        </div>
        <router-link to="/block_unblock"><button>Block/Unblock Users</button></router-link> 
       
        <div>
            <h2>Admin Dashboard</h2>
            <div>
                <p>Total Users: {{ stats.total_users }}</p>
                <p>Total Blocked Users: {{ stats.total_blocked_users }}</p>
                <p>Total Songs: {{ stats.total_songs }}</p>
                <p>Total Albums: {{ stats.total_albums }}</p>
                <p>Total Artists: {{ stats.total_artists }}</p>
            </div>
        </div>
        
    </div>
</template>

<script>
import AdminNav from '../../components/AdminNav'
import axios from 'axios'
import refreshAccessToken from '@/utils/refreshToken';


export default {
    components: {
        'admin-nav': AdminNav
    },
    data() {
        return {
            stats: {}
        };
    },
    mounted() {
        this.fetchStats();
    },
    methods: {
        async fetchStats() {
            try {
                // const user_mail = localStorage.getItem("user_mail");
                // const user_id = localStorage.getItem("user_id");
                // const roles = localStorage.getItem("roles");
                let access_token = localStorage.getItem("access_token");

                axios.defaults.headers.common["Authorization"] = "Bearer " + access_token;

                const response = await axios.get("http://127.0.0.1:8081/api/stats");

                this.stats = response.data;
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.fetchStats();
                } else if (error.response) {
                    alert("An error occurred while fetching statistics");
                } else {
                    console.error("An unexpected error occurred:", error);
                }
            }
        }
    }
}
</script>

<style scoped>
button{
    position: fixed;
    top: 80px;
    right: 30px;
}
</style>
