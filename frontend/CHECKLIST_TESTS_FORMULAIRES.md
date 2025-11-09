# CHECKLIST COMPLÈTE DES TESTS FORMULAIRES

## Format: [FORM] - [TEST TYPE] - [STATUS]

### Legend:
- ✓ = Implémenté/Réussi
- ✗ = Manquant/Échoué
- ⚠️ = À Vérifier
- ⏳ = En Cours
- N/A = Non Applicable

---

## 1. LOGIN FORM

### 1.1 Rendu & UI
```
✗ Email input visible et accessible
✗ Password input visible et accessible
✗ Submit button visible et accessible
✗ "Register" link visible
✗ "Forgot Password" link visible
✗ Quick login buttons visible
✗ 2FA form appears when needed
✗ Error message styling correct
✗ Loading spinner visible
✗ Mobile responsive
```

### 1.2 Input Handling
```
✗ Email input accepts text
✗ Password input accepts text
✗ Password input masks characters
✗ Tab navigation works
✗ Enter key submits form
✗ Clear button works (if implemented)
✗ Input max length enforced
✗ Input auto-trim whitespace
```

### 1.3 Validation - Client Side
```
✗ Email required validation
✗ Password required validation
✗ Email format validation
✗ Email regex works correctly
✗ Shows error on invalid email
✗ Shows error on empty email
✗ Shows error on empty password
✗ Error messages in correct language
```

### 1.4 Form Submission
```
✗ Calls login API on submit
✗ Sends correct payload
✗ Button disabled during loading
✗ Button shows loading text
✗ No double submission possible
✗ Clears sensitive data on unmount
✗ Calls preventDefault on form
✗ Submits on Enter key
```

### 1.5 Success Flow
```
✗ Redirects to /dashboard on success
✗ Stores token in localStorage
✗ Stores user data in localStorage
✗ Clears form on success
✗ Shows success message (if implemented)
✗ Respects redirectAfterLogin param
✗ Respects pendingPlanSelection
```

### 1.6 Error Handling
```
✗ Shows error message on 401
✗ Shows error message on 500
✗ Shows network error message
✗ Error message is clear and helpful
✗ Allows retry after error
✗ Clears error on new input
✗ Handles API timeout gracefully
✗ Handles malformed response
```

### 1.7 2FA Flow
```
✗ Shows 2FA form after credentials
✗ 2FA input accepts 6 digits
✗ 2FA input limits to 6 chars
✗ Submits 2FA code
✗ Shows error on invalid code
✗ Allows back to email/password
✗ Stores temp token correctly
✗ Validates code length before submit
```

### 1.8 Quick Login
```
✗ Admin quick login works
✗ Influencer quick login works
✗ Merchant quick login works
✗ Quick login buttons disabled during loading
✗ Quick login shows correct account info
✗ Quick login displays credentials info
```

### 1.9 Security
```
✗ Password not visible in logs
✗ XSS prevention works
✗ CSRF token present (if required)
✗ No sensitive data in localStorage (except token)
✗ HTTPS enforced in production
✗ Secure cookie flags set
✗ No password in URL params
✗ Rate limiting works (if implemented)
```

### 1.10 Accessibility
```
✗ Form has aria-label
✗ Inputs have associated labels
✗ Error messages announced to screen readers
✗ Loading state announced
✗ Keyboard navigation works
✗ Tab order is logical
✗ Color contrast ratio sufficient
✗ Focus visible on all elements
```

### 1.11 Performance
```
✗ Form loads < 2 seconds
✗ API response < 1 second
✗ No memory leaks on unmount
✗ No unnecessary re-renders
✗ Optimized for slow network
✗ No console errors
✗ No console warnings
```

---

## 2. REGISTER FORM

### 2.1 Step 1: Role Selection
```
✗ Role selection page loads
✗ "Entrepreneur/Company" option visible
✗ "Influencer/Commercial" option visible
✗ Options are clickable
✗ Options show correct icons
✗ Hover effects work
✗ Keyboard navigation works
✗ Mobile layout correct
```

