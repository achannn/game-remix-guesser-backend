<template>
  <div class="submit-ocremix-id">
    <input v-model="secretId" placeholder="Input Secret ID" />
    <input v-model="publicId" placeholder="Input Public ID" />
    <button @click="submitIds">Check</button>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'CompareIDs',
  data() {
    return {
      secretId: '',
      publicId: '',
    };
  },
  methods: {
    submitIds() {
      const data = {
        public_id: Number(this.publicId),
        secret_id: Number(this.secretId),
      };
      this.$store.dispatch('checkAnswer', data);
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
