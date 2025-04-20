document.addEventListener('DOMContentLoaded', function() {
    // Form submission for adding a profit entry
    const addProfitForm = document.getElementById('add-profit-form');
    if (addProfitForm) {
        addProfitForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const dateInput = document.getElementById('profit-date');
            const amountInput = document.getElementById('profit-amount');
            
            // Simple validation
            if (!dateInput.value || !amountInput.value) {
                showAlert('Please fill in all fields', 'danger');
                return;
            }
            
            if (parseFloat(amountInput.value) < 0) {
                showAlert('Profit amount cannot be negative', 'danger');
                return;
            }
            
            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Prepare data
            const data = {
                date: dateInput.value,
                amount: amountInput.value
            };
            
            // Send AJAX request
            fetch('/startup/add_profit_entry/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Add the new entry to the table
                    addProfitEntryToTable(data.profit_id, data.date, data.amount);
                    
                    // Clear the form
                    addProfitForm.reset();
                    
                    // Update chart
                    updateProfitChart();
                    
                    showAlert('Profit entry added successfully', 'success');
                } else {
                    showAlert(data.error || 'Failed to add profit entry', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred while adding the profit entry', 'danger');
            });
        });
    }
    
    // Delete profit entry
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('delete-profit-btn')) {
            e.preventDefault();
            
            if (!confirm('Are you sure you want to delete this profit entry?')) {
                return;
            }
            
            const profitId = e.target.getAttribute('data-profit-id');
            const rowElement = document.getElementById(`profit-row-${profitId}`);
            
            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Send delete request
            fetch('/startup/delete_profit_entry/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    profit_id: profitId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove the entry from the table
                    if (rowElement) {
                        rowElement.remove();
                    }
                    
                    // Update chart
                    updateProfitChart();
                    
                    showAlert('Profit entry deleted successfully', 'success');
                } else {
                    showAlert(data.error || 'Failed to delete profit entry', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred while deleting the profit entry', 'danger');
            });
        }
    });
    
    // Helper function to add a profit entry to the table
    function addProfitEntryToTable(id, dateStr, amount) {
        const table = document.getElementById('profit-entries-table');
        const tbody = table.querySelector('tbody');
        
        if (!tbody) return;
        
        // Format the date for display
        const date = new Date(dateStr);
        const formattedDate = date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long'
        });
        
        // Format the amount
        const formattedAmount = parseFloat(amount).toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD'
        });
        
        // Create new row
        const newRow = document.createElement('tr');
        newRow.id = `profit-row-${id}`;
        newRow.innerHTML = `
            <td>${formattedDate}</td>
            <td>${formattedAmount}</td>
            <td>
                <button class="btn btn-sm btn-danger delete-profit-btn" data-profit-id="${id}">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        `;
        
        // Add to table
        tbody.appendChild(newRow);
        
        // If table was hidden, show it
        if (table.classList.contains('d-none')) {
            table.classList.remove('d-none');
            document.getElementById('no-profits-message')?.classList.add('d-none');
        }
    }
    
    // Helper function to show alerts
    function showAlert(message, type) {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        alertContainer.appendChild(alert);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    }
    
    // Initialize chart
    const ctx = document.getElementById('profit-chart').getContext('2d');
    let profitChart;
    
    // If profitData is available from the template
    if (typeof profitData !== 'undefined' && profitData.labels.length > 0) {
        profitChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: profitData.labels,
                datasets: [{
                    label: 'Monthly Profit',
                    data: profitData.values,
                    backgroundColor: 'rgba(108, 99, 255, 0.2)',
                    borderColor: 'rgba(108, 99, 255, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.y.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Function to update profit chart data
    function updateProfitChart() {
        // Fetch updated data via AJAX
        fetch('/startup/profit_data/')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const labels = data.profit_data.map(item => item.date);
                    const values = data.profit_data.map(item => item.amount);
                    
                    if (profitChart) {
                        profitChart.data.labels = labels;
                        profitChart.data.datasets[0].data = values;
                        profitChart.update();
                    } else {
                        // Create new chart if none exists
                        profitChart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: 'Monthly Profit',
                                    data: values,
                                    backgroundColor: 'rgba(108, 99, 255, 0.2)',
                                    borderColor: 'rgba(108, 99, 255, 1)',
                                    borderWidth: 2,
                                    tension: 0.3,
                                    fill: true
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        ticks: {
                                            callback: function(value) {
                                                return '$' + value.toLocaleString();
                                            }
                                        }
                                    }
                                },
                                plugins: {
                                    tooltip: {
                                        callbacks: {
                                            label: function(context) {
                                                return '$' + context.parsed.y.toLocaleString();
                                            }
                                        }
                                    }
                                }
                            }
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Error updating chart:', error);
            });
    }
}); 