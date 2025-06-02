document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const taskForm = document.getElementById('task-form');
    const taskHistoryContainer = document.getElementById('task-history');
    const browserContent = document.getElementById('browser-content');
    const urlBar = document.getElementById('url-bar');
    const goButton = document.getElementById('go-button');
    const taskTypeSelect = document.getElementById('task-type');
    const taskParamsContainer = document.getElementById('task-params-container');
    
    // Task type parameters templates
    const taskParamsTemplates = {
        'google_search': `
            <div class="form-group">
                <label for="search-query">Search Query</label>
                <input type="text" id="search-query" name="search_query" required>
            </div>
        `,
        'purchase_watch': `
            <div class="form-group">
                <label for="watch-type">Watch Type</label>
                <select id="watch-type" name="watch_type" required>
                    <option value="">Select a watch type</option>
                    <option value="smart_watch">Smart Watch</option>
                    <option value="luxury_watch">Luxury Watch</option>
                    <option value="sports_watch">Sports Watch</option>
                </select>
            </div>
            <div class="form-group">
                <label for="price-range">Price Range</label>
                <select id="price-range" name="price_range" required>
                    <option value="">Select price range</option>
                    <option value="budget">Budget (Under $100)</option>
                    <option value="mid_range">Mid-range ($100-$500)</option>
                    <option value="premium">Premium (Over $500)</option>
                </select>
            </div>
        `,
        'custom_task': `
            <div class="form-group">
                <label for="task-description">Task Description</label>
                <textarea id="task-description" name="task_description" rows="4" required></textarea>
            </div>
            <div class="form-group">
                <label for="target-website">Target Website</label>
                <input type="url" id="target-website" name="target_website" required>
            </div>
        `
    };
    
    // Update task parameters based on selected task type
    taskTypeSelect.addEventListener('change', function() {
        const selectedTaskType = this.value;
        taskParamsContainer.innerHTML = taskParamsTemplates[selectedTaskType] || '';
    });
    
    // Handle URL navigation
    goButton.addEventListener('click', function() {
        navigateToUrl(urlBar.value);
    });
    
    urlBar.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            navigateToUrl(urlBar.value);
        }
    });
    
    // Handle task form submission
    taskForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(taskForm);
        const taskData = {
            task_type: formData.get('task_type'),
            params: {}
        };
        
        // Collect task parameters based on task type
        if (taskData.task_type === 'google_search') {
            taskData.params.search_query = formData.get('search_query');
        } else if (taskData.task_type === 'purchase_watch') {
            taskData.params.watch_type = formData.get('watch_type');
            taskData.params.price_range = formData.get('price_range');
        } else if (taskData.task_type === 'custom_task') {
            taskData.params.task_description = formData.get('task_description');
            taskData.params.target_website = formData.get('target_website');
        }
        
        // Submit task to backend
        submitTask(taskData);
    });
    
    // Function to navigate to URL
    function navigateToUrl(url) {
        // Ensure URL has protocol
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }
        
        // Update URL bar
        urlBar.value = url;
        
        // In a real implementation, this would load the URL in an iframe or browser automation
        // For demo purposes, we'll just show a message
        browserContent.innerHTML = `<div style="padding: 20px; text-align: center;">
            <h2>Simulated Browser</h2>
            <p>Navigating to: ${url}</p>
            <p>In a real implementation, this would show the actual website or browser automation.</p>
        </div>`;
        
        // You could also make an AJAX request to your backend to start a browser session
        fetch('/browser/navigate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Navigation response:', data);
            // Handle response if needed
        })
        .catch(error => {
            console.error('Error navigating:', error);
        });
    }
    
    // Function to submit task
    function submitTask(taskData) {
        // Add task to history with 'running' status
        const taskId = 'task-' + Date.now();
        addTaskToHistory(taskId, taskData, 'running');
        
        // Make API request to backend
        fetch('/browser/task/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(taskData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Task submission response:', data);
            // Update task status in history
            updateTaskStatus(taskId, data.status || 'completed', data.result || 'Task completed');
            
            // If the task involves navigation, update the browser content
            if (data.url) {
                urlBar.value = data.url;
                // In a real implementation, this would show the actual website
                browserContent.innerHTML = `<div style="padding: 20px; text-align: center;">
                    <h2>Task Result</h2>
                    <p>Navigated to: ${data.url}</p>
                    <p>${data.result || 'Task completed successfully'}</p>
                </div>`;
            }
        })
        .catch(error => {
            console.error('Error submitting task:', error);
            updateTaskStatus(taskId, 'failed', 'Error: ' + error.message);
        });
    }
    
    // Function to add task to history
    function addTaskToHistory(taskId, taskData, status) {
        const taskElement = document.createElement('div');
        taskElement.id = taskId;
        taskElement.className = 'task-item';
        
        let taskTitle = 'Unknown Task';
        if (taskData.task_type === 'google_search') {
            taskTitle = `Google Search: "${taskData.params.search_query}"`;
        } else if (taskData.task_type === 'purchase_watch') {
            taskTitle = `Purchase ${taskData.params.watch_type.replace('_', ' ')} (${taskData.params.price_range.replace('_', ' ')})`;
        } else if (taskData.task_type === 'custom_task') {
            taskTitle = `Custom Task: ${taskData.params.task_description.substring(0, 30)}...`;
        }
        
        taskElement.innerHTML = `
            <h3>${taskTitle}</h3>
            <p>Started: ${new Date().toLocaleTimeString()}</p>
            <p>Status: <span class="task-status status-${status}">${status}</span></p>
            <div class="task-result"></div>
        `;
        
        // Add to history container (at the beginning)
        if (taskHistoryContainer.firstChild) {
            taskHistoryContainer.insertBefore(taskElement, taskHistoryContainer.firstChild);
        } else {
            taskHistoryContainer.appendChild(taskElement);
        }
    }
    
    // Function to update task status
    function updateTaskStatus(taskId, status, result) {
        const taskElement = document.getElementById(taskId);
        if (taskElement) {
            const statusElement = taskElement.querySelector('.task-status');
            statusElement.className = `task-status status-${status}`;
            statusElement.textContent = status;
            
            const resultElement = taskElement.querySelector('.task-result');
            resultElement.innerHTML = `<p>${result}</p>`;
            
            if (status === 'completed' || status === 'failed') {
                taskElement.innerHTML += `<p>Completed: ${new Date().toLocaleTimeString()}</p>`;
            }
        }
    }
    
    // Function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    // Initialize with Google Search task type selected
    taskTypeSelect.value = 'google_search';
    taskTypeSelect.dispatchEvent(new Event('change'));
});