### 2.2 Step 2: Form Fields
```
✗ First name input visible
✗ Last name input visible
✗ Email input visible
✗ Phone input visible
✗ Password input visible
✗ Confirm password input visible
✗ Company name (merchant) visible
✗ Username (influencer) visible
✗ Terms checkbox visible
✗ Submit button visible
✗ Back button visible
```

### 2.3 Input Handling
```
✗ All inputs accept text
✗ Password input masks characters
✗ Phone input formats correctly
✗ Email input validates format
✗ Inputs don't lose focus on error
✗ Inputs auto-fill from password manager
✗ Back button returns to role selection
✗ Form doesn't lose data on back
```

### 2.4 Validation - Client Side
```
✗ First name required
✗ Last name required
✗ Email required
✗ Email format validation
✗ Phone required
✗ Password required
✗ Password min 6 characters
✗ Confirm password required
✗ Passwords must match
✗ Company name required (merchant)
✗ Username required (influencer)
✗ Terms checkbox required
✗ Error message on each failed field
```

### 2.5 Validation - Server Side
```
✗ Duplicate email rejected
✗ Invalid email format rejected
✗ Weak password rejected
✗ Invalid phone format rejected
✗ Role validation on server
✗ Clear error message displayed
✗ Allows correction and retry
```

### 2.6 Form Submission
```
✗ All required fields filled -> submits
✗ Some fields empty -> doesn't submit
✗ Passwords don't match -> doesn't submit
✗ Button disabled during loading
✗ Button shows loading text
✗ API call sent with correct data
✗ Merchant data includes company_name
✗ Influencer data includes username
✗ No double submission
```

### 2.7 Success Flow
```
✗ Success page shows "Inscription réussie"
✗ CheckCircle icon visible
✗ Loading spinner shows
✗ Auto-redirect to /login (3 seconds)
✗ Prevents accidental back navigation
✗ New account can login
✗ User data correctly saved
```

### 2.8 Error Handling
```
✗ Duplicate email shows error
✗ Server error (500) shows error
✗ Network error shows error
✗ Validation errors show per-field
✗ Errors are clear and actionable
✗ Can retry after error
✗ Form keeps data after error
```

### 2.9 URL Parameters
```
✗ /register?role=merchant skips step 1
✗ /register?role=influencer skips step 1
✗ /register?plan=pro prefills plan (if shown)
✗ Invalid role param ignored
```

### 2.10 Security
```
✗ Password not shown in plaintext
✗ Password not in logs
✗ No sensitive data leak
✗ XSS prevention works
✗ CSRF token present (if required)
✗ No duplicate account creation possible
✗ Rate limiting works
```

### 2.11 Accessibility
```
✗ Form has proper labels
✗ Step indicator accessible
✗ Error messages announced
✗ Keyboard navigation works
✗ Tab order correct
✗ Focus management good
✗ Color contrast sufficient
```

---

## 3. CONTACT FORM

### 3.1 Form Fields
```
✗ Name input visible
✗ Email input visible
✗ Phone input visible (optional)
✗ Subject input visible
✗ Category dropdown visible
✗ Message textarea visible
✗ Submit button visible
✗ Reset button visible
```

### 3.2 Input Handling
```
✗ All inputs accept text
✗ Textarea accepts multi-line
✗ Category dropdown opens
✗ All categories available
✗ Inputs are editable
✗ Inputs can be cleared
✗ Tab navigation works
```

### 3.3 Validation
```
✗ Name required
✗ Email required
✗ Email format validation
✗ Subject required
✗ Message required
✗ Shows error on submit with empty fields
✗ Error messages clear
```

### 3.4 Auto-fill for Logged-in Users
```
✗ Logged-in user name prefilled
✗ Logged-in user email prefilled
✗ Logged-in user phone prefilled (if available)
✗ Can override prefilled data
```

### 3.5 Submission
```
✗ Sends correct payload
✗ API call to /api/contact
✗ Button disabled during loading
✗ Shows loading state
✗ No double submission
```

### 3.6 Success
```
✗ Shows success message
✗ Toast notification appears
✗ Message is "succès" or similar
✗ Form resets on success
✗ All fields cleared
```

