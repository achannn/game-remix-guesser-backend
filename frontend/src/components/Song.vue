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

// eslint-disable-next-line
// ts-ignore
function getYoutubeIdFromUrl(url: any) {
  // eslint-disable-next-line
  // ts-ignore
  const blah = url.split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
  // eslint-disable-next-line
  // ts-ignore
  // eslint-disable-next-line
  return (blah[2] !== undefined) ? blah[2].split(/[^0-9a-z_\-]/i)[0] : blah[0];
}

export default defineComponent({
  name: 'Song',
  data() {
    return {
      youtubeId: getYoutubeIdFromUrl('https://www.youtube.com/watch?v=1xhghJVj2KE'),
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
