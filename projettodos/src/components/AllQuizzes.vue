// AllQuizzes.vue
<template>
  <div>
    <h1>Tous les Quizzes</h1>
    <ul>
      <li v-for="quiz in quizzes" :key="quiz.id">
        {{ quiz.name }}
        {{ quiz.questions.length }} questions
        <button @click="viewQuizDetail(quiz)">Voir détails</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    quizzes: {
      type: Array,
      required: true
    }
  },
  methods: {
    viewQuizDetail(quiz) {
      this.$emit('viewQuizDetail', quiz); // Émet un événement vers le composant parent pour afficher les détails du quiz sélectionné
    }
  }
};
</script>
