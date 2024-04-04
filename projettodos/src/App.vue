<template>
  <div id="app">
    <div v-if="selectedQuiz">
      <QuizDetail :selectedQuiz="selectedQuiz" @questionCreatedToApp="questionCreated" @goBack="showAllQuizzes" @deleteQuiz="deleteQuiz" @deleteQuestion="deleteQuestionFromQuiz" />
    </div>
    <div v-else-if="addingNewQuiz">
      <NewQuizForm @cancel="cancelAddingNewQuiz" @quizCreated="fetchQuizzes" />
    </div>
    <div v-else>
      <AllQuizzes :quizzes="quizzes" @viewQuizDetail="showQuizDetail" />
      <button @click="addNewQuiz">Ajouter un nouveau quiz</button>
    </div>
  </div>
</template>

<script>
import AllQuizzes from './components/AllQuizzes.vue';
import QuizDetail from './components/QuizDetail.vue';
import NewQuizForm from './components/NewQuizForm.vue';

export default {
  data() {
    return {
      quizzes: [],
      selectedQuiz: null,
      addingNewQuiz: false
    };
  },
  methods: {
    addNewQuiz() {
      this.addingNewQuiz = true;
    },
    cancelAddingNewQuiz() {
      this.addingNewQuiz = false;
    },
    async showQuizDetail(quiz) {
      this.selectedQuiz = quiz;
    },
    showAllQuizzes() {
      this.selectedQuiz = null;
      this.fetchQuizzes();
    },
    async deleteQuiz(quiz) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${quiz.id}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          await this.fetchQuizzes();
          this.selectedQuiz = null;
        } else {
          console.error('Erreur lors de la suppression du quiz');
        }
      } catch (error) {
        console.error('Erreur lors de la suppression du quiz:', error);
      }
    },
    async deleteQuestionFromQuiz(question) {
      try {
        const response = await fetch(`${question.url}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          const quiz = await (await fetch(`${question.quiz_url}`)).json();
          this.selectedQuiz = quiz;
        } else {
          console.error('Erreur lors de la suppression de la question');
        }
      } catch (error) {
        console.error('Erreur lors de la suppression de la question:', error);
      }
    },
    async fetchQuizzes() {
      this.selectedQuiz = null;
      this.addingNewQuiz = false;
      try {
        const response = await fetch('http://127.0.0.1:5000/quiz/api/v1.0/quiz');
        const data = await response.json();
        this.quizzes = data;
      } catch (error) {
        console.error('Erreur lors de la récupération des quizzes:', error);
      }
    },
    async questionCreated(urlquiz) {
    this.selectedQuiz = await (await fetch(urlquiz)).json();
  },

  },
  components: {
    AllQuizzes,
    QuizDetail,
    NewQuizForm
  },
  mounted() {
    this.fetchQuizzes();
  },
};
</script>
