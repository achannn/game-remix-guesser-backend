<template>
  <div class="submit-ocremix-id">
    <input v-model="ocremixId" placeholder="Input ID" />
    <button @click="submitId">Submit</button>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'SubmitOcremixId',
  data() {
    return {
      ocremixId: '',
    };
  },
  methods: {
    submitId() {
      this.$store.dispatch('submitRemixForParsing', this.ocremixId);
    },
  },
});
</script>
<style scoped lang="scss">
  .submit-ocremix-id {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-flow: column;
    * {
      margin: 5px;
    }

    input {
      padding: 5px;
    }
    button {
      height: 2em;
    }
  }
</style>
