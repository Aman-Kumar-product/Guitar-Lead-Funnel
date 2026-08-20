# Application Hygiene Checks

This document outlines a comprehensive list of hygiene checks and validation rules that should be implemented across the application to ensure data quality, security, and a robust user experience.

## 1. Input Validation & Data Quality

### Phone Number Validation
- [ ] **Length:** Must be exactly 10 digits (adjust based on expected country codes if international).
- [ ] **Format:** Strip any non-numeric characters (dashes, spaces, parentheses) before validation or submission.
- [ ] **Block Consecutive/Identical Sequences:** Reject inputs like `0000000000`, `1111111111`, `9999999999`.
- [ ] **Block Common Dummy Numbers:** Reject common fake sequences such as:
  - `1234567890`
  - `0987654321`
  - `9876543210`
  - `0123456789`
- [ ] **Valid Starts:** Depending on the region, ensure the phone number starts with a valid digit (e.g., in the US, an area code cannot start with 0 or 1).

### Email Address Validation
- [ ] **Format Validation:** Must pass standard email Regex (e.g., `^[^\s@]+@[^\s@]+\.[^\s@]+$`).
- [ ] **Block Dummy Emails:** Reject obvious fake emails like `test@test.com`, `example@example.com`, `a@a.com`, `dummy@dummy.com`.
- [ ] **Typo Catching (Optional):** Suggest corrections for common domain typos (e.g., `gamil.com` -> `gmail.com`).
- [ ] **Trailing/Leading Whitespace:** Automatically `.trim()` inputs before validation.

### Name Validation (First Name / Last Name)
- [ ] **Length Limits:** Minimum 2 characters, maximum ~50 characters.
- [ ] **Character Restrictions:** Only allow letters, spaces, hyphens, and apostrophes. Reject numbers and special symbols (`!@#$%^&*()`).
- [ ] **Block Dummy Names:** Reject inputs like `test`, `asdf`, `qwer`, `admin`, `null`.

## 2. Form & Submission Handling

- [ ] **Prevent Double Submissions:** Disable the submit button immediately upon the first click and show a loading spinner/state.
- [ ] **Error Visibility:** Display clear, human-readable validation error messages near the respective input fields (not just generic alerts).
- [ ] **Success Feedback:** Provide clear visual feedback upon successful submission (e.g., redirect to a Thank You page, display a success toast/modal).
- [ ] **Bot Prevention:** Implement a honeypot field (hidden input that bots might fill but real users won't) or integrate CAPTCHA/Turnstile.
- [ ] **Required Fields:** Ensure all mandatory fields are clearly marked (e.g., with an `*`) and validated on both frontend and backend.

## 3. Security & Data Sanitization

- [ ] **Cross-Site Scripting (XSS):** Ensure all user inputs are sanitized before rendering. (React handles most of this by default, but avoid `dangerouslySetInnerHTML`).
- [ ] **SQL Injection Prevention:** Backend must use parameterized queries or an ORM for all database interactions.
- [ ] **Rate Limiting:** Implement rate limiting on the backend API endpoints (especially form submissions) to prevent spam/DDoS.
- [ ] **Secret Management:** Ensure NO API keys, database URIs, or secrets are hardcoded in the frontend code or committed to version control.

## 4. Error Handling & Logging

- [ ] **Graceful Failures:** If the backend is down, the frontend should show a user-friendly error message ("Something went wrong, please try again later") rather than crashing.
- [ ] **No Stack Traces in Production:** Ensure backend errors do not leak stack traces or sensitive database structure details to the client network response.

## 5. Accessibility (A11y) & UX

- [ ] **Labels:** All inputs must have associated `<label>` elements or `aria-label` attributes for screen readers.
- [ ] **Keyboard Navigation:** Forms must be fully navigable using the `Tab` key, and the `Enter` key should trigger form submission when focused inside an input.
- [ ] **Focus States:** Input fields and buttons should have clear visual focus rings for keyboard users.
- [ ] **Contrast:** Ensure text and placeholder contrast meets WCAG accessibility guidelines against the background.
- [ ] **Responsive Design:** Verify form layouts scale properly on small mobile screens without horizontal scrolling or overlapping elements.
