# language: fr
Fonctionnalité: Gestion des congés

  En tant qu'employé
  Je veux pouvoir poser des congés et suivre leur statut
  Afin que mon manager puisse approuver ou rejeter mes demandes

  Scénario: Cycle de demande et approbation de congé

    Étant donné que je suis connecté en tant qu'employé
    Quand je crée une demande de congé pour une période donnée
    Alors la demande apparaît comme "En attente" dans la liste des congés

    Étant donné que je suis connecté en tant que manager
    Quand je valide la demande de congé de l'employé
    Alors le statut de la demande doit être "Approuvé"