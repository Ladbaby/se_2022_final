<template>
  <Transition name="slide" mode="out-in">
    <div id="not-logged-in" v-if="!ifLoggedIn">
      <img
        alt="Vue logo"
        :src="require('@/icons/logo.png')"
        style="width: 150px; height: 150px"
        draggable="false"
      />
      <Transition name="slide-up" mode="out-in">
        <LoginWindow
          v-if="currentWindow === 'LoginWindow'"
          @login="login"
          @register="register"
        />
        <RegisterWindow
          v-else-if="currentWindow === 'RegisterWindow'"
          @cancel="cancel"
        />
      </Transition>
    </div>
    <div id="logged-in" v-else-if="ifLoggedIn">
      <MainUI @log-out="handleLogout" :ifLoggedIn="ifLoggedIn"/>
    </div>
  </Transition>
</template>

<script>
import LoginWindow from "./components/Login.vue";
import RegisterWindow from "./components/Register.vue";
import MainUI from "./components/MainUI.vue";
import Cookies from "js-cookie";
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  name: "App",
  components: {
    LoginWindow,
    RegisterWindow,
    MainUI,
  },
  data() {
    return {
      windowList: ["LoginWindow", "RegisterWindow"],
      currentWindow: "LoginWindow",
      ifLoggedIn: false,
    };
  },
  methods: {
    register() {
      this.currentWindow = "RegisterWindow";
    },
    cancel() {
      this.currentWindow = "LoginWindow";
    },
    async login(userName, password) {
      var csrftoken = Cookies.get("csrftoken");
      const loginResult = await axios
        .post(
          "login/",
          {
            auth: {
              "user-name": userName,
              "password": password,
            },
          },
          {
            headers: {
              "Content-Type": "application/json;charset=UTF-8",
              "X-CSRFToken": csrftoken,
            },
          }
        )
        .then(function (response) {
          return response;
        })
        .catch(function (error) {
          console.log(error);
          return error;
        });
      const statusCode = loginResult["status"];
      if (statusCode == "200") {
        this.ifLoggedIn = true;
        ElMessage({
          type: "success",
          message: "Successfully login",
        });
      } else {
        ElMessage.error(
          "Login failed! Please check your user name and password!"
        );
      }
    },
    async handleLogout() {
      var csrftoken = Cookies.get("csrftoken");
      await axios
        .post(
          "logout/",
          {},
          {
            headers: {
              "X-CSRFToken": csrftoken,
            },
          }
        )
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      this.ifLoggedIn = false;
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-image: url("https://cn.bing.com/th?id=OHR.SeitanLimania_ZH-CN3831790369_UHD.jpg&rf=LaDigue_UHD.jpg&w=3840&h=2160&c=8&rs=1&o=3&r=0");
  background-attachment: fixed;
  background-size: cover;
  background-repeat: no-repeat;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
.slide-up-enter-active {
  animation: bounceIn;
  animation-duration: 0.5s;
}
.slide-enter-active {
  animation: fadeIn;
  animation-duration: 0.5s;
}
.slide-up-leave-active {
  animation: backOutDown;
  animation-duration: 0.2s;
}
.slide-leave-active {
  animation: backOutRight;
  animation-duration: 0.5s;
}
#not-logged-in {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
#logged-in {
  width: 100%;
  height: 100%;
}
</style>
