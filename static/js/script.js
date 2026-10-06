/**
 * CAREER GUIDANCE EXPERT SYSTEM - CLIENT-SIDE SCRIPT (script.js)
 * Handles:
 *  - 5-Section Wizard Navigation & Progress Management
 *  - Form Validation on Step Transitions
 *  - Stepper Visual State Synchronization
 *  - Submission Loading State & Inference Trigger
 */

document.addEventListener('DOMContentLoaded', function () {
    let currentStep = 1;
    const totalSteps = 5;

    // Element References
    const form = document.getElementById('assessmentForm');
    if (!form) return; // Only execute on pages containing the assessment wizard

    const btnNext = document.getElementById('btnNext');
    const btnPrev = document.getElementById('btnPrev');
    const btnSubmit = document.getElementById('btnSubmit');
    const progressBar = document.getElementById('stepperProgressBar');
    const stepCounterBadge = document.getElementById('stepCounterBadge');
    const studentNameInput = document.getElementById('student_name');
    const nameError = document.getElementById('nameError');
    const stepperSteps = document.querySelectorAll('.stepper-node, .stepper-step');

    /**
     * Validates current section inputs before allowing transition to next section.
     */
    function validateCurrentStep(step) {
        if (step === 1) {
            const nameVal = studentNameInput.value.trim();
            const nameRegex = /^[a-zA-Z\s\-'.]+$/;
            if (!nameVal || !nameRegex.test(nameVal)) {
                studentNameInput.classList.add('is-invalid');
                if (nameError) {
                    nameError.textContent = !nameVal
                        ? 'Please enter your name to proceed.'
                        : "Full Name can only contain letters, spaces, hyphens (-), apostrophes ('), and periods (.)";
                    nameError.classList.remove('d-none');
                }
                studentNameInput.focus();
                return false;
            } else {
                studentNameInput.classList.remove('is-invalid');
                if (nameError) nameError.classList.add('d-none');
            }
        }
        return true;
    }

    /**
     * Updates visibility of sections and controls according to active step.
     */
    function updateStepView(newStep) {
        // Hide all sections
        for (let i = 1; i <= totalSteps; i++) {
            const sec = document.getElementById(`section-${i}`);
            if (sec) {
                sec.classList.add('d-none');
                sec.classList.remove('active');
            }
        }

        // Show active section
        const activeSection = document.getElementById(`section-${newStep}`);
        if (activeSection) {
            activeSection.classList.remove('d-none');
            activeSection.classList.add('active');
        }

        // Update Buttons
        if (newStep === 1) {
            btnPrev.style.display = 'none';
        } else {
            btnPrev.style.display = 'inline-block';
        }

        if (newStep === totalSteps) {
            btnNext.style.display = 'none';
            btnSubmit.style.display = 'inline-block';
        } else {
            btnNext.style.display = 'inline-block';
            btnSubmit.style.display = 'none';
        }

        // Update Stepper Progress Bar & Badges
        const progressPercentage = (newStep / totalSteps) * 100;
        if (progressBar) {
            progressBar.style.width = `${progressPercentage}%`;
        }

        if (stepCounterBadge) {
            stepCounterBadge.textContent = `Step ${newStep} of ${totalSteps}`;
        }

        // Update Stepper Circles
        stepperSteps.forEach((stepEl) => {
            const stepNum = parseInt(stepEl.getAttribute('data-step'), 10);
            if (stepNum < newStep) {
                stepEl.classList.add('completed');
                stepEl.classList.remove('active');
            } else if (stepNum === newStep) {
                stepEl.classList.add('active');
                stepEl.classList.remove('completed');
            } else {
                stepEl.classList.remove('active', 'completed');
            }
        });

        currentStep = newStep;

        // Smooth scroll to top of wizard
        const header = document.querySelector('.clean-card, .card');
        if (header) {
            header.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // Event Listener: Next Button
    btnNext.addEventListener('click', function () {
        if (!validateCurrentStep(currentStep)) {
            return;
        }
        if (currentStep < totalSteps) {
            updateStepView(currentStep + 1);
        }
    });

    // Event Listener: Prev Button
    btnPrev.addEventListener('click', function () {
        if (currentStep > 1) {
            updateStepView(currentStep - 1);
        }
    });

    // Allow clicking on previous steps in stepper
    stepperSteps.forEach((stepEl) => {
        stepEl.addEventListener('click', function () {
            const targetStep = parseInt(this.getAttribute('data-step'), 10);
            if (targetStep < currentStep) {
                updateStepView(targetStep);
            } else if (targetStep > currentStep) {
                // If attempting to jump forward, validate current step first
                if (validateCurrentStep(currentStep)) {
                    updateStepView(targetStep);
                }
            }
        });
    });

    // Form Submit Animation & Guard
    form.addEventListener('submit', function (e) {
        if (!validateCurrentStep(currentStep)) {
            e.preventDefault();
            return;
        }

        // Visual loading state
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Evaluating Knowledge Base Rules...
        `;
    });

    // Realtime input listener for student name
    if (studentNameInput) {
        studentNameInput.addEventListener('input', function () {
            // Allow only English letters A-Z, a-z, spaces, hyphen (-), apostrophe ('), and period (.)
            // Do not remove spaces or call trim() while the user is typing
            const sanitized = this.value.replace(/[^a-zA-Z\s\-'.]/g, '');
            if (this.value !== sanitized) {
                this.value = sanitized;
            }

            // Clear validation error when user types characters (without calling trim() on input)
            if (this.value.length > 0) {
                this.classList.remove('is-invalid');
                if (nameError) nameError.classList.add('d-none');
            }
        });
    }
});
