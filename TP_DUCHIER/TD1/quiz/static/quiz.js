function get_all_quiz_old(){
    fetch('/quiz/api/v1.0/quiz')
    .then((rep) => { 
        rep.json()
        .then((json) => console.log(json));
    });
}

async function get_all_quiz(){
    const rep = await fetch('/quiz/api/v1.0/quiz');
    const json = await rep.json();
    console.log(json);
    show_all_quiz(json);
}

//modification ici pour ajouter un bouton de suppression à côté de chaque quiz
function show_all_quiz(quizs) {
    $("#all-quiz ul").empty();
    for (const q of quizs) {
        
        const quizLink = $("<a>")
        .text(q.name) 
        .attr("href", q.url); 
        const quizItem = $("<li>").append(quizLink);
           
        $("#all-quiz ul").append(quizItem);
        
        
        $("#all-quiz ul").append(
            $("<li>").append(
                $("<button>").text("Delete").addClass("delete-quiz-btn").data("quiz-id", q["id"])
            )
        )
    }
    show("all-quiz");
} 

async function get_quiz(quiz_id){
    const rep = await fetch(`/quiz/api/v1.0/quiz/${quiz_id}`);
    const json = await rep.json();
    console.log(json);
    show_quiz(json);
}

function show_quiz(json){
    $("#quiz h2").empty();
    $("#quiz ul").empty();
    $("#quiz h2").text(json["name"]);
    for(const q of json["questions"]){
        $("#quiz ul").append(
            $("<li>")
            .text(q["title"])
        )
    }
}

async function create_quiz(json){
    const rep = await fetch('/quiz/api/v1.0/quiz',
        {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify(json)
        }
    );
    json = await rep.json();
    console.log(json);
    show_quiz(json);
}


async function create_question(json){
    const rep = await fetch('/quiz/api/v1.0/question',
        {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify(json)
        }
    );
    json = await rep.json();
    console.log(json);
}

async function get_all_question(){
    const rep = await fetch("/quiz/api/v1.0/question");
    const json = await rep.json();
    console.log(json);
}

//modification ici pour ajouter les gestionnaires d'événements pour les boutons de suppression dans la fonction
async function setup() {
    $("#create-quiz-create").on("click", async () => { await click_create_quiz(); });
    $("#create-quiz-abord").on("click", async () => { await get_all_quiz(); });
    $("#create-question button").on("click", async () => { await click_create_question(); });
    $("#all-quiz-add-quiz").on("click", () => click_add_quiz());
    
    // Ajoute les gestionnaires d'événements pour les boutons de suppression
    $("body").on("click", ".delete-quiz-btn", async function() {
        const quiz_id = $(this).data("quiz-id");
        await delete_quiz(quiz_id);
    });

    $("body").on("click", ".delete-question-btn", async function() {
        const question_id = $(this).data("question-id");
        await delete_question(question_id);
    });

    await get_all_quiz();
}


function click_add_quiz(){
    show("create-quiz")
}

async function click_create_quiz(){
    const name = $("#create-quiz-name").val();
    await create_quiz({"name": name});
}

async function click_create_question(){
    const title = $("#create-question-title").val();
    const quiz_id = $("#create-question-id").val();
    await create_question(
        {
            "title": title,
            "quiz_id": quiz_id
        }
    )
}

function hide_all(){
    $("#all-quiz").css("display", "none");
    //$("#create-question").css("display","none");
    $("#create-quiz").css("display", "none");
    $("#quiz").css("display", "none");
}


function show(id){
    hide_all();
    $("#"+id).css("display", "block");
}

$(async() => { await setup(); });



//AJOUT DE LA SUPPRESSION DE QUIZ

async function delete_quiz(quiz_id) {
    const rep = await fetch(`/quiz/api/v1.0/quiz/${quiz_id}`, {
        method: "DELETE"
    });
    if (rep.ok) {
        console.log("Quiz deleted successfully");
        await get_all_quiz(); // Actualise la liste des quiz après suppression
    } else {
        console.error("Failed to delete quiz");
    }
}


//AJOUT DE LA SUPPRESSION DE QUESTION

async function delete_question(question_id) {
    const rep = await fetch(`/quiz/api/v1.0/question/${question_id}`, {
        method: "DELETE"
    });
    if (rep.ok) {
        console.log("Question deleted successfully");
        // Ajoutez ici le code pour rafraîchir la liste des questions après la suppression si nécessaire
    } else {
        console.error("Failed to delete question");
    }
}
