# SETUP COMPLET DES TESTS - FORMULAIRES

## 1. INSTALLATION DÉPENDANCES

### 1.1 Dépendances de Test

```bash
# Jest & React Testing Library
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest

# Cypress (optionnel)
npm install --save-dev cypress @testing-library/cypress

# Playwright (optionnel)
npm install --save-dev @playwright/test

# Mocking
npm install --save-dev jest-mock-axios @testing-library/jest-dom

# Coverage
npm install --save-dev @testing-library/jest-dom
```

### 1.2 Vérification Installation

```bash
npm test -- --version
npx cypress --version
npx playwright --version
```

---

## 2. CONFIGURATION JEST

### 2.1 jest.config.js

```javascript
module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
  moduleFileExtensions: ['js', 'jsx', 'json'],
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/index.js',
    '!src/serviceWorkerRegistration.js',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/src/__mocks__/fileMock.js'
  },
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest'
  }
};
```

### 2.2 src/setupTests.js

```javascript
// jest-dom adds custom jest matchers
import '@testing-library/jest-dom';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock window.fetch
global.fetch = jest.fn();

// Suppress console errors in tests
const originalError = console.error;
beforeAll(() => {
  console.error = (...args) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Warning: ReactDOM.render')
    ) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});
```

### 2.3 .babelrc

```json
{
  "presets": [
    ["@babel/preset-env", { "targets": { "node": "current" } }],
    ["@babel/preset-react", { "runtime": "automatic" }]
  ]
}
```

---

## 3. CONFIGURATION CYPRESS

### 3.1 cypress.config.js

```javascript
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    pageLoadTimeout: 30000,

    setupNodeEvents(on, config) {
      // Events
    },

    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.js',
  },

  component: {
    devServer: {
      framework: 'react',
      bundler: 'webpack',
    },
  },
});
```

### 3.2 cypress/support/e2e.js

```javascript
import './commands';

beforeEach(() => {
  cy.clearLocalStorage();
  cy.clearCookies();
});
```

### 3.3 cypress/support/commands.js

```javascript
// Login command
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('[data-testid="email-input"]').type(email);
  cy.get('[data-testid="password-input"]').type(password);
  cy.get('[data-testid="login-button"]').click();
  cy.url().should('include', '/dashboard');
});

// Logout command
Cypress.Commands.add('logout', () => {
  cy.get('[data-testid="logout-button"]').click();
  cy.url().should('include', '/login');
});

// Fill form command
Cypress.Commands.add('fillForm', (formData) => {
  Object.entries(formData).forEach(([name, value]) => {
    cy.get(`input[name="${name}"], textarea[name="${name}"], select[name="${name}"]`)
      .type(value);
  });
});

// Check error message
Cypress.Commands.add('checkError', (message) => {
  cy.get('[data-testid="error-message"]')
    .should('be.visible')
    .should('contain', message);
});

// Check success message
Cypress.Commands.add('checkSuccess', (message) => {
  cy.get('[data-testid="toast-success"]')
    .should('be.visible')
    .should('contain', message);
});
```

---

## 4. CONFIGURATION PLAYWRIGHT

### 4.1 playwright.config.js

```javascript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### 4.2 tests/fixtures/auth.js

```javascript
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Login
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'admin@shareyoursales.ma');
    await page.fill('[data-testid="password-input"]', 'Admin123');
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/dashboard');

    // Use the page
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

---

## 5. STRUCTURE DOSSIERS TESTS

