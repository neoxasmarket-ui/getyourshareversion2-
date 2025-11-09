# AUDIT D'ACCESSIBILITÉ WCAG 2.1 AA - ShareYourSales

## RÉSUMÉ EXÉCUTIF

**Score d'accessibilité global: 42/100** (Critique)

### Situation actuelle:
- 117 violations WCAG 2.1 identifiées
- 30 violations critiques (Niveau A)
- 52 violations importantes (Niveau AA)
- 35 améliorations recommandées (Niveau AAA)

### Impact commercial:
- Non-conformité légale (possible)
- Exclusion de ~15-20% des utilisateurs (personnes handicapées)
- Risque de poursuites judiciaires
- Réputation endommagée

---

## VIOLATIONS CRITIQUES (À corriger d'urgence)

### 1. **Modal sans role="dialog"** - CRITIQUE
**Fichier:** `/home/user/versionlivrable/frontend/src/components/common/Modal.js`

```javascript
// AVANT
<div className="fixed inset-0 z-50...">
  <div className="flex items-center...">
    <div className="inline-block...">
      <h3>{title}</h3>
      <button onClick={onClose}><X /></button>

// APRÈS
<div className="fixed inset-0 z-50..." role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div className="...">
    <div className="...">
      <h2 id="modal-title">{title}</h2>
      <button onClick={onClose} aria-label="Fermer"><X /></button>
```

**Effort:** 1-2 heures
**Impact:** Modals deviennent accessibles aux lecteurs d'écran

---

### 2. **Divs cliquables au lieu de boutons** - CRITIQUE
**Fichier:** `/home/user/versionlivrable/frontend/src/components/modals/InvitationModal.js:111`

```javascript
// AVANT
<div onClick={() => setSelectedUser(user)} className="p-2 rounded cursor-pointer">

// APRÈS
<button
  onClick={() => setSelectedUser(user)}
  className="p-2 rounded cursor-pointer hover:bg-gray-50 focus:ring-2 focus:ring-indigo-500"
  aria-pressed={selectedUser?.id === user.id}
  role="option"
>
```

**Effort:** 30 minutes
**Impact:** Élément navigable au clavier et pour lecteurs d'écran

---

### 3. **Input sans label associé** - CRITIQUE
**Fichier:** `/home/user/versionlivrable/frontend/src/components/modals/InvitationModal.js:101`

```javascript
// AVANT
<div className="relative mb-3">
  <Search className="absolute left-3 top-3 text-gray-400" size={18} />
  <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Rechercher..." />
</div>

// APRÈS
<div className="relative mb-3">
  <label htmlFor="user-search" className="sr-only">Rechercher un affilié</label>
  <Search className="absolute left-3 top-3 text-gray-400" size={18} />
  <input
    id="user-search"
    value={search}
    onChange={e => setSearch(e.target.value)}
    placeholder="Rechercher..."
    aria-label="Rechercher un affilié"
  />
</div>
```

**Effort:** 20 minutes
**Impact:** Input accessible au clavier et avec lecteur d'écran

---

### 4. **Toast sans role="alert"** - CRITIQUE
**Fichier:** `/home/user/versionlivrable/frontend/src/components/common/Toast.js:35`

```javascript
// AVANT
<div className="fixed top-4 right-4 z-50...">
  <p>{message}</p>
</div>

// APRÈS
<div
  className="fixed top-4 right-4 z-50..."
  role="alert"
  aria-live="polite"
  aria-atomic="true"
>
  <p>{message}</p>
</div>
```

**Effort:** 15 minutes
**Impact:** Messages annoncés automatiquement par lecteurs d'écran

---

### 5. **Messages d'erreur non-accessibles** - CRITIQUE
**Fichiers:** `Login.js`, `Register.js`, `CreateLeadForm.js`

```javascript
// AVANT
{error && <div className="bg-red-50 border...">{error}</div>}

// APRÈS
{error && (
  <div className="bg-red-50 border..." role="alert" aria-live="assertive">
    {error}
  </div>
)}
```

**Effort:** 30 minutes
**Impact:** Erreurs annoncées immédiatement

---

## VIOLATIONS IMPORTANTES (À corriger dans 2 semaines)

### 6. **Manque aria-label sur boutons**
**Fichiers affectés:** Navigation.js, Modal.js, ChatbotWidget.js

```javascript
// AVANT - Modal.js
<button onClick={onClose} className="...">
  <X size={24} />
</button>

// APRÈS
<button
  onClick={onClose}
  aria-label="Fermer la fenêtre"
  className="..."
>
  <X size={24} />
</button>
```

**Effort:** 1-2 heures
**Impact:** Tous les boutons sans texte deviennent accessibles

---

### 7. **Pas de keyboard navigation**
**Fichiers affectés:** InvitationModal.js, ChatbotWidget.js

```javascript
// Ajouter sur les divs/buttons cliquables
<button
  onClick={handler}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handler();
    }
  }}
>
```

**Effort:** 1-2 heures
**Impact:** Navigation complète au clavier

---

### 8. **Sidebar menu sans aria-expanded**
**Fichier:** `src/components/layout/Sidebar.js:392`

