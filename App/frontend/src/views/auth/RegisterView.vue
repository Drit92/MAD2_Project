<template>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-3"></div>
                <div class="col-6">
                    
                    <div class="inner-box">
                        <div class="buttons-div">
                            <div class="container text-center">
                                <div class="row">
                                    <div class="col-12">
                                    <h2> Register</h2> 
                                        
                                    </div>
                                    
                                </div>
                            </div>
                        </div>
                        <div>
                            <form>
                                <div class="mb-3">
                                    <input type="email" class="form-control" id="exampleInputEmail1" v-model="user_mail"
                                        required aria-describedby="emailHelp" placeholder="Enter email Address">
                                </div>
                                <div class="mb-3">
                                    <input type="password" class="form-control" id="exampleInputPassword1"
                                        v-model="password" required placeholder=" Enter password">
                                </div>
                                <div class="mb-3">
                                    <input type="text" class="form-control" v-model="re_password" required
                                        placeholder="Re-enter password">
                                </div>
                                <router-link to="/login">Login</router-link>
                                <button type="button" class="form-control" id="submit" @click="registerUser()">Register</button>
                                
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
    name: "RegisterUserView",
    data() {
        return {
            user_mail: "",
            password: "",
            re_password: "",
        };
    },
    methods: {
        registerUser() {
            if (!this.user_mail || !this.password || !this.re_password) {
                alert("All fields are required !!");
                return;
            }

            if (!this.user_mail.includes("@") || !this.user_mail.endsWith(".com")) {
                alert("Invalid email format !! Email must include '@' and end with '.com'");
                return;
            }

            if (this.password != this.re_password) {
                alert("Passwords don't match !!");
                return;
            }



            axios
                .post("http://127.0.0.1:8081/api/register", {
                    user_mail: this.user_mail,
                    password: this.password,
                })
                .then((response) => {
                    if (response.data.status === "success"){
                        alert("Successfully Registered !!")
                        this.$router.push("/login");
                    }
                    if (response.data.status === "failed"){
                        alert("User Already Exist. Use Forget password")
                        this.$router.push("/login");
                    }
                })
                .catch((error) => {
                    console.error(error);
                    alert("An error occurred while registering the user");
                });

        }

    }
}

</script>

<style scoped>




.inner-box {
    padding: 0px 20px 25px 20px;
}

.buttons-div {
    margin-top: 20px;
    padding: 0 20px 0 20px;
}

#outer_box {
    border: 1px solid black;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.current_btn {
    font-weight: 300;
    font: "Courier New";
    color: darkblue;
    background-color: rgb(214, 235, 250);
    border-radius: .2rem;
    border-width: 0.5px;
    border-color: rgb(62, 188, 230);
    width: 100%;
    padding-top: 7px;
    padding-bottom: 7px;
}

.other_btn {
    font-weight: 300;
    font: "Courier New";
    color: rgb(42, 56, 43);
    background-color: rgb(233, 234, 234);
    border-width: 0px;
    border-radius: .2rem;
    border-color: rgb(62, 188, 230);
    width: 100%;
    padding-top: 7px;
    padding-bottom: 7px;
    opacity: 0.8;
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
    margin-top: 200px;
    padding: 0;
    border: 1px solid black;
}
</style>
