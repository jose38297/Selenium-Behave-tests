Feature: Gestion des feuilles de temps dans OrangeHRM

  Background: Connexion en tant qu'admin
    Given je suis connecté en tant qu'admin

  Scenario: Consulter la feuille de temps d'un employé
    Given je navigue vers la page Timesheets
    When je sélectionne un employé dans la liste
    And je sélectionne la période de la semaine courante
    Then la feuille de temps de l'employé doit être affichée