```
frontend/
├── src/
│   ├── __tests__/
│   │   ├── __mocks__/
│   │   │   ├── fileMock.js
│   │   │   └── apiMock.js
│   │   ├── forms/
│   │   │   ├── Login.test.js
│   │   │   ├── Register.test.js
│   │   │   ├── Contact.test.js
│   │   │   ├── CreateLead.test.js
│   │   │   └── Settings.test.js
│   │   ├── hooks/
│   │   │   ├── useForm.test.js
│   │   │   └── useAuth.test.js
│   │   ├── components/
│   │   │   ├── Button.test.js
│   │   │   └── Card.test.js
│   │   └── setupTests.js
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   └── utils/
├── cypress/
│   ├── e2e/
│   │   ├── forms/
│   │   │   ├── login.cy.js
│   │   │   ├── register.cy.js
│   │   │   └── contact.cy.js
│   │   └── integration/
│   │       ├── auth-flow.cy.js
│   │       └── form-validation.cy.js
│   ├── support/
│   │   ├── e2e.js
│   │   └── commands.js
│   └── fixtures/
│       └── users.json
├── tests/
│   ├── fixtures/
│   │   └── auth.js
│   ├── forms/
│   │   ├── login.spec.js
│   │   └── register.spec.js
│   ├── e2e/
│   │   └── auth-flow.spec.js
│   └── utils/
│       └── test-helpers.js
├── jest.config.js
├── cypress.config.js
└── playwright.config.js
```

---

## 6. NPM SCRIPTS

### 6.1 package.json

```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test --coverage",
    "test:watch": "react-scripts test",
    "test:ci": "react-scripts test --ci --coverage",
    "cypress:open": "cypress open",
    "cypress:run": "cypress run",
    "cypress:run:ci": "cypress run --headless",
    "playwright:test": "playwright test",
    "playwright:ui": "playwright test --ui",
    "playwright:debug": "playwright test --debug",
    "test:all": "npm run test:ci && npm run cypress:run:ci && npm run playwright:test",
    "lint": "eslint src",
    "format": "prettier --write src"
  }
}
```

---

## 7. EXÉCUTION DES TESTS

### 7.1 Tests Unitaires (Jest)

```bash
# Mode watch
npm run test:watch

# Mode CI
npm run test:ci

# Coverage report
npm test -- --coverage

# Fichier spécifique
npm test Login.test.js

# Pattern spécifique
npm test -- --testNamePattern="should login"
```

### 7.2 Tests E2E (Cypress)

```bash
# Mode interactif
npm run cypress:open

# Headless mode
npm run cypress:run

# Fichier spécifique
npm run cypress:run -- --spec "cypress/e2e/forms/login.cy.js"

# Browser spécifique
npm run cypress:run -- --browser chrome

# Video recording
npm run cypress:run -- --record
```

### 7.3 Tests E2E (Playwright)

```bash
# Run all tests
npm run playwright:test

# UI mode
npm run playwright:ui

# Debug mode
npm run playwright:debug

# Fichier spécifique
npm run playwright:test tests/forms/login.spec.js

# Browser spécifique
npm run playwright:test -- --project=chromium

# Headed mode
npm run playwright:test -- --headed
```

### 7.4 Tous les Tests

```bash
npm run test:all
```

---

## 8. MOCKS & STUBS

### 8.1 src/__mocks__/apiMock.js

```javascript
import axios from 'axios';
jest.mock('axios');

export const mockLoginSuccess = {
  data: {
    success: true,
    access_token: 'test-token-123',
    user: {
      id: 1,
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User'
    }
  }
};

export const mockLoginError = {
  response: {
    status: 401,
    data: {
      detail: 'Email ou mot de passe incorrect'
    }
  }
};

export const setupMocks = () => {
  axios.post.mockResolvedValue(mockLoginSuccess);
  axios.get.mockResolvedValue({ data: {} });
  axios.put.mockResolvedValue({ data: { success: true } });
};

export const resetMocks = () => {
  jest.clearAllMocks();
};
```

### 8.2 src/__mocks__/fileMock.js

```javascript
module.exports = 'test-file-stub';
```

### 8.3 Test Fixtures