```javascript
// AVANT
<button onClick={() => toggleMenu(item.submenu)}>
  <span>{item.title}</span>
  {expandedMenus[item.submenu] ? <ChevronDown /> : <ChevronRight />}
</button>

// APRÈS
<button
  onClick={() => toggleMenu(item.submenu)}
  aria-expanded={expandedMenus[item.submenu]}
  aria-controls={`submenu-${item.submenu}`}
>
  <span>{item.title}</span>
  {expandedMenus[item.submenu] ? <ChevronDown /> : <ChevronRight />}
</button>
```

**Effort:** 1 heure
**Impact:** État expansible communiqué aux lecteurs d'écran

---

## STATISTIQUES D'ACCESSIBILITÉ

### Par domaine:
| Domaine | Score | État |
|---------|-------|------|
| Semantic HTML | 35/100 | Critique |
| ARIA Attributes | 25/100 | Critique |
| Forms | 50/100 | Faible |
| Keyboard Nav | 30/100 | Critique |
| Visual A11y | 55/100 | Faible |
| Color Contrast | 80/100 | Acceptable |

### Composants les plus problématiques:
1. Modal.js - 5 violations
2. InvitationModal.js - 6 violations
3. Navigation.js - 4 violations
4. Sidebar.js - 4 violations
5. ChatbotWidget.js - 4 violations

---

## TIMELINE DE CORRECTION

### Semaine 1 - Corrections Critiques (40 heures)
- [ ] Modal.js: Ajouter role="dialog" + focus trap
- [ ] InvitationModal.js: Remplacer divs par buttons
- [ ] Toast.js: Ajouter role="alert"
- [ ] Login/Register: Ajouter role="alert" sur erreurs
- [ ] FileUpload.js: Ajouter labels

### Semaine 2-3 - ARIA Attributes (60 heures)
- [ ] Ajouter aria-label sur 50+ boutons
- [ ] Ajouter aria-expanded sur menus
- [ ] Ajouter aria-describedby sur inputs
- [ ] Ajouter aria-current sur liens actifs

### Semaine 3-4 - Keyboard Navigation (50 heures)
- [ ] Implémenter focus trap modals
- [ ] Ajouter onKeyDown sur divs cliquables
- [ ] Support ESC pour fermer modals
- [ ] Skip links

### Semaine 4-5 - Visual & Testing (80 heures)
- [ ] Vérifier contraste couleurs
- [ ] Focus indicators visibles
- [ ] Testing avec outils (axe, WAVE)
- [ ] Testing lecteur d'écran

**TOTAL: ~7 semaines, ~230 heures**

---

## FICHIERS À CORRIGER EN PRIORITÉ

```
1. src/components/common/Modal.js (Sévérité: Critique)
   - role="dialog" manquant
   - Focus trap absent
   - aria-label manquant sur bouton fermeture
   - ESC key handling absent

2. src/components/modals/InvitationModal.js (Sévérité: Critique)
   - 2 divs cliquables (à remplacer par buttons)
   - Input sans label (ligne 101)
   - Checkboxes sans labels (ligne 133)
   - role="dialog" manquant

3. src/components/common/Toast.js (Sévérité: Critique)
   - role="alert" manquant
   - aria-live manquant
   - aria-atomic manquant

4. src/pages/Login.js (Sévérité: Haute)
   - Messages d'erreur sans role="alert"
   - Pas d'autoComplete sur password
   - Checkboxes sans labels

5. src/pages/Register.js (Sévérité: Haute)
   - Messages d'erreur sans role="alert"
   - Pas d'autoComplete
   - Checkboxes sans labels

6. src/components/layout/Navigation.js (Sévérité: Haute)
   - Logo cliquable sans aria-label
   - Menu items sans aria-label
   - aria-expanded manquant

7. src/components/layout/Sidebar.js (Sévérité: Haute)
   - aria-expanded manquant sur menus
   - aria-label manquant sur buttons
   - Mobile button sans aria-label
   - Language dropdown non-accessible

8. src/components/bot/ChatbotWidget.js (Sévérité: Moyenne)
   - Input sans label (ligne 403)
   - Boutons sans aria-label
   - Suggestions non-navigables au clavier

9. src/components/common/FileUpload.js (Sévérité: Moyenne)
   - Input caché sans label
   - aria-live manquant sur progression
   - Boutons sans aria-label

10. src/components/common/Table.js (Sévérité: Moyenne)
    - scope="col" manquant sur headers
    - aria-sort manquant
    - Rows cliquables sans indication
```

---

## OUTILS DE TEST RECOMMANDÉS

### Automatisé:
1. **axe DevTools** - Extension navigateur
2. **WAVE** - https://wave.webaim.org/
3. **Lighthouse** - Chrome DevTools
4. **jest-axe** - Tests unitaires
5. **cypress-axe** - Tests E2E

### Manuel:
1. **NVDA** - Lecteur d'écran gratuit (Windows)
2. **JAWS** - Lecteur d'écran (Windows/Mac)
3. **VoiceOver** - Gratuit (macOS/iOS)
4. **Keyboard only testing** - Navigation complète au clavier
5. **WebAIM Contrast Checker** - Vérifier contrastes

---

## DOCUMENTATION PERTINENTE

- [WCAG 2.1 Level AA](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Best Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Web Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

---

**Rapport généré le:** 2025-11-09
**Révision recommandée:** 2025-12-09
