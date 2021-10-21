<template>
  <div class="home">
    <SubmitOcremixId />
    <GenerateQuestionButton />
    <CompareIDs />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import SubmitOcremixId from '@/components/SubmitOcremixId.vue';
import GenerateQuestionButton from '@/components/GenerateQuestionButton.vue';
import CompareIDs from '@/components/CompareSecretPublicIDs.vue';

export default defineComponent({
  name: 'Home',
  components: {
    SubmitOcremixId,
    GenerateQuestionButton,
    CompareIDs,
  },
  mounted() {
    this.$store.dispatch('getRemixes');
  },
});
</script>
