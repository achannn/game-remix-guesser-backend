<template>
  <div class="home">
    <SubmitOcremixId />
    <GenerateQuestionButton />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import SubmitOcremixId from '@/components/SubmitOcremixId.vue';
import GenerateQuestionButton from '@/components/GenerateQuestionButton.vue';

export default defineComponent({
  name: 'Home',
  components: {
    SubmitOcremixId,
    GenerateQuestionButton,
  },
  mounted() {
    this.$store.dispatch('getRemixes');
  },
});
</script>
