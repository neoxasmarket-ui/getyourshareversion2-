# GUIDE DE TESTS MANUELS - FORMULAIRES

**Objectif:** Valider le comportement des formulaires en environment réel
**Date:** November 2025
**Format:** Checklist step-by-step

---

## PRÉAMBULE

### Avant de Commencer
1. Ouvrir une session incognito (Ctrl+Shift+P ou Cmd+Shift+P)
2. Vider le cache et les cookies (DevTools > Storage)
3. Ouvrir la console DevTools (F12)
4. Activer "Preserve logs" dans la console

### Prérequis
- Backend en cours d'exécution
- Frontend en cours d'exécution
- Compte test disponible
- Données test préparées

---

## TEST 1: LOGIN FORM (P1 - CRÍTICO)

### 1.1 Test Heureux - Valid Credentials

```
Objectif: Vérifier que le login fonctionne avec des identifiants valides
Utilisateur: admin@shareyoursales.ma / Admin123

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Vérifier que le formulaire s'affiche correctement
      - Email input visible et vide
      - Password input visible et vide
      - Button "Se connecter" visible
      - Test accounts visible

[ ] 3. Remplir le formulaire
      - Type email: admin@shareyoursales.ma
      - Type password: Admin123

[ ] 4. Soumettre le formulaire
      - Click button "Se connecter"
      - Vérifier que le button est disabled
      - Vérifier que le text change en "Connexion..."

[ ] 5. Attendre la réponse (max 3 secondes)
      - Vérifier que le token est stocké dans localStorage
      - Vérifier que l'utilisateur est stocké dans localStorage
      - Vérifier la redirection vers /dashboard

[ ] 6. Vérifier l'état final
      - Page dashboard chargée
      - Utilisateur nommé visible
      - Menu sidebar visible avec les options correctes

RÉSULTAT ATTENDU:
- Login réussi
- Redirection vers dashboard
- Token et utilisateur en localStorage
```

### 1.2 Test Erreur - Invalid Email

```
Objectif: Vérifier la validation de l'email
Email: invalid-email / Password: Admin123

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Remplir le formulaire
      - Type email: invalid-email
      - Type password: Admin123

[ ] 3. Cliquer le bouton
      - Click "Se connecter"

[ ] 4. Vérifier le comportement
      - L'email doit être un email valide (HTML5 validation)
      - Le formulaire ne doit pas être soumis
      - Le navigateur affiche un message "Please include @"

RÉSULTAT ATTENDU:
- HTML5 validation
- Message du navigateur
- Pas de requête API
```

### 1.3 Test Erreur - Wrong Password

```
Objectif: Vérifier le message d'erreur avec mauvais mot de passe
Email: admin@shareyoursales.ma / Password: WrongPassword

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Remplir le formulaire
      - Type email: admin@shareyoursales.ma
      - Type password: WrongPassword

[ ] 3. Soumettre
      - Click "Se connecter"

[ ] 4. Vérifier le message d'erreur
      - Attendre 2-3 secondes pour la réponse
      - Un message d'erreur rouge doit apparaître
      - Message: "Email ou mot de passe incorrect"
      - L'icon AlertCircle doit être visible

[ ] 5. Vérifier l'état
      - Button "Se connecter" réactif (pas disabled)
      - Les inputs gardent les valeurs
      - Pas de token en localStorage

RÉSULTAT ATTENDU:
- Message d'erreur visible et clair
- Form reste remplie pour rétry
- Pas de navigation
```

### 1.4 Test Erreur - Empty Email

```
Objectif: Vérifier la validation "required" sur email
Email: (vide) / Password: Admin123

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Remplir seulement le password
      - Leave email empty
      - Type password: Admin123

[ ] 3. Cliquer le bouton
      - Click "Se connecter"

[ ] 4. Vérifier le comportement
      - HTML5 validation déclenche
      - Message du navigateur: "Please fill in this field"
      - Pas de requête API

RÉSULTAT ATTENDU:
- HTML5 validation fonctionne
- Focus sur le champ email
```

### 1.5 Test Loading State

