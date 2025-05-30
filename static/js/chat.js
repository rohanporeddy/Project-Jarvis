/**
 * Entertainment Chatbot - Frontend JavaScript
 * Handles chat interactions, animations, and UI updates
 */

class ChatApp {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.messageInput = document.getElementById('messageInput');
        this.chatForm = document.getElementById('chatForm');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.quickRepliesContainer = document.getElementById('quickRepliesContainer');
        this.errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
        
        this.isTyping = false;
        this.messageQueue = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.focusInput();
        
        // Auto-hide welcome quick replies after 10 seconds
        setTimeout(() => {
            const welcomeQuickReplies = document.getElementById('welcomeQuickReplies');
            if (welcomeQuickReplies) {
                welcomeQuickReplies.style.opacity = '0.7';
            }
        }, 10000);
    }

    setupEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Input events
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit();
            }
        });

        // Quick reply delegation
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-reply-btn') || 
                e.target.closest('.quick-reply-btn')) {
                const button = e.target.classList.contains('quick-reply-btn') 
                    ? e.target 
                    : e.target.closest('.quick-reply-btn');
                this.handleQuickReply(button);
            }
        });

        // Auto-resize input on mobile
        this.messageInput.addEventListener('input', () => {
            this.adjustInputHeight();
        });
    }

    adjustInputHeight() {
        // Auto-resize for long messages on mobile
        if (window.innerWidth <= 768) {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        }
    }

    async handleSubmit() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;

        // Clear input and disable form
        this.messageInput.value = '';
        this.adjustInputHeight();
        this.setFormState(false);

        // Add user message
        this.addUserMessage(message);
        
        // Hide quick replies
        this.hideQuickReplies();

        // Send to backend
        await this.sendMessage(message);
    }

    async handleQuickReply(button) {
        if (this.isTyping) return;

        const message = button.dataset.message;
        if (!message) return;

        // Add visual feedback
        button.classList.add('loading');
        
        // Hide all quick replies
        this.hideAllQuickReplies();

        // Add user message
        this.addUserMessage(message);

        // Send to backend
        await this.sendMessage(message);
    }

    async sendMessage(message) {
        try {
            this.showTyping();
            
            // Simulate realistic typing delay
            const typingDelay = Math.min(Math.max(message.length * 50, 1000), 3000);
            await this.delay(typingDelay);

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            this.hideTyping();
            this.addBotMessage(data.response, data.quick_replies || [], data.category || 'general');

        } catch (error) {
            console.error('Chat error:', error);
            this.hideTyping();
            this.showError(error.message || 'Failed to send message. Please try again.');
            this.addBotMessage(
                "Oops! Something went wrong on my end. 😅 Could you try that again?",
                ['Try again', 'Tell me a joke', 'Ask me trivia']
            );
        } finally {
            this.setFormState(true);
        }
    }

    addUserMessage(message) {
        const messageGroup = this.createMessageGroup();
        const messageElement = this.createMessage('user', message);
        messageGroup.appendChild(messageElement);
        this.chatContainer.appendChild(messageGroup);
        this.scrollToBottom();
    }

    addBotMessage(message, quickReplies = [], category = 'general') {
        const messageGroup = this.createMessageGroup();
        const messageElement = this.createMessage('bot', message, category);
        messageGroup.appendChild(messageElement);

        // Add quick replies if provided
        if (quickReplies && quickReplies.length > 0) {
            const quickRepliesElement = this.createQuickReplies(quickReplies);
            messageGroup.appendChild(quickRepliesElement);
        }

        this.chatContainer.appendChild(messageGroup);
        this.scrollToBottom();
    }

    createMessageGroup() {
        const group = document.createElement('div');
        group.className = 'message-group mb-4';
        return group;
    }

    createMessage(type, content, category = 'general') {
        const message = document.createElement('div');
        message.className = `message ${type}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        const avatarEmoji = document.createElement('span');
        avatarEmoji.className = 'avatar-emoji';
        if (type === 'bot') {
            avatarEmoji.textContent = this.getBotIcon(category);
        } else {
            avatarEmoji.textContent = '👤';
        }
        avatar.appendChild(avatarEmoji);

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        // Handle multiline content
        const lines = content.split('\n');
        lines.forEach((line, index) => {
            if (line.trim()) {
                const p = document.createElement('p');
                p.textContent = line;
                if (index === lines.length - 1) {
                    p.className = 'mb-0';
                } else {
                    p.className = 'mb-2';
                }
                bubble.appendChild(p);
            }
        });

        const time = document.createElement('small');
        time.className = 'message-time text-muted';
        time.textContent = this.formatTime(new Date());

        messageContent.appendChild(bubble);
        messageContent.appendChild(time);

        message.appendChild(avatar);
        message.appendChild(messageContent);

        // Initialize icons after DOM insertion
        setTimeout(() => {
            feather.replace();
        }, 50);

        return message;
    }

    createQuickReplies(replies) {
        const container = document.createElement('div');
        container.className = 'quick-replies mt-2';

        replies.forEach(reply => {
            const button = document.createElement('button');
            button.className = 'btn btn-outline-primary btn-sm quick-reply-btn';
            button.dataset.message = reply;
            
            // Add appropriate emoji based on reply content
            const emoji = document.createElement('span');
            emoji.className = 'btn-emoji';
            emoji.textContent = this.getQuickReplyIcon(reply);
            
            button.appendChild(emoji);
            button.appendChild(document.createTextNode(' ' + reply));
            
            container.appendChild(button);
        });

        // Initialize icons
        setTimeout(() => {
            feather.replace();
        }, 50);

        return container;
    }

    getBotIcon(category) {
        const emojiMap = {
            'joke': '😂',
            'trivia': '🧠',
            'riddle': '🧩',
            'story': '📚',
            'greeting': '👋',
            'compliments': '❤️',
            'personal_questions': '🤖',
            'default': '😄'
        };
        return emojiMap[category] || '😄';
    }

    getQuickReplyIcon(reply) {
        const text = reply.toLowerCase();
        if (text.includes('joke') || text.includes('funny')) return '😂';
        if (text.includes('trivia') || text.includes('question')) return '🧠';
        if (text.includes('riddle') || text.includes('puzzle')) return '🧩';
        if (text.includes('story') || text.includes('tale')) return '📚';
        if (text.includes('hint')) return '💡';
        if (text.includes('again') || text.includes('another')) return '🔄';
        if (text.includes('give up')) return '🏳️';
        return '✨';
    }

    showTyping() {
        this.isTyping = true;
        this.typingIndicator.classList.remove('d-none');
        this.scrollToBottom();
    }

    hideTyping() {
        this.isTyping = false;
        this.typingIndicator.classList.add('d-none');
    }

    hideQuickReplies() {
        this.quickRepliesContainer.classList.add('d-none');
    }

    hideAllQuickReplies() {
        // Hide all quick reply containers
        const allQuickReplies = document.querySelectorAll('.quick-replies');
        allQuickReplies.forEach(container => {
            container.style.opacity = '0.5';
            container.style.pointerEvents = 'none';
        });
    }

    setFormState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.sendButton.classList.remove('loading');
            this.focusInput();
        } else {
            this.sendButton.classList.add('loading');
        }
    }

    focusInput() {
        // Focus input with slight delay to ensure proper behavior
        setTimeout(() => {
            if (!this.messageInput.disabled) {
                this.messageInput.focus();
            }
        }, 100);
    }

    scrollToBottom() {
        // Smooth scroll to bottom with slight delay for animation
        setTimeout(() => {
            this.chatContainer.scrollTo({
                top: this.chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }

    showError(message) {
        const errorBody = document.getElementById('errorToastBody');
        errorBody.textContent = message;
        this.errorToast.show();
    }

    formatTime(date) {
        return date.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the chat app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});

// Handle page visibility for better UX
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        const chatApp = window.chatApp;
        if (chatApp && !chatApp.isTyping) {
            chatApp.focusInput();
        }
    }
});

// Handle window resize for responsive behavior
window.addEventListener('resize', () => {
    const chatContainer = document.getElementById('chatContainer');
    if (chatContainer) {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }
});
