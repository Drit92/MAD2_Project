<template>
<div>
    <div  class="headbox"><h1>Creator's Page</h1></div>
    <div class="boxed">
        <ul> <h3>Songs</h3>
            <li><router-link to="/add_song">Add Songs </router-link></li>
            <li><router-link to="/updateSong"> Update songs</router-link></li>
            <li><router-link to="/delsong">Delete songs </router-link></li>
            
            

        </ul>

    </div>
    <div class="boxed">
        <ul><h3>Albums</h3>
            <li><router-link to="/add_album"> Add Albums</router-link></li>
            <li><router-link to="/update_album"> Update Albums</router-link></li>
            <li><router-link to="/delete_album"> Delete Albums</router-link></li>
            <li><router-link to="/select_alb_add_del"> Add / Delete Songs to Albums</router-link></li>
        </ul>

    </div>

    



</div>
</template>

<script>

</script>

<style>

.headbox{
    height:10vh;
    margin-top: 5px;
}


.boxed{
    border: none; 
    width: 95%;
    height: 20vh;
    margin-top: 10px;
    margin-left: 3%;
    align-items: center;
    background-color:rgb(247, 244, 249);
    /*#background-color: #a3b1d8;*/
    
}

</style>