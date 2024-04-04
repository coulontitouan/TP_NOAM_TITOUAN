<template>
    <div>
        <h1>Créer une nouvelle Question</h1>
        <form @submit.prevent="createQuestion">
            <label for="questionTitle">Titre de la question:</label>
            <input type="text" id="questionTitle" v-model="questionTitle" required>
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
                    const response = await fetch('http://127.0.0.1:5000/quiz/api/v1.0/question', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ quiz_id: this.quizId, title: this.questionTitle })
                    });
                    if (!response.ok) {
                        throw new Error('Failed to create new question');
                    }
                    this.$emit('questionCreated');
                    this.questionTitle = '';
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