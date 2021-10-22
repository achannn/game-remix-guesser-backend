<template>
  <div class="answers nes-container with-title">
    <h3 id="answer-area-title" class="title">Which game is this from?</h3>
    <ul class="answer-list-area" role="radiogroup" aria-labelledby="answer-area-title">
      <li
        v-for="choice in choices"
        :key="choice.public_id"
      >
        <label>
          <input
            class="nes-radio"
            type="radio"
            name="choice"
            v-model="selectedChoice"
            :value="choice.public_id" />
          <span>{{choice.origin_game}}</span>
        </label>
      </li>
    </ul>
    <button
      class="nes-btn"
      :class="{'is-disabled': !selectedChoice}"
      :disabled="!selectedChoice"
      @click="submitAnswer"
    >
      Submit Answer
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Answers',
  data() {
    return {
      selectedChoice: '',
    };
  },
  methods: {
    submitAnswer() {
      this.$store.dispatch('submitAnswer');
    },
  },
  computed: {
    choices() {
      return this.$store.getters.currentQuestionChoices;
    },
  },
  watch: {
    // Why does a String need Deep????
    selectedChoice: {
      handler() {
        console.log('selected choice changed', this.selectedChoice);
        this.$store.commit('setSelectedChoice', Number(this.selectedChoice));
      },
      deep: true,
    },
  },
});

</script>
<style lang="scss" scoped>
@import '../colors';

.answers {
  margin-top: 30px;
}

ul, li {
  list-style-type: none;
  argin-block-start: 0;
  margin-block-end: 0;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  padding-inline-start: 0px;
}
.nes-radio:checked:focus+span::before {
  color: black;
}
.title {
  background-color: $lightCornflowerBlue !important;
}
</style>
