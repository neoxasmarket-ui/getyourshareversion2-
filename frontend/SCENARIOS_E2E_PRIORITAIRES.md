# SCÉNARIOS E2E PRIORITAIRES - Cypress / Playwright

**Outil:** Cypress ou Playwright
**Status:** À implémenter
**Priorité:** P1 - Critical

---

## SETUP RECOMMANDÉ

### Installation Cypress
```bash
npm install --save-dev cypress @testing-library/cypress
npx cypress open
```

### Installation Playwright
```bash
npm install --save-dev playwright @playwright/test
npx playwright install
```

### Configuration Jest/RTL
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

---

## SCÉNARIO 1: COMPLETE LOGIN FLOW (P1 - CRÍTICO)

### Cypress Version

```javascript
describe('Complete Login Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
    cy.clearLocalStorage();
  });

  it('should login successfully with valid credentials', () => {
    // Arrange
    cy.get('[data-testid="email-input"]').should('be.visible');
    cy.get('[data-testid="password-input"]').should('be.visible');
    cy.get('[data-testid="login-button"]').should('be.visible');

    // Act
    cy.get('[data-testid="email-input"]').type('admin@shareyoursales.ma');
    cy.get('[data-testid="password-input"]').type('Admin123');
    cy.get('[data-testid="login-button"]').click();

    // Assert
    cy.get('[data-testid="login-button"]').should('be.disabled');
    cy.get('[data-testid="login-button"]').should('contain', 'Connexion...');

    // Wait for redirect
    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="dashboard-header"]').should('be.visible');

    // Verify token storage
    cy.window().then((win) => {
      expect(win.localStorage.getItem('token')).to.exist;
      expect(win.localStorage.getItem('user')).to.exist;
    });
  });

  it('should show error message with invalid credentials', () => {
    // Arrange
    cy.get('[data-testid="email-input"]').type('admin@shareyoursales.ma');
    cy.get('[data-testid="password-input"]').type('WrongPassword123');

    // Act
    cy.get('[data-testid="login-button"]').click();

    // Assert
    cy.get('[data-testid="error-message"]').should('be.visible');
    cy.get('[data-testid="error-message"]').should('contain', 'Email ou mot de passe incorrect');
    cy.url().should('include', '/login');
  });

  it('should prevent empty field submission', () => {
    // Act - try to submit without filling
    cy.get('[data-testid="login-button"]').click();

    // Assert - HTML5 validation should prevent submission
    cy.get('[data-testid="email-input"]').then(($input) => {
      expect($input[0].validationMessage).to.not.be.empty;
    });
  });

  it('should handle 2FA flow correctly', () => {
    // Setup: account with 2FA enabled
    const twoFAEmail = 'user@shareyoursales.ma';
    const twoFAPassword = 'Password123';
    const twoFACode = '123456';

    // Fill and submit
    cy.get('[data-testid="email-input"]').type(twoFAEmail);
    cy.get('[data-testid="password-input"]').type(twoFAPassword);
    cy.get('[data-testid="login-button"]').click();

    // Should show 2FA form
    cy.get('[data-testid="2fa-form"]').should('be.visible');
    cy.get('[data-testid="2fa-code-input"]').should('be.visible');

    // Enter 2FA code
    cy.get('[data-testid="2fa-code-input"]').type(twoFACode);
    cy.get('[data-testid="verify-2fa-button"]').click();

    // Should redirect to dashboard
    cy.url().should('include', '/dashboard');
  });

  it('should use quick login buttons', () => {
    // Test Admin quick login
    cy.get('button').contains('Admin').click();
    cy.get('[data-testid="login-button"]').should('be.disabled');
    cy.url().should('include', '/dashboard');

    // Logout and test Influencer
    cy.clearLocalStorage();
    cy.visit('http://localhost:3000/login');
    cy.get('button').contains('Hassan Oudrhiri').click();
    cy.url().should('include', '/dashboard');
  });
});
```

### Playwright Version

