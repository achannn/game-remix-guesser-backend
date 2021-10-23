<template>
  <div class="maintenance">
    <SubmitOcremixId />
    <GenerateQuestionButton />
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import SubmitOcremixId from '../components/SubmitOcremixId.vue';
import GenerateQuestionButton from '../components/GenerateQuestionButton.vue';

const Maintenance = defineComponent({
  name: 'Maintenance',
  components: {
    SubmitOcremixId,
    GenerateQuestionButton,
  },
});

export default Maintenance;

</script>
<style scoped lang="scss">
@import '../colors';

.title {
  background-color: $lightCornflowerBlue !important;
}

</style>
