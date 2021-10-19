<template>
  <div class="home">
    <SubmitOcremixId />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import SubmitOcremixId from '@/components/SubmitOcremixId.vue';

export default defineComponent({
  name: 'Home',
  components: {
    SubmitOcremixId,
  },
  mounted() {
    this.$store.dispatch('getRemixes');
  },
});
</script>