```javascript
import { test, expect } from '@playwright/test';

test.describe('Complete Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/login');
    await page.context().clearCookies();
    await page.evaluate(() => localStorage.clear());
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    // Arrange
    await expect(page.getByTestId('email-input')).toBeVisible();
    await expect(page.getByTestId('password-input')).toBeVisible();
    await expect(page.getByTestId('login-button')).toBeVisible();

    // Act
    await page.getByTestId('email-input').fill('admin@shareyoursales.ma');
    await page.getByTestId('password-input').fill('Admin123');
    await page.getByTestId('login-button').click();

    // Assert
    await expect(page.getByTestId('login-button')).toBeDisabled();
    await page.waitForURL('/dashboard');
    await expect(page.getByTestId('dashboard-header')).toBeVisible();

    // Verify token storage
    const token = await page.evaluate(() => localStorage.getItem('token'));
    expect(token).toBeTruthy();
  });

  test('should show error message with invalid credentials', async ({ page }) => {
    // Arrange & Act
    await page.getByTestId('email-input').fill('admin@shareyoursales.ma');
    await page.getByTestId('password-input').fill('WrongPassword');
    await page.getByTestId('login-button').click();

    // Assert
    await expect(page.getByTestId('error-message')).toBeVisible();
    await expect(page.getByTestId('error-message')).toContainText('Email ou mot de passe incorrect');
  });

  test('should handle 2FA flow', async ({ page }) => {
    // Fill credentials
    await page.getByTestId('email-input').fill('user@shareyoursales.ma');
    await page.getByTestId('password-input').fill('Password123');
    await page.getByTestId('login-button').click();

    // Wait for 2FA form
    await expect(page.getByTestId('2fa-form')).toBeVisible();

    // Enter 2FA code
    await page.getByTestId('2fa-code-input').fill('123456');
    await page.getByTestId('verify-2fa-button').click();

    // Verify redirect
    await page.waitForURL('/dashboard');
  });
});
```

---

## SCÉNARIO 2: COMPLETE REGISTRATION FLOW (P1 - CRÍTICO)

### Cypress Version

```javascript
describe('Complete Registration Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/register');
  });

  it('should register merchant successfully', () => {
    const email = `merchant${Date.now()}@test.com`;
    const password = 'TestPassword123';

    // Step 1: Role selection
    cy.get('button').contains('Entreprise').click();

    // Wait for Step 2
    cy.get('h2').should('contain', 'Inscription Entreprise');

    // Step 2: Fill form
    cy.get('input[placeholder="Jean"]').type('Jean');
    cy.get('input[placeholder="Dupont"]').type('Dupont');
    cy.get('input[placeholder="Mon Entreprise"]').type('TestCorp');
    cy.get('input[placeholder="email@exemple"]').type(email);
    cy.get('input[placeholder*="+33"]').type('+33612345678');

    // Get all password inputs
    cy.get('input[type="password"]').then(($inputs) => {
      cy.wrap($inputs[0]).type(password);
      cy.wrap($inputs[1]).type(password);
    });

    // Accept terms
    cy.get('input[type="checkbox"]').check();

    // Submit
    cy.get('button').contains('Créer mon compte').click();

    // Verify success page
    cy.get('h2').should('contain', 'Inscription réussie');
    cy.get('p').should('contain', 'Vous allez être redirigé');

    // Verify redirect and can login
    cy.url().should('include', '/login');
    cy.get('input[data-testid="email-input"]').type(email);
    cy.get('input[data-testid="password-input"]').type(password);
    cy.get('button[data-testid="login-button"]').click();
    cy.url().should('include', '/dashboard');
  });

  it('should validate password matching', () => {
    cy.get('button').contains('Entreprise').click();

    cy.get('input[placeholder="Jean"]').type('Jean');
    cy.get('input[placeholder="Dupont"]').type('Dupont');
    cy.get('input[placeholder="Mon Entreprise"]').type('TestCorp');
    cy.get('input[placeholder="email@exemple"]').type('test@example.com');
    cy.get('input[placeholder*="+33"]').type('+33612345678');

    cy.get('input[type="password"]').then(($inputs) => {
      cy.wrap($inputs[0]).type('password123');
      cy.wrap($inputs[1]).type('different123');
    });

    cy.get('input[type="checkbox"]').check();
    cy.get('button').contains('Créer mon compte').click();

    // Should show error
    cy.get('div').should('contain', 'Les mots de passe ne correspondent pas');
  });

  it('should register influencer successfully', () => {
    const email = `influencer${Date.now()}@test.com`;

    cy.get('button').contains('Influenceur').click();

    // Fill form
    cy.get('input[placeholder="Jean"]').type('Sarah');
    cy.get('input[placeholder="Dupont"]').type('Benali');
    cy.get('input[placeholder="mon_username"]').type('sarahbenali');
    cy.get('input[placeholder="email@exemple"]').type(email);
    cy.get('input[placeholder*="+33"]').type('+33623456789');

    cy.get('input[type="password"]').then(($inputs) => {
      cy.wrap($inputs[0]).type('Password123');
      cy.wrap($inputs[1]).type('Password123');
    });

    cy.get('input[type="checkbox"]').check();
    cy.get('button').contains('Créer mon compte').click();

    cy.get('h2').should('contain', 'Inscription réussie');
  });
});
```

