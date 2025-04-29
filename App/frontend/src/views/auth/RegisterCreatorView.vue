<template>
  <div>
    <h1>Register Creator Page:</h1>
    <p>Register as Creator?</p>
    <button @click="handleYes">Yes</button>
    <button @click="handleNo">No</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    handleYes() {
  const userId = localStorage.getItem("user_id");
  if (userId) {
    axios.post('http://127.0.0.1:8081/api/reg_cre', { user_id: userId })
      .then(response => {
        console.log(response);
        this.$router.push('/chome');
      })
      .catch(error => {
        console.error(error);
        alert("Error occurred")
      });
  }
},
    handleNo() {
   
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>

</style>
