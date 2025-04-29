<template>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-3"></div>
                <div class="col-6">
                    
                    <div class="inner-box">
                        <div class="buttons-div">
                            <div class="container ">
                                <div class="row">
                                    <div class="col-12 text-center">
                                        <h2>Login</h2>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <form>
                                <div class="mb-3">
                                    Enter email :
                                    <input type="email" class="form-control" id="exampleInputEmail1" v-model="user_mail"
                                        aria-describedby="emailHelp" placeholder="Email Address">
                                </div>
                                <div class="mb-3">
                                    Enter password :
                                    <input type="password" class="form-control" id="exampleInputPassword1" v-model="password"
                                        placeholder="Password">
                                </div>
                                <router-link to="/register">Register </router-link>
                                <button type="submit" class="form-control" id="submit" @click.prevent="loginUser()">Login</button>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="col-3"></div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'LoginView',
    data() {
        return {
            user_mail: "",
            password: "",
            admin: false,
        }
    },
    methods: {
        loginUser() {
            if (!this.user_mail || !this.password) {
                alert("Please enter both the user mail and password");
                return;
            }
            axios.post("http://127.0.0.1:8081/api/login", {
                user_mail: this.user_mail,
                password: this.password,
            }).then((response) => {
                if (response.data.status === 'failed') {
                    alert(response.data.message)
                } else if (response.data.status === "success") {
                    const isAdmin = this.user_mail === "admin@gmail.com" && this.password === "1234";
                    if (isAdmin) {
                        this.admin = true; 
                        const access_token = response.data.access_token;
                        const refresh_token = response.data.refresh_token;
                        const user_mail = response.data.user_mail;
                        const user_id = response.data.user_id;
                        let roles= response.data.roles;
                        localStorage.setItem("access_token", access_token);
                        localStorage.setItem("refresh_token", refresh_token);
                        localStorage.setItem("user_mail", user_mail);
                        localStorage.setItem("user_id", user_id);
                        localStorage.setItem("roles", roles);
                        
                        
                        this.$router.push("/admin/dashboard");
                    } else {
                        const access_token = response.data.access_token;
                        const refresh_token = response.data.refresh_token;
                        const user_mail = response.data.user_mail;
                        const user_id = response.data.user_id;
                        let roles= response.data.roles;
                        localStorage.setItem("access_token", access_token);
                        localStorage.setItem("refresh_token", refresh_token);
                        localStorage.setItem("user_mail", user_mail);
                        localStorage.setItem("roles", roles);
                        localStorage.setItem("user_id", user_id);
                        this.$router.push("/home");

                    }
                }
            }).catch((error) => {
                console.error("Login Error:", error);
                alert(error.response.data.message);
            });
        }
    }
}
</script>

<style scoped>
.logo-div {
    background-color: rgb(74, 64, 161);
}
img {
    height: 30%;
    width: 30%;
}
.inner-box {
    padding: 0 20px 25px 20px;
}

form {
    margin-top: 20px;
    padding: 0 30px 0 30px;
}

#submit {
    background-color: blue;
    color: white;
    font-weight: bolder;
}

.col-6 {
    padding: 0;
    margin-top: 200px;
    border: 1px solid black;
}
</style>
