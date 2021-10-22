<template>
    <div class="song">
        <div class="youtube-wrapper">
            <youtube :video-id="youtubeId" ref="youtube" />
        </div>
        <button @click="play">Play!</button>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import youtube from '../plugins/vue-youtube';

export default defineComponent({
  name: 'Song',
  props: {
    youtubeId: String,
  },
  components: {
    youtube,
  },
  methods: {
    play() {
      // eslint-disable-next-line
      // @ts-ignore
      this.player.playVideo();
    },
  },
  computed: {
    player(): any {
      // eslint-disable-next-line
      // @ts-ignore
      return this.$refs.youtube.player;
    },
  },
});

</script>
<style lang="scss" scoped>

.youtube-wrapper {
  display: none;
}
</style>
