<template>
  <div class="game">
      <Song :youtubeId="youtubeId" />
      <button @click="getSong" class="nes-btn">Get a Song</button>
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
}

</style>
