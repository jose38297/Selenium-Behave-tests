Feature: Authentification
  En tant qu utilisateur du systeme
  Je veux pouvoir me connecter et me deconnecter
  Afin d acceder ou quitter l application en securite

  # ==========================================================================
  # SCENARIO 1 : Connexion avec identifiants valides
  # Verifie que l utilisateur arrive bien sur le Dashboard apres connexion
  # ==========================================================================
  Scenario: Connexion avec identifiants valides
    Given je suis sur la page de connexion
    When je saisis le nom d utilisateur "Admin"
    And je saisis le mot de passe "admin123"
    And je clique sur le bouton de connexion
    Then je dois etre redirige vers le tableau de bord
    And je dois voir le menu de navigation

  # ==========================================================================
  # SCENARIO 2 : Connexion avec mot de passe incorrect
  # Verifie que l application affiche un message d erreur
  # ==========================================================================
  Scenario: Connexion avec mot de passe incorrect
    Given je suis sur la page de connexion
    When je saisis le nom d utilisateur "Admin"
    And je saisis le mot de passe "mauvaisMotDePasse"
    And je clique sur le bouton de connexion
    Then je dois voir un message d erreur de connexion
    And je dois rester sur la page de connexion

  # ==========================================================================
  # SCENARIO 3 : Connexion avec champs vides
  # Verifie la validation du formulaire
  # ==========================================================================
  Scenario: Connexion avec champs vides
    Given je suis sur la page de connexion
    When je clique sur le bouton de connexion
    Then je dois voir des messages de validation obligatoires

  # ==========================================================================
  # SCENARIO 4 : Deconnexion
  # Verifie que l utilisateur peut se deconnecter et est redirige
  # ==========================================================================
  Scenario: Deconnexion apres connexion reussie
    Given je suis connecte en tant qu Admin
    When je clique sur le menu utilisateur
    And je clique sur Logout
    Then je dois etre redirige vers la page de connexion
