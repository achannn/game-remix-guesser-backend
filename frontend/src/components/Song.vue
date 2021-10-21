<template>
    <div class="song">
        <div class="youtube-wrapper">
            <youtube :video-id="id" ref="youtube" />
        </div>
        <button @click="play">Play!</button>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { getIdFromUrl } from 'vue-youtube';
import youtube from '../plugins/vue-youtube';

export default defineComponent({
  name: 'Song',
  data() {
    return {
      youtubeId: getIdFromUrl('https://www.youtube.com/watch?v=1xhghJVj2KE'),
      id: 'ZVMigc6aQl0',
    };
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
    player() {
      console.log(this.$refs.youtube);
      // eslint-disable-next-line
      // @ts-ignore
      return this.$refs.youtube.player;
    },
  },
});

</script>
<style lang="scss" scoped>

.youtube-wrapper {
    opacity: 0;
}
</style>
