Feature: Gestion complète d'un employé dans OrangeHRM

  Scenario: Création, modification et suppression d'un employé

    Given je suis connecté en tant qu'admin
    When je crée un nouvel employé
    Then l'employé doit apparaître dans la liste des employés

    When je modifie les informations de l'employé
    Then les informations mises à jour doivent être visibles

    When je supprime l'employé
    Then l'employé ne doit plus apparaître dans la liste