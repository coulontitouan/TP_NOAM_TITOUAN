<template>
    <div>
      <h1>Créer une nouvelle Question</h1>
      <form @submit.prevent="createQuestion">
        <label for="questionTitle">Titre de la question:</label>
        <input type="text" id="questionTitle" v-model="questionTitle" required>
        <label for="proposition1">Titre de la 1ere proposition:</label>
        <input type="text" id="proposition1" v-model="proposition1" required>
        <label for="proposition2">Titre de la 2eme proposition:</label>
        <input type="text" id="proposition2" v-model="proposition2" required>
        <button type="submit">Créer</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        questionTitle: ''
      };
    },
    methods: {
      async createQuestion() {
  try {
    const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${this.quizId}/questions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        quiz_id: this.quizId,
        type: 'multiple', 
        title: this.questionTitle,
        proposition1:this.proposition1,
        proposition2:this.proposition2,
        answer: this.answer 
      })
    });

    if (!response.ok) {
      throw new Error('Failed to create new question');
    }

    this.$emit('questionCreated');
    this.questionTitle = '';
    this.answer = ''; 
  } catch (error) {
    console.error('Erreur lors de la création de la nouvelle question:', error);
  }
}


    },
    props: {
      quizId: {
        type: Number,
        required: true
      }
    }
  };
  </script>
  