### Playwright Version

```javascript
test.describe('Complete Registration Flow', () => {
  test('should register merchant successfully', async ({ page }) => {
    const email = `merchant${Date.now()}@test.com`;
    const password = 'TestPassword123';

    await page.goto('http://localhost:3000/register');

    // Step 1: Role selection
    await page.getByRole('button', { name: /Entreprise/i }).click();

    // Step 2: Fill form
    await page.getByPlaceholder(/Jean/).fill('Jean');
    await page.getByPlaceholder(/Dupont/).fill('Dupont');
    await page.getByPlaceholder(/Mon Entreprise/).fill('TestCorp');
    await page.getByPlaceholder(/email@exemple/).fill(email);
    await page.getByPlaceholder(/\+33/).fill('+33612345678');

    const passwordInputs = await page.locator('input[type="password"]').all();
    await passwordInputs[0].fill(password);
    await passwordInputs[1].fill(password);

    // Accept terms
    await page.getByRole('checkbox').check();

    // Submit
    await page.getByRole('button', { name: /Créer mon compte/i }).click();

    // Verify success
    await expect(page.locator('h2')).toContainText('Inscription réussie');

    // Verify redirect
    await page.waitForURL('/login');
  });

  test('should validate duplicate email', async ({ page }) => {
    await page.goto('http://localhost:3000/register');

    await page.getByRole('button', { name: /Entreprise/i }).click();

    // Use existing email
    await page.getByPlaceholder(/Jean/).fill('Jean');
    await page.getByPlaceholder(/Dupont/).fill('Dupont');
    await page.getByPlaceholder(/Mon Entreprise/).fill('TestCorp');
    await page.getByPlaceholder(/email@exemple/).fill('admin@shareyoursales.ma');
    await page.getByPlaceholder(/\+33/).fill('+33612345678');

    const passwordInputs = await page.locator('input[type="password"]').all();
    await passwordInputs[0].fill('Password123');
    await passwordInputs[1].fill('Password123');

    await page.getByRole('checkbox').check();
    await page.getByRole('button', { name: /Créer mon compte/i }).click();

    // Should show error
    await expect(page.locator('text=Email already exists')).toBeVisible();
  });
});
```

---

## SCÉNARIO 3: CONTACT FORM SUBMISSION (P2)

### Cypress

```javascript
describe('Contact Form', () => {
  it('should submit contact form successfully', () => {
    cy.visit('http://localhost:3000/contact');

    cy.get('input[name="name"]').type('Jean Dupont');
    cy.get('input[name="email"]').type('test@example.com');
    cy.get('input[name="phone"]').type('+33612345678');
    cy.get('input[name="subject"]').type('Test Subject');
    cy.get('select[name="category"]').select('support');
    cy.get('textarea[name="message"]').type('This is a test message');

    cy.get('button[type="submit"]').click();

    // Toast should appear
    cy.get('[data-testid="toast-success"]').should('be.visible');
    cy.get('[data-testid="toast-success"]').should('contain', 'succès');

    // Form should reset
    cy.get('input[name="name"]').should('have.value', '');
    cy.get('input[name="email"]').should('have.value', '');
  });

  it('should prefill logged-in user data', () => {
    // Login first
    cy.login('admin@shareyoursales.ma', 'Admin123');

    cy.visit('http://localhost:3000/contact');

    // Verify prefill
    cy.get('input[name="name"]').should('have.value', 'Admin User');
    cy.get('input[name="email"]').should('have.value', 'admin@shareyoursales.ma');
  });
});
```

---

## SCÉNARIO 4: SETTINGS UPDATE FLOW (P2)

### Cypress

```javascript
describe('Personal Settings Update', () => {
  beforeEach(() => {
    cy.login('admin@shareyoursales.ma', 'Admin123');
    cy.visit('http://localhost:3000/settings/personal');
  });

  it('should update personal settings', () => {
    // Change first name
    cy.get('input[name="first_name"]').clear().type('UpdatedName');

    // Submit form
    cy.get('button[type="submit"]').click();

    // Success message
    cy.get('[data-testid="toast-success"]').should('contain', 'succès');

    // Reload and verify persistence
    cy.reload();
    cy.get('input[name="first_name"]').should('have.value', 'UpdatedName');
  });

  it('should validate email format', () => {
    cy.get('input[name="email"]').clear().type('invalid-email');
    cy.get('button[type="submit"]').click();

    // HTML5 validation
    cy.get('input[name="email"]').then(($input) => {
      expect($input[0].validationMessage).to.contain('email');
    });
  });
});
```

