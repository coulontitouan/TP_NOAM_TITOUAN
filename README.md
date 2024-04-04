Dans ce dossier vous trouverez l'API REST implémentée et vu en cours avec les ajouts demandés 
qui sont chacun bien visible dans les différents fichiers. (views.py et models.py)


J'ai donc ajouté la possibilité de supprimer un quiz, supprimer une question.
J'ai également amélioré l'interface en y implémentant un peu de CSS.
Pour toutes les nouveautés, je me suis bien evidement basé sur les fonctionnalités existantes et vues en cours.


Attention ! La fonctionnalités de suppression des questions est utilisable avec cette commande CURL :

curl -i -H "Content-Type: application/json" -X DELETE -d '{"title":"xxxxxxx", "quiz_id":xxxx}' http://localhost:5000/quiz/api/v1.0/question/1 
("1" etant un exemple pour l'id de la question)

On peut voir les questions des quizs en cliquant sur le quiz sur la page d'accueil.

La fonctionnalités de supprimer un quiz fonctionne bel et bien depuis la page d'accueil
Le code des fonctionnalités est bien presents, je vous invite donc à le consulter.

- DUBOIS TOM