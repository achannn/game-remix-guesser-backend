<template>
  <div class="game">
    <div class="play-area">
      <button @click="getSong" class="get-song nes-btn">Get a Song</button>

      <Song v-if="youtubeId" :youtubeId="youtubeId" />
      <Answers v-if="youtubeId" />
      <RemixInfo v-if="correctAnswer" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Song from '../components/Song.vue';
import Answers from '../components/Answers.vue';
import RemixInfo from '../components/RemixInfo.vue';

export default defineComponent({
  name: 'Game',
  components: {
    Song,
    Answers,
    RemixInfo,
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
    correctAnswer() {
      return this.$store.getters.correctAnswer;
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
