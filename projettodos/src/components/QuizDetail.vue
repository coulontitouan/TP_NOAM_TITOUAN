<template>
  <div>
    <NewQuestionForm v-if="showNewQuestionForm" @questionCreated="createdQuestion" @cancel="cancelAddQuestion" :quizId="selectedQuiz.id" />
    <div v-else>
      <h1>Détails du Quiz</h1>
      <h2>{{ quizName }}</h2>
      <p>Questions:</p>
      <ul>
        <li v-for="question in selectedQuiz.questions" :key="question.id">
          {{ question.title }}
          {{ question.choices.length }} choix
          <button @click="deleteQuestion(question)">Supprimer la question</button>
          <button @click="editQuestionName(question)">Modifier le Nom de la Question</button>
        </li>
      </ul>
      <button @click="deleteQuiz">Supprimer le Quiz</button>
      <button @click="editQuizName">Modifier le Nom du Quiz</button>
      <button @click="goBack">Retour</button>
      <button @click="showNewQuestionForm = true">Ajouter une question</button>
    </div>
  </div>
</template>

<script>
import NewQuestionForm from './NewQuestionForm.vue';

export default {
  props: {
    selectedQuiz: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      quizName: '',
      showNewQuestionForm: false
    };
  },
  methods: {
    async getQuizName() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${this.selectedQuiz.id}`);
        const data = await response.json();
        this.quizName = data.name;
      } catch (error) {
        console.error('Erreur lors de la récupération du nom du quiz:', error);
      }
    },
    deleteQuiz() {
      if (confirm("Êtes-vous sûr de vouloir supprimer ce quiz ?")) {
        this.$emit('deleteQuiz', this.selectedQuiz);
      }
    },
    deleteQuestion(question) {
      if (confirm("Êtes-vous sûr de vouloir supprimer cette question ?")) {
        this.$emit('deleteQuestion', question);
      }
    },
    goBack() {
      this.$emit('goBack');
    },
    async editQuizName() {
      const newQuizName = prompt("Entrez le nouveau nom du Quiz:", this.quizName);
      if (newQuizName !== null) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${this.selectedQuiz.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: newQuizName })
          });

          if (!response.ok) {
            throw new Error('Failed to update quiz name');
          }

          this.quizName = newQuizName;
        } catch (error) {
          console.error('Erreur lors de la modification du nom du quiz:', error);
        }
      }
    },
    cancelAddQuestion() {
      this.showNewQuestionForm = false;
    },
    createdQuestion() {
      this.showNewQuestionForm = false;
      this.$emit('questionCreatedToApp', this.selectedQuiz.url);
    },
    editQuestionName(question) {
  const newQuestionTitle = prompt("Entrez le nouveau titre de la question:", question.title);
  if (newQuestionTitle !== null) {
    fetch(`${question.url}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title: newQuestionTitle })
    })
    .then(response => {
      if (response.ok) {
        question.title = newQuestionTitle;
      } else {
        console.error('Failed to update question name');
      }
    })
    .catch(error => {
      console.error('Error updating question name:', error);
    });
  }
}

  },
  components: {
    NewQuestionForm
  },
  mounted() {
    this.getQuizName();
  }
};
</script>


<style>

  button{
    margin: 25px;
  }

</style>