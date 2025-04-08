document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('startup-registration-form');
    const steps = document.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.step');
    const nextButtons = document.querySelectorAll('.btn-next');
    const prevButtons = document.querySelectorAll('.btn-prev');
    let currentStep = 0;
    
    // Create message box element
    const messageBox = document.createElement('div');
    messageBox.id = 'form-message';
    messageBox.style.display = 'none';
    form.parentNode.insertBefore(messageBox, form);
    
    // Initialize form
    function showStep(stepIndex) {
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === stepIndex);
        });
        
        progressSteps.forEach((step, index) => {
            step.classList.toggle('active', index <= stepIndex);
        });
        
        currentStep = stepIndex;
    }
    
    // Show message function
    function showMessage(type, message) {
        messageBox.innerHTML = `
            <div class="message-content ${type}">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        messageBox.style.display = 'block';
        
        // Hide after 3 seconds for success, 5 seconds for error
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, type === 'success' ? 3000 : 5000);
    }
    
    // Next button click handler
    nextButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (validateStep(currentStep)) {
                if (currentStep < steps.length - 1) {
                    showStep(currentStep + 1);
                }
            }
        });
    });
    
    // Previous button click handler
    prevButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentStep > 0) {
                showStep(currentStep - 1);
            }
        });
    });
    
    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all steps first
        let allValid = true;
        let errorMessage = '';
        
        // Clear any previous error messages
        messageBox.style.display = 'none';
        
        steps.forEach((step, index) => {
            const inputs = step.querySelectorAll('input[required], select[required], textarea[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    const fieldName = input.closest('.input-group').querySelector('label').textContent;
                    errorMessage += `• ${fieldName} is required<br>`;
                    allValid = false;
                } else if (input.type === 'number') {
                    if (input.min && parseFloat(input.value) < parseFloat(input.min)) {
                        const fieldName = input.closest('.input-group').querySelector('label').textContent;
                        errorMessage += `• ${fieldName} must be at least ${input.min}<br>`;
                        allValid = false;
                    }
                    if (input.max && parseFloat(input.value) > parseFloat(input.max)) {
                        const fieldName = input.closest('.input-group').querySelector('label').textContent;
                        errorMessage += `• ${fieldName} must be at most ${input.max}<br>`;
                        allValid = false;
                    }
                }
            });
        });
        
        if (allValid) {
            const formData = new FormData(form);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const submitBtn = document.querySelector('.btn-submit');
            
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            }
            
            // Add a timestamp to avoid caching issues
            const timestamp = new Date().getTime();
            const url = form.action + (form.action.includes('?') ? '&' : '?') + '_=' + timestamp;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => {
                // Get the content type
                const contentType = response.headers.get('content-type');
                
                // First check if it's a JSON response
                if (contentType && contentType.includes('application/json')) {
                    return response.json().then(data => {
                        // Return object with both response status and data
                        return {
                            ok: response.ok,
                            status: response.status,
                            data: data
                        };
                    });
                } else {
                    // If not JSON, get text
                    return response.text().then(text => {
                        // Try to parse as JSON anyway (sometimes content-type is wrong)
                        try {
                            const data = JSON.parse(text);
                            return {
                                ok: response.ok,
                                status: response.status,
                                data: data
                            };
                        } catch (e) {
                            // If not JSON, return as text with status
                            return {
                                ok: response.ok,
                                status: response.status,
                                text: text
                            };
                        }
                    });
                }
            })
            .then(result => {
                if (result.ok) {
                    // Request was successful
                    if (result.data && result.data.success) {
                        console.log('Form submitted successfully:', result.data);
                        showMessage('success', result.data.message || 'Submission successful!');
                        
                        if (result.data.redirect_url) {
                            setTimeout(() => {
                                window.location.href = result.data.redirect_url;
                            }, 2000);
                        }
                    } else {
                        // Even with 200 OK, success might be false
                        showMessage('success', 'Form submitted successfully!');
                        setTimeout(() => {
                            window.location.href = '/startup/dashboard/';
                        }, 2000);
                    }
                } else {
                    // Request failed
                    const errorMsg = (result.data && result.data.message) 
                        ? result.data.message 
                        : `Server error: ${result.status}`;
                    
                    console.error('Error:', errorMsg);
                    showMessage('error', errorMsg);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                showMessage('error', 'Connection error. Please try again.');
            })
            .finally(() => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Submit Application <i class="fas fa-paper-plane"></i>';
                }
            });
        } else {
            showMessage('error', `Please fix these errors:<br>${errorMessage}`);
        }
    });
    
    // Validate current step
    function validateStep(stepIndex) {
        const currentStep = steps[stepIndex];
        const inputs = currentStep.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        let errorMessage = '';
        
        inputs.forEach(input => {
            const inputGroup = input.closest('.input-group');
            
            if (!input.value.trim()) {
                inputGroup.classList.add('error');
                isValid = false;
                errorMessage += `• ${inputGroup.querySelector('label').textContent} is required<br>`;
            } else {
                inputGroup.classList.remove('error');
                
                if (input.type === 'number') {
                    if (input.min && parseFloat(input.value) < parseFloat(input.min)) {
                        inputGroup.classList.add('error');
                        isValid = false;
                        errorMessage += `• ${inputGroup.querySelector('label').textContent} must be at least ${input.min}<br>`;
                    }
                    if (input.max && parseFloat(input.value) > parseFloat(input.max)) {
                        inputGroup.classList.add('error');
                        isValid = false;
                        errorMessage += `• ${inputGroup.querySelector('label').textContent} must be at most ${input.max}<br>`;
                    }
                }
            }
        });
        
        if (!isValid) {
            showMessage('error', `Please fix these errors:<br>${errorMessage}`);
        }
        
        return isValid;
    }
    
    // Initialize first step
    showStep(0);
    
    // Add CSS for message box
    const style = document.createElement('style');
    style.textContent = `
        #form-message {
            margin-bottom: 20px;
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
        }
        .message-content {
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .message-content i {
            font-size: 20px;
        }
        .message-content.success {
            background-color: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        .message-content.error {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
    `;
    document.head.appendChild(style);
});