/**
 * Disaster Relief Chatbot - Frontend Script
 * Optimized for performance and user experience
 */
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const messageForm = document.getElementById('message-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const clearChatBtn = document.getElementById('clear-chat');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // State variables
    let isWaitingForResponse = false;
    let messageHistory = [];
    
    // Initialize the chat
    initChat();
    
    /**
     * Initialize the chat interface and event listeners
     */
    function initChat() {
        // Load chat history from localStorage if available
        loadChatHistory();
        
        // Set up event listeners
        messageForm.addEventListener('submit', handleMessageSubmit);
        userInput.addEventListener('keydown', handleInputKeydown);
        clearChatBtn.addEventListener('click', clearChat);
        
        // Set up tab functionality
        tabButtons.forEach(button => {
            button.addEventListener('click', () => switchTab(button.dataset.tab));
        });
        
        // Focus on input field
        userInput.focus();
    }
    
    /**
     * Handle form submission with debounce
     * @param {Event} e - Form submit event
     */
    function handleMessageSubmit(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message || isWaitingForResponse) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator and send message to server
        sendMessage(message);
    }
    
    /**
     * Handle keydown events in the input field
     * @param {KeyboardEvent} e - Keydown event
     */
    function handleInputKeydown(e) {
        // If Enter is pressed without Shift, submit the form
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            messageForm.dispatchEvent(new Event('submit'));
        }
    }
    
    /**
     * Send message to server and handle response
     * @param {string} message - User message to send
     */
    async function sendMessage(message) {
        isWaitingForResponse = true;
        
        // Show typing indicator
        const typingIndicator = showTypingIndicator();
        
        try {
            // Send message to server
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator(typingIndicator);
            
            // Add bot response to chat
            addMessage(data.response, 'bot', data.intent);
            
            // Save chat history
            saveChatHistory();
            
        } catch (error) {
            console.error('Error:', error);
            
            // Remove typing indicator
            removeTypingIndicator(typingIndicator);
            
            // Add error message
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } finally {
            isWaitingForResponse = false;
            userInput.focus();
        }
    }
    
    /**
     * Add a message to the chat
     * @param {string} message - Message text
     * @param {string} sender - Message sender ('user' or 'bot')
     * @param {string} intent - Message intent for styling (optional)
     */
    function addMessage(message, sender, intent = null) {
        // Create message element
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        
        // Create message content
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // Add intent-specific styling if available
        if (intent && sender === 'bot') {
            messageContent.classList.add(intent.replace('_', '-'));
        }
        
        // Create message text
        const messageText = document.createElement('p');
        messageText.textContent = message;
        messageContent.appendChild(messageText);
        
        // Create message timestamp
        const messageTime = document.createElement('div');
        messageTime.classList.add('message-time');
        messageTime.textContent = getCurrentTime();
        
        // Assemble message
        messageElement.appendChild(messageContent);
        messageElement.appendChild(messageTime);
        
        // Add to chat
        chatMessages.appendChild(messageElement);
        
        // Scroll to the bottom of the chat
        scrollToBottom();
        
        // Add to message history
        messageHistory.push({
            message,
            sender,
            intent,
            time: new Date().toISOString()
        });
    }
    
    /**
     * Show typing indicator in the chat
     * @returns {HTMLElement} - The typing indicator element
     */
    function showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.classList.add('message', 'bot-message', 'typing-indicator');
        
        const typingContent = document.createElement('div');
        typingContent.classList.add('message-content');
        
        const dots = document.createElement('div');
        dots.classList.add('typing-dots');
        dots.innerHTML = '<span></span><span></span><span></span>';
        
        typingContent.appendChild(dots);
        typingElement.appendChild(typingContent);
        
        chatMessages.appendChild(typingElement);
        scrollToBottom();
        
        return typingElement;
    }
    
    /**
     * Remove typing indicator from the chat
     * @param {HTMLElement} element - The typing indicator element to remove
     */
    function removeTypingIndicator(element) {
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }
    
    /**
     * Get current time in HH:MM format with AM/PM
     * @returns {string} - Formatted time string
     */
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    }
    
    /**
     * Scroll to the bottom of the chat messages
     */
    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }
    
    /**
     * Clear the chat history
     */
    function clearChat() {
        // Confirm before clearing
        if (messageHistory.length <= 1 || confirm('Are you sure you want to clear the chat history?')) {
            // Keep only the first welcome message
            while (chatMessages.children.length > 1) {
                chatMessages.removeChild(chatMessages.lastChild);
            }
            
            // Reset message history to just the welcome message
            messageHistory = messageHistory.slice(0, 1);
            
            // Clear local storage
            localStorage.removeItem('chatHistory');
        }
    }
    
    /**
     * Save chat history to localStorage
     */
    function saveChatHistory() {
        try {
            localStorage.setItem('chatHistory', JSON.stringify(messageHistory));
        } catch (error) {
            console.error('Error saving chat history:', error);
        }
    }
    
    /**
     * Load chat history from localStorage
     */
    function loadChatHistory() {
        try {
            const savedHistory = localStorage.getItem('chatHistory');
            
            if (savedHistory) {
                messageHistory = JSON.parse(savedHistory);
                
                // Clear existing messages except the first one
                while (chatMessages.children.length > 1) {
                    chatMessages.removeChild(chatMessages.lastChild);
                }
                
                // Add messages from history (skip the first welcome message)
                messageHistory.slice(1).forEach(item => {
                    addMessage(item.message, item.sender, item.intent);
                });
            } else {
                // Initialize with just the welcome message
                messageHistory = [{
                    message: "Hello! I'm the Disaster Relief Assistant. How can I help you today?",
                    sender: 'bot',
                    time: new Date().toISOString()
                }];
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
    
    /**
     * Switch between tabs in the Do's and Don'ts section
     * @param {string} tabId - ID of the tab to switch to
     */
    function switchTab(tabId) {
        // Update tab buttons
        tabButtons.forEach(button => {
            if (button.dataset.tab === tabId) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
        
        // Update tab contents
        tabContents.forEach(content => {
            if (content.id === `${tabId}-content`) {
                content.classList.add('active');
            } else {
                content.classList.remove('active');
            }
        });
    }
});