### 3.7 Error Handling
```
✗ Shows error message on failure
✗ Allows retry
✗ Network error handled
✗ Form data preserved
```

### 3.8 Security
```
✗ XSS prevention works
✗ Input sanitization
✗ No script execution
✗ CSRF token present (if required)
```

### 3.9 Accessibility
```
✗ Form labeled properly
✗ Error messages announced
✗ Keyboard navigation works
✗ Contrast sufficient
```

---

## 4. CREATE LEAD FORM (Influencer)

### 4.1 Form Fields
```
✗ Campaign dropdown visible
✗ Customer name input visible
✗ Customer email input visible
✗ Customer phone input visible
✗ Company name input visible
✗ Notes textarea visible
✗ Estimated value input visible
✗ Source dropdown visible
✗ Submit button visible
```

### 4.2 Validation
```
✗ Campaign required
✗ Customer name required
✗ Customer email required (format)
✗ Customer phone required
✗ Estimated value required (number)
✗ Source required
✗ Shows errors on submit
```

### 4.3 Dynamic Behavior
```
✗ Campaign dropdown loads campaigns
✗ Commission previewed on value change
✗ Deposit availability checked
✗ Real-time calculation works
✗ Values update immediately
```

### 4.4 Submission
```
✗ Sends correct data to API
✗ Includes commission info
✗ Button disabled during loading
✗ Shows success message
✗ Form resets on success
```

### 4.5 Error Handling
```
✗ Shows error if deposit unavailable
✗ Prevents submission if deposit insufficient
✗ Shows calculation errors
✗ Network errors handled
```

---

## 5. CREATE CAMPAIGN FORM

### 5.1 Form Fields
```
✗ Name input visible
✗ Description textarea visible
✗ Category dropdown visible
✗ Commission type dropdown visible
✗ Commission value input visible
✗ Start date input visible
✗ End date input visible
✗ Budget input visible (optional)
✗ Product selection visible
✗ Briefing fields visible
✗ Submit button visible
```

### 5.2 Validation
```
✗ Name required
✗ Description required
✗ Category required
✗ Commission value is number
✗ Dates valid
✗ Start date before end date
✗ Product selection optional but multiple possible
```

### 5.3 Submission
```
✗ Sends campaign data
✗ Includes briefing info
✗ Includes product list
✗ Button disabled during loading
✗ Shows success/error message
```

---

## 6. SETTINGS FORMS

### 6.1 Personal Settings
```
✗ First name field editable
✗ Last name field editable
✗ Email field shows (read-only if not editable)
✗ Phone field editable
✗ Timezone selector works
✗ Language selector works
✗ Submit button functional
✗ Success message shows
✗ Changes persist on reload
```

### 6.2 Security Settings
```
✗ Current password input
✗ New password input
✗ Confirm password input
✗ Password visibility toggle works
✗ Password match validation
✗ Password strength indicator (if implemented)
✗ 2FA enable/disable works
✗ IP whitelist management works
✗ Success message shows
```

### 6.3 Payment Settings
```
✗ Payment method dropdown
✗ Bank details fields appear (if method=bank)
✗ IBAN validation works
✗ PayPal email field appears (if method=paypal)
✗ Stripe fields appear (if method=stripe)
✗ Details saved correctly
✗ Can edit and update
✗ Pre-filled with existing data
```

### 6.4 All Settings
```
✗ Loading state while fetching
✗ Save button disabled during submit
✗ Success message after save
✗ Error message on failure
✗ Can retry after error
✗ Form preserves data on error
```

---

## 7. UNIVERSAL FORM TESTS

### 7.1 Loading States
```
✗ Form shows skeleton/loader while loading
✗ Submit button disabled during loading
✗ Submit button shows loading text
✗ No interaction possible during loading
✗ Loading spinner visible
✗ Timeout handled (if > 5 seconds)
```

### 7.2 Error States
```
✗ Error message visible
✗ Error message styled appropriately
✗ Error message has icon
✗ Error message readable
✗ Multiple errors shown (if multiple fields fail)
✗ Field-level errors shown
✗ Form-level errors shown
✗ Errors cleared on input
```

