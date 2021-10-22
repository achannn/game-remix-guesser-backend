<template>
  <div class="game">
      <button @click="getSong" class="get-song nes-btn">Get a Song</button>

      <Song v-if="youtubeId" :youtubeId="youtubeId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Song from '../components/Song.vue';

export default defineComponent({
  name: 'Game',
  components: {
    Song,
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

  .get-song {
    margin-bottom: 40px;
  }
}

</style>
