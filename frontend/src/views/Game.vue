<template>
  <div class="game">
    <div class="play-area">
      <button @click="getSong" class="get-song nes-btn">Get a Song</button>

      <Song v-if="youtubeId" :youtubeId="youtubeId" />
      <Answers />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Song from '../components/Song.vue';
import Answers from '../components/Answers.vue';

export default defineComponent({
  name: 'Game',
  components: {
    Song,
    Answers,
  },
  methods: {
    getSong() {
      this.$store.dispatch('getSong');
    },
  },
  computed: {
    youtubeId() {
      return this.$store.getters.currentQuestionYoutubeId;
    },
  },
});

</script>
<style lang="scss" scoped>

.game {
  height: 80vh;
  display: flex;
  justify-content: center;

  .play-area {
    width: 80vw;
  }

  .get-song {
    margin-bottom: 40px;
  }
}

</style>