```
Objectif: Vérifier que le button est disabled pendant le loading
Email: admin@shareyoursales.ma / Password: Admin123

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Ouvrir DevTools Network tab
[ ] 3. Remplir et soumettre
      - Type email et password
      - Click "Se connecter"
      - Immédiatement vérifier le button

[ ] 4. Vérifier pendant la requête (throttle à Fast 3G pour voir)
      - Button est disabled
      - Text change en "Connexion..."
      - Impossible de cliquer plusieurs fois
      - Spinner ou loading indicator (si implémenté)

[ ] 5. Attendre la réponse
      - Button redevient actif (ou redirige)

RÉSULTAT ATTENDU:
- Button disabled pendant le loading
- Pas de double submission possible
- UX feedback clair
```

### 1.6 Test 2FA Flow

```
Objectif: Vérifier le flux 2FA complet
Email: Compte avec 2FA activé / 2FA Code: 123456

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Remplir avec compte 2FA
      - Type email et password du compte 2FA

[ ] 3. Cliquer "Se connecter"
      - Le formulaire doit changer pour afficher 2FA
      - Shield icon visible
      - Code input vide avec placeholder "000000"

[ ] 4. Entrer le code 2FA
      - Type: 123456
      - Code doit être masqué (ou visible selon design)

[ ] 5. Cliquer "Vérifier le code"
      - Button doit être disabled pendant le loading
      - Attendre la réponse

[ ] 6. Vérifier le résultat
      - Redirection vers /dashboard
      - Token stocké
      - Utilisateur connecté

RÉSULTAT ATTENDU:
- 2FA form apparaît après credentials
- Code input accepte 6 chiffres
- Vérification fonctionne
- Redirection après succès
```

### 1.7 Test Quick Login Buttons

```
Objectif: Vérifier que les boutons de quick login fonctionnent
Accounts: Admin, Influencers, Merchants

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Scroller vers les quick login buttons
[ ] 3. Cliquer sur "Admin" button
      - Button doit avoir "Admin" label
      - Button doit avoir "Enterprise - Accès Total"

[ ] 4. Vérifier le résultat
      - Loading state visible
      - Redirection vers /dashboard (ou 2FA si activé)

[ ] 5. Logout et revenir
[ ] 6. Tester avec "Hassan Oudrhiri" (Influencer STARTER)
      - Click button
      - Vérifier les données du profil (67K followers)

[ ] 7. Tester avec "Luxury Crafts" (Merchant PRO)
      - Click button
      - Vérifier les données du profil

RÉSULTAT ATTENDU:
- Quick login buttons raccourcissent le processus
- Credentials correctes envoyées
- Navigation vers dashboard
```

### 1.8 Test Forget Password (si implémenté)

```
Objectif: Vérifier le lien "Mot de passe oublié"
Email: test@example.com

STEPS:
[ ] 1. Navigate à http://localhost:3000/login
[ ] 2. Cliquer sur "Mot de passe oublié" (si visible)
      - Link doit naviguer vers /forgot-password ou afficher un modal

[ ] 3. Remplir l'email
      - Type: test@example.com

[ ] 4. Soumettre
      - Vérifier le message (email de reset envoyé)

RÉSULTAT ATTENDU:
- Link visible (ou dans error message)
- Reset email flow fonctionne
```

---

## TEST 2: REGISTER FORM (P1 - CRÍTICO)

### 2.1 Test Heureux - Complete Registration