```javascript
// tests/fixtures/testData.js

export const testUsers = {
  admin: {
    email: 'admin@shareyoursales.ma',
    password: 'Admin123',
    name: 'Admin User'
  },
  merchant: {
    email: 'merchant@shareyoursales.ma',
    password: 'Merchant123',
    name: 'Test Merchant'
  },
  influencer: {
    email: 'influencer@shareyoursales.ma',
    password: 'Influencer123',
    name: 'Test Influencer'
  }
};

export const testForms = {
  validLogin: {
    email: 'admin@shareyoursales.ma',
    password: 'Admin123'
  },
  invalidLogin: {
    email: 'admin@shareyoursales.ma',
    password: 'WrongPassword'
  },
  validRegister: {
    first_name: 'Jean',
    last_name: 'Dupont',
    email: 'newuser@example.com',
    phone: '+33612345678',
    password: 'TestPassword123',
    confirm_password: 'TestPassword123',
    company_name: 'TestCorp'
  }
};
```

---

## 9. CI/CD INTEGRATION

### 9.1 GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v3

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Jest tests
        run: npm run test:ci

      - name: Run Cypress tests
        uses: cypress-io/github-action@v5
        with:
          start: npm start
          wait-on: 'http://localhost:3000'
          spec: 'cypress/e2e/**/*.cy.js'

      - name: Run Playwright tests
        run: npm run playwright:test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests
          name: codecov-umbrella

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: |
            coverage/
            playwright-report/
            cypress/videos/
```

---

## 10. DEBUGGING TESTS

### 10.1 Jest Debugging

```bash
# Debug with Node inspector
node --inspect-brk node_modules/.bin/jest --runInBand

# Attach to Chrome
# Open chrome://inspect

# VS Code launch.json
{
  "type": "node",
  "request": "launch",
  "name": "Jest Debug",
  "program": "${workspaceFolder}/node_modules/.bin/jest",
  "args": ["--runInBand"],
  "console": "integratedTerminal"
}
```

### 10.2 Cypress Debugging

```javascript
// In test
cy.pause(); // Pause execution
cy.log('Debug message'); // Log to console
cy.debug(); // Debug current subject
```

### 10.3 Playwright Debugging

```javascript
// In test
await page.pause(); // Pause execution
console.log(await page.content()); // Log page content
await page.screenshot({ path: 'screenshot.png' }); // Screenshot
```

---

## 11. BEST PRACTICES

### 11.1 Test Naming
```javascript
describe('Login Form', () => {
  it('should display email input field', () => {
    // ✓ GOOD: Clear intent
  });

  it('displays email field', () => {
    // ✗ BAD: Unclear intent
  });
});
```

### 11.2 Assertions
```javascript
// ✓ GOOD: Clear, specific
expect(screen.getByTestId('error-message')).toHaveTextContent('Email required');

// ✗ BAD: Vague
expect(screen.getByTestId('error-message')).toBeTruthy();
```

### 11.3 Async Handling
```javascript
// ✓ GOOD: Wait for element
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument();
});

// ✗ BAD: No wait
expect(screen.getByText(/success/i)).toBeInTheDocument();
```

---

## 12. COMMANDES ÚTILES

```bash
# Clean and reinstall
rm -rf node_modules package-lock.json && npm install

# Run tests with coverage
npm test -- --coverage

# Update snapshots
npm test -- -u

# Run tests matching pattern
npm test -- --testNamePattern="login"

# Run tests in file
npm test Login.test.js

# Cypress open in headless
npm run cypress:run -- --headless --headed=false

# Generate HTML report
npm test -- --coverage --coverageReporters="html"

# Clear Jest cache
npm test -- --clearCache
```

---

## 13. TROUBLESHOOTING

### 13.1 Common Issues

**Issue:** Tests timeout
```bash
# Solution: Increase timeout in jest.config.js
testTimeout: 30000
```

**Issue:** localStorage not clearing between tests
```javascript
// Solution: Add beforeEach
beforeEach(() => {
  localStorage.clear();
  jest.clearAllMocks();
});
```

**Issue:** Cypress hangs
```bash
# Solution: Clear cache and retry
npx cypress cache clear
npm run cypress:run
```

---

## 14. RESSOURCES SUPPLÉMENTAIRES

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Cypress Documentation](https://docs.cypress.io)
- [Playwright Documentation](https://playwright.dev)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

