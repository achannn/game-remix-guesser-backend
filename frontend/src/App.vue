<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </div>
  <router-view/>
  <div class="grass"></div>
  <div class="ground"></div>
</template>

<style lang="scss">
@import 'colors';

* {
  font-family: "Press Start 2P";
}
body {
    background-color: $saddleBrown;
}
.grass {
    height: 2vh;
    background-color: $lawnGreen;
}
.ground {
    height: 2vh;
    background-color: $darkGreen;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: $lightCornflowerBlue;

}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
