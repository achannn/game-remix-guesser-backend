<template>
  <div class="generate-question">
    <button @click="generateQuestion">Generate</button>
    <button class='seed' @click="seedDB">Seed</button>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'GenerateQuestionButton',
  data() {
    return {
      ocremixId: '',
    };
  },
  methods: {
    generateQuestion() {
      this.$store.dispatch('generateQuestion');
    },
    seedDB() {
      this.$store.dispatch('seedDB');
    },
  },
});
</script>
<style scoped lang="scss">
  .generate-question {
    display: flex;
    align-items: center;
    justify-content: center;
    * {
      margin: 5px;
    }

    button {
      height: 2em;
      background-color: #cdf4ff;
      &.seed {
        background-color: #cef400;
      }
    }
  }
</style>
