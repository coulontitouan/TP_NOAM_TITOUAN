<template>
    <div>
        <NewQuestionForm v-if="showNewQuestionForm" @questionCreated="createdQuestion" @cancel="cancelAddQuestion"
            :quizId="selectedQuiz.id" />
        <div v-else>
            <h1>Détails du Quiz</h1>
            <h2>{{ quizName }}</h2>
            <p>Questions:</p>
            <ul>
                <li v-for="question in selectedQuiz.questions" :key="question.id">
                    {{ question.title }}
                    <ul>
                        <li>
                            {{ question.proposition1 }}<br>
                            <span v-if="question.proposition1 === question.answer">'Correcte'</span>
                            <button @click="definirReponse(question.id, 1)" v-else>Definir comme réponse</button>
                            <button @click="modifierReponse(question.id, 1)">Modifier la réponse</button>
                        </li>
                        <li>
                            {{ question.proposition2 }}<br>
                            <span v-if="question.proposition2 === question.answer">Correcte</span>
                            <button @click="definirReponse(question.id, 2)" v-else>Definir comme réponse</button>
                            <button @click="modifierReponse(question.id, 2)">Modifier la réponse</button>
                        </li>
                    </ul>
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
            async deleteQuiz() {
                if (confirm("Êtes-vous sûr de vouloir supprimer ce quiz ?")) {
                    try {
                        const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${this.selectedQuiz.id}`, {
                            method: 'DELETE'
                        });

                        if (!response.ok) {
                            throw new Error('Failed to delete quiz');
                        }

                        this.$emit('deleteQuiz', this.selectedQuiz);
                    } catch (error) {
                        console.error('Erreur lors de la suppression du quiz:', error);
                    }
                }
            },
            async deleteQuestion(question) {
                if (confirm("Êtes-vous sûr de vouloir supprimer cette question ?")) {
                    try {
                        const response = await fetch(question.url, {
                            method: 'DELETE'
                        });

                        if (!response.ok) {
                            throw new Error('Failed to delete question');
                        }

                        this.$emit('deleteQuestion', question);
                    } catch (error) {
                        console.error('Erreur lors de la suppression de la question:', error);
                    }
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
            async createdQuestion() {
                this.showNewQuestionForm = false;
                try {
                    const response = await fetch(this.selectedQuiz.url);
                    if (!response.ok) {
                        throw new Error('Failed to fetch quiz');
                    }
                    this.$emit('questionCreatedToApp', this.selectedQuiz.url);
                } catch (error) {
                    console.error('Erreur lors de la création de la question:', error);
                }
            },
            async editQuestionName(question) {
                const newQuestionTitle = prompt("Entrez le nouveau titre de la question:", question.title);
                if (newQuestionTitle !== null) {
                    try {
                        const response = await fetch(question.url, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ title: newQuestionTitle })
                        });

                        if (!response.ok) {
                            throw new Error('Failed to update question name');
                        }

                        question.title = newQuestionTitle;
                    } catch (error) {
                        console.error('Erreur lors de la modification du nom de la question:', error);
                    }
                }
            },
            async modifierReponse(questionId, proposition) {
                proposition = 'proposition' + proposition;
                let answer = false;
                const newProp = prompt(`Entrez le nouveau nom de la ${proposition}:`);
                if (this.selectedQuiz.answer === newProp) {
                    answer = true;
                }
                try {
                    const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${this.selectedQuiz.id}/questions/${questionId}`, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: `{"${proposition}": "${newProp}"${answer ? `,"answer": ${newProp}` : ""}}`
                    });

                    if (!response.ok) {
                        throw new Error('Failed to update question answer');
                    }

                    this.selectedQuiz.questions.find(question => question.id === questionId)[proposition] = newProp;
                } catch (error) {
                    console.error('Erreur lors de la modification de la réponse de la question:', error);
                }
            },
            async definirReponse(questionId, proposition) {
                proposition = 'proposition' + proposition;
                console.log(`{"answer": "${this.selectedQuiz.questions.find(question => question.id === questionId)[proposition]}"}`)
                try {
                    const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${this.selectedQuiz.id}/questions/${questionId}`, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: `{"answer": "${this.selectedQuiz.questions.find(question => question.id === questionId)[proposition]}"}`
                    });

                    if (!response.ok) {
                        throw new Error('Failed to update question answer');
                    }

                    this.selectedQuiz.questions.find(question => question.id === questionId).answer = this.selectedQuiz.questions.find(question => question.id === questionId)[proposition];
                } catch (error) {
                    console.error('Erreur lors de la définition de la réponse de la question:', error);
                }
            }
        },
        components: {
            NewQuestionForm
        },
        mounted() {
            this.getQuizName();
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
    fetch(`http://127.0.0.1:5000/quiz/api/v1.0/quiz/${this.selectedQuiz.id}/questions/${question.id}`, {
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
    button {
        margin: 25px;
    }
</style>