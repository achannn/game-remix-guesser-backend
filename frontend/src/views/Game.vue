<template>
  <div class="game">
      <Song />
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
  },
});

</script>
<style lang="scss" scoped>

.game {
    height: 80vh;
}

</style>