---

## SCÉNARIO 5: ERROR RECOVERY (P2)

### Cypress

```javascript
describe('Error Recovery', () => {
  it('should recover from network error', () => {
    cy.visit('http://localhost:3000/login');

    // Go offline
    cy.intercept('POST', '**/api/**', { statusCode: 0 });

    cy.get('[data-testid="email-input"]').type('admin@shareyoursales.ma');
    cy.get('[data-testid="password-input"]').type('Admin123');
    cy.get('[data-testid="login-button"]').click();

    // Should show error
    cy.get('[data-testid="error-message"]').should('be.visible');

    // Go online and retry
    cy.intercept('POST', '**/api/auth/login', {
      statusCode: 200,
      body: { success: true, access_token: 'token123' }
    });

    cy.get('[data-testid="login-button"]').click();
    cy.url().should('include', '/dashboard');
  });

  it('should handle 500 server error gracefully', () => {
    cy.visit('http://localhost:3000/login');

    cy.intercept('POST', '**/api/auth/login', {
      statusCode: 500,
      body: { detail: 'Internal server error' }
    });

    cy.get('[data-testid="email-input"]').type('admin@shareyoursales.ma');
    cy.get('[data-testid="password-input"]').type('Admin123');
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="error-message"]').should('be.visible');
  });
});
```

---

## HELPER FUNCTIONS (Custom Commands)

### Cypress Helpers

```javascript
// cypress/support/commands.js

Cypress.Commands.add('login', (email, password) => {
  cy.visit('http://localhost:3000/login');
  cy.get('[data-testid="email-input"]').type(email);
  cy.get('[data-testid="password-input"]').type(password);
  cy.get('[data-testid="login-button"]').click();
  cy.url().should('include', '/dashboard');
  cy.get('[data-testid="dashboard-header"]').should('be.visible');
});

Cypress.Commands.add('logout', () => {
  cy.visit('http://localhost:3000');
  cy.get('[data-testid="logout-button"]').click();
  cy.url().should('include', '/login');
});

Cypress.Commands.add('fillForm', (formData) => {
  Object.entries(formData).forEach(([name, value]) => {
    cy.get(`input[name="${name}"], textarea[name="${name}"]`).type(value);
  });
});
```

### Playwright Helpers

```javascript
// tests/helpers.js

export async function login(page, email, password) {
  await page.goto('http://localhost:3000/login');
  await page.getByTestId('email-input').fill(email);
  await page.getByTestId('password-input').fill(password);
  await page.getByTestId('login-button').click();
  await page.waitForURL('/dashboard');
}

export async function logout(page) {
  await page.getByTestId('logout-button').click();
  await page.waitForURL('/login');
}

export async function fillForm(page, formData) {
  for (const [name, value] of Object.entries(formData)) {
    const selector = `input[name="${name}"], textarea[name="${name}"]`;
    await page.fill(selector, value);
  }
}
```

---

## RUNNING THE TESTS

### Cypress
```bash
# Interactive mode
npm run cypress:open

# Headless mode
npm run cypress:run

# Single test file
npm run cypress:run -- --spec "cypress/e2e/forms/login.cy.js"

# With specific browser
npm run cypress:run -- --browser chrome
```

### Playwright
```bash
# Run all tests
npm run playwright test

# Run specific test file
npm run playwright test tests/login.spec.js

# Run with specific browser
npm run playwright test --project=chromium

# Debug mode
npm run playwright test --debug

# Record videos
npm run playwright test --record
```

### Jest/RTL
```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Specific file
npm test Login.test.js
```

---

## CI/CD INTEGRATION

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - run: npm ci
      - run: npm run build

      - name: Run Cypress tests
        uses: cypress-io/github-action@v5
        with:
          start: npm start
          wait-on: 'http://localhost:3000'
          spec: 'cypress/e2e/**/*.cy.js'

      - name: Run Playwright tests
        run: npm run playwright test

      - name: Run Jest tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

---

## METRICS & TARGETS

### Coverage Goals
- **Unit Tests:** 80% coverage
- **Integration Tests:** 100% of critical paths
- **E2E Tests:** All P1 scenarios
- **Overall:** 70%+ coverage

### Performance Targets
- Form load time: < 2 seconds
- Form submit time: < 3 seconds
- API response: < 1 second
- Lighthouse Score: > 90

### Success Criteria
- All P1 scenarios pass
- No regressions
- Performance metrics met
- Accessibility audit passes
- Zero critical bugs