```
Objectif: Tester l'inscription complète pour un merchant
Role: Merchant
Plan: Pro

STEPS:
[ ] 1. Navigate à http://localhost:3000/register
[ ] 2. Vérifier la page
      - Logo et branding visible
      - "Créer un compte" header
      - "Vous êtes ?" question
      - Deux options: "Entreprise" et "Influenceur"

[ ] 3. Cliquer "Entreprise"
      - Page change pour afficher le formulaire
      - "Inscription Entreprise" visible

[ ] 4. Remplir le formulaire
      [ ] Prénom: Jean
      [ ] Nom: Dupont
      [ ] Nom de l'entreprise: TestCorp
      [ ] Email: jean.dupont.newtest@example.com
      [ ] Téléphone: +33612345678
      [ ] Mot de passe: TestPassword123
      [ ] Confirmer mot de passe: TestPassword123
      [ ] Accepter les CGU (checkbox)

[ ] 5. Cliquer "Créer mon compte"
      - Button disabled avec "Inscription en cours..."
      - Attendre la réponse (max 3 secondes)

[ ] 6. Vérifier la page de succès
      - CheckCircle icon vert
      - "Inscription réussie ! 🎉"
      - Spinner de redirection
      - Auto-redirect vers /login après 3 secondes

[ ] 7. Vérifier que le compte peut être utilisé
      - Remplir le formulaire login avec:
        Email: jean.dupont.newtest@example.com
        Password: TestPassword123
      - Cliquer "Se connecter"
      - Vérifier la redirection vers dashboard

RÉSULTAT ATTENDU:
- Registration complète
- Success page affichée
- Redirection vers login
- Login fonctionne avec les nouvelles credentials
```

### 2.2 Test Validation - Password Mismatch

```
Objectif: Vérifier que les mots de passe doivent matcher
Passwords: password123 / different123

STEPS:
[ ] 1. Navigate à http://localhost:3000/register
[ ] 2. Cliquer "Entreprise"
[ ] 3. Remplir le formulaire
      [ ] Prénom: Jean
      [ ] Nom: Dupont
      [ ] Nom de l'entreprise: TestCorp
      [ ] Email: test@newemail.com
      [ ] Téléphone: +33612345678
      [ ] Mot de passe: password123
      [ ] Confirmer mot de passe: different123
      [ ] Accepter CGU

[ ] 4. Cliquer "Créer mon compte"
      - Vérifier le message d'erreur
      - "Les mots de passe ne correspondent pas"
      - Error box rouge visible

[ ] 5. Corriger les mots de passe
      [ ] Mot de passe: password123
      [ ] Confirmer: password123
      [ ] Cliquer "Créer mon compte"
      - Doit fonctionner maintenant

RÉSULTAT ATTENDU:
- Validation de matching immédiate
- Message d'erreur clair
- Correction possible
```

### 2.3 Test Validation - Password Too Short

```
Objectif: Vérifier que le password min 6 chars
Password: short

STEPS:
[ ] 1. Navigate à /register et sélectionner "Entreprise"
[ ] 2. Remplir le formulaire
      [ ] Tous les champs sauf password
      [ ] Mot de passe: short
      [ ] Confirmer: short
      [ ] Accepter CGU

[ ] 3. Cliquer "Créer mon compte"
      - Vérifier le message d'erreur
      - "Le mot de passe doit contenir au moins 6 caractères"

[ ] 4. Corriger le password
      [ ] Mot de passe: password123
      [ ] Confirmer: password123
      [ ] Submit

RÉSULTAT ATTENDU:
- Password validation min 6 chars
- Message d'erreur spécifique
```

### 2.4 Test Validation - Duplicate Email

```
Objectif: Vérifier que les emails doivent être uniques
Email: admin@shareyoursales.ma (already exists)

STEPS:
[ ] 1. Navigate à /register et sélectionner "Entreprise"
[ ] 2. Remplir le formulaire
      [ ] Tous les champs
      [ ] Email: admin@shareyoursales.ma
      [ ] Password: TestPassword123
      [ ] Confirm Password: TestPassword123
      [ ] Accepter CGU

[ ] 3. Cliquer "Créer mon compte"
      - Attendre la réponse du serveur (2-3 secondes)
      - Vérifier le message d'erreur
      - Doit être quelque chose comme "Email already exists"

[ ] 4. Entrer un nouvel email
      [ ] Email: newemail@example.com
      [ ] Cliquer "Créer mon compte"
      - Doit fonctionner maintenant

RÉSULTAT ATTENDU:
- Validation serveur du duplicate email
- Message d'erreur clair
- Pas de création de compte doublonné
```

### 2.5 Test Influencer Registration

