<template>
  <div class="answers nes-container with-title">
    <transition name="slide-fade" mode="out-in">
    <h3 id="answer-area-title" class="title" :key="titleText">
      {{titleText}}
    </h3>
    </transition>
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
      submitted: false,
    };
  },
  methods: {
    submitAnswer() {
      this.$store.commit('setHasCheckedAnswer', false);
      this.submitted = true;
      this.$store.dispatch('submitAnswer');
    },
  },
  computed: {
    choices() {
      return this.$store.getters.currentQuestionChoices;
    },
    titleText() {
      if (this.submitted) {
        return 'Checking...';
      }
      if (this.hasCheckedAnswer) {
        return 'Sorry, wrong! Which game is this from?';
      }
      return 'Which game is this from?';
    },
    hasCheckedAnswer() {
      return this.$store.getters.hasCheckedAnswer;
    },
  },
  watch: {
    // Why does a String need Deep????
    selectedChoice: {
      handler() {
        this.$store.commit('setSelectedChoice', Number(this.selectedChoice));
      },
      deep: true,
    },
    hasCheckedAnswer() {
      if (this.hasCheckedAnswer) {
        this.submitted = false;
      }
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
.slide-fade-enter-active {
  transition: all .3s ease;
}
.slide-fade-leave-active {
  /* transition: all .2s cubic-bezier(1.0, 0.5, 0.8, 1.0); */
  transition: all .2s ease;
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active for <2.1.8 */ {
  transform: rotate(1.0turn);
  opacity: 1;
}
</style>
