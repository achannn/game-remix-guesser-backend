<template>
  <div class="home">
      <section class="introduction nes-container is-rounded">
          <p>Welcome to the Game Music Guessing Game!</p>
          <p>To play, click the "Play" button below.</p>
          <button @click="goToGame" class="play nes-btn">Play</button>
          <h2>Instructions</h2>
          <p>You will be presented with a "play song" button.
              When you click it, music will start playing,
              and four video game titles will display as radio items.</p>
          <p>When you think you know which game the song is derived from,
              choose it in the list, and click "Submit my Guess"</p>
          <p>The game will tell you whether you chose properly or not,
              and show you some more information about the song,
              such as the Ocremix where you listen to more music by the artist.</p>
          <p>Then, you can get a new song by clicking "next song".</p>
          <p>The game runs indefinitely, play as long as you like!</p>
      </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Home',
  components: {
  },
  methods: {
    goToGame() {
      this.$router.push({ name: 'Game' });
    },
  },
});

</script>
<style lang="scss" scoped>

.home {
    display: flex;
    justify-content: center;
}
.introduction {
    width: 80vw;
    margin-bottom: 18px;
}
.play {
    margin-bottom: 16px;
}
</style>