```
Objectif: Tester l'inscription pour un influencer
Role: Influencer

STEPS:
[ ] 1. Navigate à /register
[ ] 2. Cliquer "Influenceur / Commercial"
      - Page change vers "Inscription Influenceur"
      - "Nom d'utilisateur" field visible au lieu de "Nom de l'entreprise"

[ ] 3. Remplir le formulaire
      [ ] Prénom: Sarah
      [ ] Nom: Benali
      [ ] Nom d'utilisateur: sarahbenali
      [ ] Email: sarah.benali.test@example.com
      [ ] Téléphone: +33623456789
      [ ] Mot de passe: TestPassword123
      [ ] Confirmer: TestPassword123
      [ ] Accepter CGU

[ ] 4. Cliquer "Créer mon compte"
      - Attendre la réponse
      - Page de succès

[ ] 5. Vérifier login avec le nouveau compte
      - Email: sarah.benali.test@example.com
      - Password: TestPassword123
      - Vérifier que le profil influencer charge

RÉSULTAT ATTENDU:
- Influencer registration fonctionne
- Formulaire différent (username au lieu de company)
- Login avec le nouveau compte
```

### 2.6 Test URL Parameters

```
Objectif: Tester les paramètres URL pour pre-selection
URL: /register?role=merchant&plan=pro

STEPS:
[ ] 1. Navigate à http://localhost:3000/register?role=merchant&plan=pro
      - Vérifier que le formulaire d'inscription merchant apparaît
      - Ne doit pas montrer l'écran de sélection de rôle

[ ] 2. Remplir et soumettre
      - Le plan "pro" doit être pré-sélectionné (si visible)

RÉSULTAT ATTENDU:
- URL params skippent l'écran de sélection
- Formulaire merchant s'affiche directement
- Plan pro est pré-sélectionné
```

---

## TEST 3: CONTACT FORM (P2 - IMPORTANT)

### 3.1 Test Complete Contact Submission

```
Objectif: Tester le formulaire de contact complet
Email: test@example.com (logué ou pas)

STEPS:
[ ] 1. Navigate à http://localhost:3000/contact
[ ] 2. Vérifier la page
      - Titre "Nous contacter"
      - Formulaire visible
      - Catégories disponibles

[ ] 3. Remplir le formulaire
      [ ] Nom: Jean Dupont
      [ ] Email: test@example.com
      [ ] Téléphone: +33612345678
      [ ] Sujet: Test Bug Report
      [ ] Catégorie: "Signaler un Bug"
      [ ] Message: "Test message for form validation"

[ ] 4. Soumettre
      [ ] Cliquer "Envoyer"
      [ ] Attendre le loading
      [ ] Vérifier le message de succès
      [ ] Toast notification doit apparaître

[ ] 5. Vérifier que le formulaire reset
      [ ] Tous les inputs vides
      [ ] Catégorie revient à "Générale" (si applicable)

RÉSULTAT ATTENDU:
- Contact soumis avec succès
- Toast notification visible
- Formulaire reset
```

### 3.2 Test Auto-Fill pour Logged-In User

```
Objectif: Vérifier que le formulaire pré-remplit les données utilisateur connecté

STEPS:
[ ] 1. Login avec un compte (ex: admin)
[ ] 2. Navigate à http://localhost:3000/contact
[ ] 3. Vérifier le pré-remplissage
      [ ] Nom: Admin User (ou le vrai nom)
      [ ] Email: admin@shareyoursales.ma
      [ ] Téléphone: (si disponible)
      - Les champs doivent être pré-remplis

[ ] 4. Éditer les champs
      [ ] Changer le sujet: Custom subject
      [ ] Changer le message: Custom message
      [ ] Sélectionner catégorie: "Support Technique"

[ ] 5. Soumettre
      - Vérifier que la soumission utilise les bonnes données

RÉSULTAT ATTENDU:
- Auto-fill fonctionne pour utilisateur connecté
- Peut être modifié
- Soumission utilise les nouvelles valeurs
```

---

## TEST 4: FORM SECURITY & EDGE CASES

### 4.1 Test XSS Prevention

