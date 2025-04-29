<template>
  <div class="container">
    <h2>Give Song Review</h2>
    <div class="star-container">
      <span v-for="star in 5" :key="star" @click="selectRating(star)" :class="{ 'selected': star <= selectedStars }">★</span>
    </div>
    <button @click="submitReview">Submit Review</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<template>
  <div class="container">
    <h2>Give Song Review</h2>
    <div class="star-container">
      <span v-for="star in 5" :key="star" @click="selectRating(star)" :class="{ 'selected': star <= selectedStars }">★</span>
    </div>
    <button @click="submitReview">Submit Review</button>
  </div>
</template>

<script>
import axios from 'axios';
import refreshAccessToken from '@/utils/refreshToken';

export default {
  data() {
    return {
      selectedStars: 0,
      songId: null,
      userId: null,
    };
  },
  created() {
    this.songId = this.$route.params.songId;
    this.userId = localStorage.getItem('user_id');
  },
  methods: {
    selectRating(star) {
      this.selectedStars = star;
    },
    async submitReview() {
      try {
        const access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const response = await axios.post(`http://localhost:8081/api/review/${this.songId}`, {
          user_id: this.userId,
          review: this.selectedStars,
        });
        console.log(response.data);
        this.$router.go(-1); // Redirect to previous page upon success
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken();
          await this.submitReview();
        } else {
          
          this.$router.go(-1);
        }
      }
    },
  },
};
</script>



<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.star-container {
  font-size: 40px;
}

.selected {
  color: yellow;
}

.error-message {
  color: red;
}
</style>