### 7.3 Success States
```
✗ Success message visible
✗ Toast notification shown (if applicable)
✗ Success message has icon
✗ Success message readable
✗ Auto-dismiss (if applicable)
✗ Manual dismiss available
✗ Redirect happens (if applicable)
✗ Form resets (if applicable)
```

### 7.4 Data Persistence
```
✗ Form data saved in localStorage (if applicable)
✗ Reloading page doesn't lose data
✗ Can continue after accidental close
✗ No data loss on error
✗ Sensitive data not stored
```

### 7.5 Accessibility - All Forms
```
✗ Form has <form> tag
✗ Submit button type="submit"
✗ All inputs have labels
✗ Labels properly associated with inputs
✗ Error messages associated with inputs
✗ Error messages have aria-live="polite"
✗ Loading state announced
✗ Success message announced
✗ Keyboard navigation works
✗ Tab order logical
✗ Focus management good
✗ Color contrast >= 4.5:1
✗ No color-only information
```

### 7.6 Security - All Forms
```
✗ XSS prevention (input sanitized)
✗ CSRF token sent (if required)
✗ No sensitive data in URL
✗ No sensitive data in localStorage (except auth token)
✗ HTTPS enforced
✗ Secure cookie flags
✗ Rate limiting on submit (if implemented)
✗ Input max length enforced
✗ Input type="password" for passwords
✗ Input type="email" for emails
```

### 7.7 Mobile Responsiveness
```
✗ Form responsive on 320px (mobile)
✗ Form responsive on 768px (tablet)
✗ Form responsive on 1024px (desktop)
✗ Inputs are touch-friendly (min 48px height)
✗ Labels visible on mobile
✗ Error messages readable on mobile
✗ Buttons clickable on mobile
✗ No horizontal scrolling
```

### 7.8 Cross-browser Compatibility
```
✗ Works on Chrome 90+
✗ Works on Firefox 88+
✗ Works on Safari 14+
✗ Works on Edge 90+
✗ Works on mobile Safari
✗ Works on mobile Chrome
✗ Works on Samsung Internet
```

### 7.9 Performance
```
✗ Form loads < 2 seconds
✗ No lighthouse warnings
✗ No memory leaks
✗ No unnecessary re-renders
✗ Optimized bundle size
✗ No jank on interaction
✗ No console errors
✗ No console warnings
```

### 7.10 Browser DevTools
```
✗ No console errors
✗ No console warnings (excluding third-party)
✗ No React warnings
✗ Network tab shows expected requests
✗ No failed network requests
✗ API calls have correct headers
✗ Responses are valid JSON
✗ No sensitive data in Network tab
```

---

## SUMMARY TABLE

| Form | Rendering | Input | Validation | Submission | Success | Error | Security | Accessibility | Performance |
|------|-----------|-------|-----------|-----------|---------|-------|----------|--------------|-------------|
| Login | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Register | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Contact | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Create Lead | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Create Campaign | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Personal Settings | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Security Settings | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Payment Settings | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

---

## REGRESSION TEST CHECKLIST

After each code change, verify:

```
[ ] Login still works
[ ] Register still works
[ ] All error messages still display
[ ] Loading states still work
[ ] No new console errors
[ ] No new accessibility violations
[ ] Performance unchanged
[ ] Mobile still works
[ ] Cross-browser still works
[ ] API calls still correct
[ ] No data loss
```

---

## FINAL CHECKLIST BEFORE PRODUCTION

```
[ ] All P1 forms tested manually
[ ] All P2 forms tested manually
[ ] Unit tests written and passing
[ ] Integration tests written and passing
[ ] E2E tests written and passing
[ ] Security tests passed
[ ] Accessibility audit passed
[ ] Performance audit passed
[ ] Code review completed
[ ] No console errors
[ ] No console warnings
[ ] Lint checks passed
[ ] Build successful
[ ] Test coverage > 80%
[ ] Documentation updated
[ ] Change log updated
```

---

## NOTES

Last Updated: November 9, 2025
Tester: _________________
Status: [ ] IN PROGRESS [ ] COMPLETED [ ] BLOCKED

