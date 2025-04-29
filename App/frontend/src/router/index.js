import Vue from "vue";
import VueRouter from "vue-router";

import RegisterView from "../views/auth/RegisterView.vue";
import LoginView from "../views/auth/LoginView";
import commonHomeView from "@/views/home/commonHomeView.vue";
import AddSongsView from "../views/songs/AddSongsView.vue";
import AddAlbumsView from "../views/songs/AddAlbumsView.vue";
import AddPlaylistsView from "../views/songs/AddPlaylistsView.vue";
import adminDashboard from "../views/admin/adminDashboard.vue";
import CreatorPageView from "../views/user/CreatorPageView.vue";
import DeleteSongsView from "../views/songs/DeleteSongsView.vue";
import UpdateSongView from "@/views/songs/UpdateSongView.vue";
import DeleteAlbums from "../views/songs/DeleteAlbums.vue";
import UpdateAlbumsView from "../views/songs/UpdateAlbumsView.vue";
import LandingView from "../views/user/LandingView.vue" ;
import CreatorHomeView from "../views/home/CreatorHomeView.vue";
import RegisterCreatorView from "@/views/auth/RegisterCreatorView.vue";
import AddDelSongAlbum from "@/views/songs/AddDelSongAlbum.vue";
import SongRatingsView from "@/views/user/SongRatingsView.vue";
import AlbumSongsView from "../views/songs/AlbumSongsView.vue";
import DeletePlaylists from "../views/songs/DeletePlaylists";
import AddDelSongstoPlaylists from "@/views/songs/AddDelSongstoPlaylists.vue";
import ViewPlaylist from "@/views/songs/ViewPlaylist.vue"
import SearchResults from '@/components/SearchResults.vue'; 
import SelectALbumtoAddDelSon from "../views/songs/SelectALbumtoAddDelSon.vue"
import BlockUnblock from "@/views/auth/BlockUnblock.vue";
import TrendsPage from "../views/songs/TrendsPage.vue";



Vue.use(VueRouter)

const routes = [
    {
        path:"/",
        name: "Landing-Page",
        component: LandingView,
    },
    {
        path:"/home",
        name: "Home-Page",
        component: commonHomeView,
    },
    {
        path:"/chome",
        name: "Chome-Page",
        component: CreatorHomeView,
    },
    {
        path:"/regis_Create",
        name: "RegCreate-Page",
        component: RegisterCreatorView,
    },
       
    {
        path:"/register",
        name: "Registration-Page",
        component: RegisterView,
    },
    {
        path:"/login",
        name: "Login-Page",
        component: LoginView,
    },
    {
        path:"/add_song",
        name: "Add_Song-Page",
        component: AddSongsView,
    },
    {
        path:"/add_album",
        name: "Add_Album-Page",
        component: AddAlbumsView,
    },
    {
        path:"/delete_album",
        name: "Delete_Album-Page",
        component: DeleteAlbums,
    },
    {
        path:"/update_album",
        name: "Update_Album-Page",
        component: UpdateAlbumsView,
    },
    {
        path:"/add_playlist",
        name: "Add_Playlist-Page",
        component: AddPlaylistsView,
    },
    {
        path:"/admin/dashboard",
        name: "Addmin_Dashboard",
        component: adminDashboard,
    },
    {
        path:"/creatorpage",
        name: "Creator-Page",
        component: CreatorPageView,
    },
    {
        path:"/delsong",
        name: "Delete-Song",
        component: DeleteSongsView,
    },
    {
        path:"/updateSong",
        name: "Update-Song",
        component: UpdateSongView,
    },
    {
        path:"/addDel_son_alb/:albumId",
        name: "Add_Del_Song_album",
        component: AddDelSongAlbum,
    },
    {
        path:"/song_rate/:songId",
        name: "Add_Song_rate",
        component: SongRatingsView,
    },
    {
        path: "/album/:albumId",
        name: 'AlbumSongs',
        component: AlbumSongsView,
      },
    {
        path: "/delete_playlists",
        name: 'Delete-Playlists',
        component: DeletePlaylists,
      },
    {
        path: "/add_del_son_playlist/:playlistId",
        name: 'Add-DelSong_Playlists',
        component: AddDelSongstoPlaylists,
      },
    {
        path: "/view_play/:playlistId",
        name: 'View_Playlists',
        component: ViewPlaylist,
      },      
    {   path: '/search_result',
        name: 'Search_Result',
        component: SearchResults, 
      },
      { path: '/select_alb_add_del',
        name: 'SelAddDel',
        component: SelectALbumtoAddDelSon, 
    },
      { path: '/block_unblock',
        name: 'BlockUnblock',
        component: BlockUnblock, 
    },
      { path: '/trending',
        name: 'TrendsPage',
        component: TrendsPage, 
    }
      
      

];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router