```
Objectif: Vérifier que le contenu malveillant est échappé
Payload: <script>alert('XSS')</script>

STEPS:
[ ] 1. Navigate à /contact
[ ] 2. Remplir un champ avec script malveillant
      [ ] Nom: <script>alert('XSS')</script>
      [ ] Soumettre

[ ] 3. Vérifier le comportement
      - Aucune alerte JS ne doit s'afficher
      - Le formulaire doit traiter la soumission
      - Le script doit être échappé

[ ] 4. Vérifier le résultat en backend
      - Les données stockées doivent être saines
      - Pas de code malveillant exécuté

RÉSULTAT ATTENDU:
- XSS prevention fonctionne
- Script ne s'exécute pas
- Texte littéral "[script]" stocké
```

### 4.2 Test SQL Injection Prevention

```
Objectif: Vérifier la prévention d'injection SQL
Payload: '; DROP TABLE users; --

STEPS:
[ ] 1. Navigate à /register
[ ] 2. Remplir email avec payload
      [ ] Email: test'); DROP TABLE users; --@example.com
      [ ] Ou dans un autre champ

[ ] 3. Soumettre
      - Vérifier que le formulaire valide l'email
      - Invalid email format doit être affiché

[ ] 4. Si en quelque sorte c'était validé
      - Vérifier en backend que les données sont traitées de manière sûre
      - La table users ne doit pas être supprimée

RÉSULTAT ATTENDU:
- Input validation prévient les injections
- Email validation rejette le format invalide
```

### 4.3 Test Rate Limiting (si implémenté)

```
Objectif: Vérifier la prévention du brute force
Scénario: Plusieurs tentatives de login échouées

STEPS:
[ ] 1. Navigate à /login
[ ] 2. Entrer mauvais credentials
      [ ] Email: admin@shareyoursales.ma
      [ ] Password: WrongPassword
      [ ] Cliquer "Se connecter" 10 fois rapidement

[ ] 3. Vérifier le comportement
      - Après 5 tentatives, le form doit afficher un message
      - "Trop de tentatives, réessayez dans 5 minutes"
      - Ou similaire

[ ] 4. Attendre un peu et retry
      - Le formulaire doit redevenir actif

RÉSULTAT ATTENDU:
- Rate limiting fonctionne
- Brute force prevention en place
- Message utilisateur clair
```

### 4.4 Test Field Length Limits

```
Objectif: Vérifier les limites de longueur des champs

STEPS:
[ ] 1. Navigate à /register
[ ] 2. Remplir un champ avec un texte très long
      [ ] Prénom: aaaaaaa...aaaaaaa (200+ chars)

[ ] 3. Vérifier le comportement
      - Le champ doit limiter la saisie (maxLength)
      - Ou afficher une erreur après soumission

[ ] 4. Remplir avec contenu normal
      [ ] Prénom: Jean (normal)
      [ ] Soumettre

RÉSULTAT ATTENDU:
- Field length validation fonctionne
- Limite respectée
```

### 4.5 Test Network Resilience

```
Objectif: Tester le comportement sans réseau

STEPS:
[ ] 1. Navigate à /login
[ ] 2. Ouvrir DevTools Network tab
[ ] 3. Cliquer sur "Offline" (simulator no network)
[ ] 4. Remplir le formulaire
      [ ] Email: admin@shareyoursales.ma
      [ ] Password: Admin123
      [ ] Cliquer "Se connecter"

[ ] 5. Vérifier le comportement
      - Attendre le timeout (devrait être ~5-10 seconds)
      - Un message d'erreur doit apparaître
      - "Erreur de connexion" ou "Vérifiez votre connexion"

[ ] 6. Reactiver le réseau
      [ ] Click "Online" dans DevTools
      [ ] Essayer la soumission à nouveau
      - Doit fonctionner maintenant

RÉSULTAT ATTENDU:
- Error handling pour offline
- Message utilisateur clair
- Retry possible
```

---

## TEST 5: PERFORMANCE & LOAD TESTING

### 5.1 Test Form Load Time

