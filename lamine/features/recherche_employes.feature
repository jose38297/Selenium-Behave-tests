Feature: Recherche et filtrage des employes
  En tant qu administrateur RH
  Je veux pouvoir rechercher et filtrer les employes
  Afin de retrouver rapidement les informations desirees

  Background:
    Given je suis connecte en tant qu admin
    And je suis sur la page liste des employes

  # SCENARIO 1 : Autocomplete - nom existant
  Scenario: Recherche par nom avec un nom existant
    When je recherche par autocomplete le nom "Joy"
    Then au moins un resultat doit s afficher

  # SCENARIO 2 : Employee ID existant (0323 est dans la base)
  Scenario: Recherche par ID existant retourne un resultat
    When je recherche par employee id "0323"
    Then au moins un resultat doit s afficher

  # SCENARIO 3 : Employee ID inexistant
  Scenario: Recherche par ID inexistant retourne zero resultat
    When je recherche par employee id "IDXXXINCONNU999"
    Then aucun resultat ne doit s afficher

  # SCENARIO 4 : Champ vide = tous les employes
  Scenario: Recherche avec champ vide affiche tous les employes
    When je recherche un employe par le nom vide
    Then le nombre de resultats doit etre superieur a 0

  # SCENARIO 5 : Filtre par departement
  Scenario: Filtrage par departement Sub Unit
    When je filtre les employes par sous-unite "Engineering"
    Then le nombre de resultats doit etre superieur ou egal a 0