```
Objectif: Vérifier le temps de chargement du formulaire

STEPS:
[ ] 1. Ouvrir DevTools Performance tab
[ ] 2. Record una nouvelle visite
[ ] 3. Navigate à http://localhost:3000/login
      - Record le chargement complet

[ ] 4. Arrêter la recording
[ ] 5. Analyser les metrics
      [ ] First Paint: < 1 second
      [ ] Largest Contentful Paint: < 2 seconds
      [ ] Time to Interactive: < 3 seconds

RÉSULTAT ATTENDU:
- Form charge rapidement
- < 3 secondes pour interaction
```

### 5.2 Test Submission Speed

```
Objectif: Mesurer le temps de réponse de la soumission

STEPS:
[ ] 1. Ouvrir DevTools Network tab
[ ] 2. Navigate à /login
[ ] 3. Remplir et soumettre
      [ ] Mesurer le temps jusqu'à la réponse

[ ] 4. Vérifier les metrics
      [ ] Temps de réponse API: < 2 seconds
      [ ] Total page load après submit: < 3 secondes

RÉSULTAT ATTENDU:
- API responds quickly
- User feedback fast
```

---

## TEST 6: ACCESSIBILITY & USABILITY

### 6.1 Test Keyboard Navigation

```
Objectif: Vérifier que le formulaire peut être navigué au clavier

STEPS:
[ ] 1. Navigate à /login
[ ] 2. Utiliser TAB pour naviguer
      [ ] Tab 1: Focus sur email input
      [ ] Tab 2: Focus sur password input
      [ ] Tab 3: Focus sur submit button
      [ ] Tab 4: Focus sur register link (si navigable)

[ ] 3. Remplir le formulaire avec Tab et typing
      [ ] Tab: email input
      [ ] Type: admin@shareyoursales.ma
      [ ] Tab: password input
      [ ] Type: Admin123
      [ ] Tab: submit button
      [ ] Enter: soumettre

[ ] 4. Vérifier le tab order
      - Doit être logique et fonctionnel

RÉSULTAT ATTENDU:
- Navigation au clavier fonctionne
- Tab order sensé
- Enter soumet le formulaire
```

### 6.2 Test Screen Reader Compatibility

```
Objectif: Vérifier l'accessibilité pour les lecteurs d'écran

STEPS (avec NVDA ou JAWS):
[ ] 1. Activer le screen reader
[ ] 2. Navigate à /login
[ ] 3. Vérifier les annonces
      [ ] "Form Login"
      [ ] "Email input"
      [ ] "Password input"
      [ ] "Submit button"
      [ ] "Error messages" (si applicable)

[ ] 4. Vérifier les labels
      - Chaque input doit avoir un label accessible
      - Les messages d'erreur doivent être annoncés

RÉSULTAT ATTENDU:
- Screen reader announces form elements
- Labels associated correctly
- Errors announced
```

### 6.3 Test Color Contrast

```
Objectif: Vérifier que le texte est lisible

STEPS:
[ ] 1. Ouvrir DevTools Lighthouse tab
[ ] 2. Run Accessibility audit
      - Navigate à /login
      - Run audit

[ ] 3. Vérifier les résultats
      [ ] Color contrast ratio > 4.5:1 (normal text)
      [ ] Color contrast ratio > 3:1 (large text)
      [ ] No color-only information

RÉSULTAT ATTENDU:
- Contrast ratio accessible
- Text readable for color blind users
```

---

## CHECKLIST FINALE

### Avant de déployer en production

```
[ ] Login form tests pass
[ ] Register form tests pass
[ ] Contact form tests pass
[ ] All validation works
[ ] Error messages display correctly
[ ] Loading states visible
[ ] Success feedback clear
[ ] Navigation works
[ ] Security tests pass (XSS, SQL injection, etc.)
[ ] Performance acceptable
[ ] Accessibility audit passes
[ ] Mobile responsive
[ ] Cross-browser compatible
[ ] Offline handling works
[ ] Rate limiting works
[ ] 2FA flow works
[ ] All endpoints respond
[ ] Data persistence works
[ ] No console errors
[ ] No console warnings
```

### Sign-off

- **Tester:** _________________
- **Date:** _________________
- **Status:** [ ] PASS [ ] FAIL
- **Notes:** _________________

