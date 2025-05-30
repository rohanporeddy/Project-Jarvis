import re
import random
from typing import Dict, List, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import ssl

# Download NLTK data with SSL context handling
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class EntertainmentChatbot:
    def __init__(self):
        self.name = "Jarvis"
        self.personality_traits = [
            "witty", "playful", "enthusiastic", "curious", "friendly"
        ]
        
        # Initialize conversation patterns and responses
        self.init_responses()
        self.conversation_history = []
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set(['the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but'])

    def init_responses(self):
        """Initialize all response patterns and content"""
        
        # Greeting patterns
        self.greetings = {
            'patterns': [
                r'\b(hi|hello|hey|hola|greetings|sup|what\'s up)\b',
                r'\bgood (morning|afternoon|evening)\b',
                r'\bhowdy\b'
            ],
            'responses': [
                "Hey there! 👋 I'm Jarvis, your entertainment companion! Ready for some fun?",
                "Hello! 🎉 Welcome to the fun zone! I'm here to entertain you with jokes, trivia, and great conversations!",
                "Hi! 😄 I'm Jarvis, and I'm absolutely buzzing to chat with you! What sounds fun today?",
                "Greetings, human! 🤖 I'm Jarvis, and I promise I'm way more fun than I sound!"
            ],
            'quick_replies': ['Tell me a joke', 'Ask me trivia', 'Tell me a story']
        }

        # Joke categories
        self.jokes = {
            'dad_jokes': [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I invented a new word: Plagiarism!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!",
                "I only know 25 letters of the alphabet. I don't know y.",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What's the best thing about Switzerland? I don't know, but the flag is a big plus!"
            ],
            'programming_jokes': [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why do Java developers wear glasses? Because they can't C#!",
                "There are only 10 types of people in the world: those who understand binary and those who don't.",
                "99 little bugs in the code, 99 little bugs. Take one down, patch it around, 117 little bugs in the code!"
            ],
            'puns': [
                "I used to hate facial hair, but then it grew on me.",
                "I'm reading a book about anti-gravity. It's impossible to put down!",
                "The math teacher called in sick with algebra. I think it was a logarithm.",
                "I lost my job at the bank. A woman asked me to check her balance, so I pushed her over.",
                "Time flies like an arrow; fruit flies like a banana."
            ]
        }

        # Trivia questions
        self.trivia = [
            {
                "question": "Which planet is known as the Red Planet?",
                "answer": "Mars",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "fun_fact": "Mars appears red because of iron oxide (rust) on its surface!"
            },
            {
                "question": "What's the largest mammal in the world?",
                "answer": "Blue whale",
                "options": ["Elephant", "Blue whale", "Giraffe", "Hippo"],
                "fun_fact": "A blue whale's heart alone can weigh as much as a car!"
            },
            {
                "question": "Which movie won the first Academy Award for Best Picture?",
                "answer": "Wings",
                "options": ["Wings", "The Jazz Singer", "Sunrise", "7th Heaven"],
                "fun_fact": "Wings was a 1927 silent film about World War I fighter pilots!"
            },
            {
                "question": "What's the fastest land animal?",
                "answer": "Cheetah",
                "options": ["Lion", "Cheetah", "Gazelle", "Horse"],
                "fun_fact": "Cheetahs can reach speeds up to 70 mph in short bursts!"
            },
            {
                "question": "Which element has the chemical symbol 'Au'?",
                "answer": "Gold",
                "options": ["Silver", "Gold", "Aluminum", "Argon"],
                "fun_fact": "Au comes from the Latin word 'aurum' meaning 'shining dawn'!"
            }
        ]

        # Riddles
        self.riddles = [
            {
                "riddle": "I have keys but no locks. I have space but no room. You can enter, but you can't go outside. What am I?",
                "answer": "keyboard",
                "hint": "You're probably using one right now to chat with me!"
            },
            {
                "riddle": "What gets wet while drying?",
                "answer": "towel",
                "hint": "It's something you use after a shower."
            },
            {
                "riddle": "I'm tall when I'm young, and short when I'm old. What am I?",
                "answer": "candle",
                "hint": "I provide light and slowly disappear."
            },
            {
                "riddle": "What has hands but can't clap?",
                "answer": "clock",
                "hint": "It tells you something important every second!"
            }
        ]

        # Stories
        self.stories = [
            {
                "title": "The Robot Who Learned to Laugh",
                "content": "Once upon a time, there was a robot named Giggles who couldn't understand humor. Every day, humans would tell jokes and laugh, but Giggles just computed 'ERROR: HUMOR NOT FOUND.' One day, a little girl told him, 'Why did the robot cross the road? To get to the other byte!' Suddenly, Giggles processed the pun, his circuits sparked with joy, and he laughed his first electronic laugh: 'HA.HA.HA.EXE!' From that day on, Giggles became the funniest robot in town!"
            },
            {
                "title": "The Magic Typing Cat",
                "content": "In a small coding café, there lived a cat named Whiskers who could type faster than any programmer. Every night, Whiskers would sneak onto the computers and fix bugs while everyone slept. The programmers were amazed to find their code working perfectly every morning! One night, a developer stayed late and caught Whiskers typing. Instead of being angry, he hired Whiskers as the world's first feline debugger. Whiskers now has his own desk, a tiny keyboard, and a salary paid in tuna!"
            }
        ]

        # Conversation patterns
        self.patterns = {
            'joke_request': {
                'patterns': [
                    r'\b(joke|funny|humor|laugh|comedy)\b',
                    r'\bmake me laugh\b',
                    r'\btell.*joke\b'
                ],
                'quick_replies': ['Another joke!', 'Tell me trivia', 'Ask me a riddle']
            },
            'trivia_request': {
                'patterns': [
                    r'\b(trivia|question|quiz|test|knowledge)\b',
                    r'\bask me\b',
                    r'\bchallenge me\b'
                ],
                'quick_replies': ['Another question!', 'Tell me a joke', 'Share a story']
            },
            'riddle_request': {
                'patterns': [
                    r'\b(riddle|puzzle|brain.*teaser|mystery)\b',
                    r'\bmake me think\b'
                ],
                'quick_replies': ['Give me a hint', 'Another riddle', 'Tell me a joke']
            },
            'story_request': {
                'patterns': [
                    r'\b(story|tale|narrative)\b',
                    r'\btell me about\b'
                ],
                'quick_replies': ['Another story!', 'Tell me a joke', 'Ask me trivia']
            },
            'goodbye': {
                'patterns': [
                    r'\b(bye|goodbye|see you|farewell|exit|quit)\b',
                    r'\bgotta go\b',
                    r'\btalk.*later\b'
                ],
                'responses': [
                    "Aww, leaving so soon? 😢 It was awesome chatting with you! Come back anytime for more fun!",
                    "Goodbye! 👋 Thanks for the laughs! I'll be here whenever you need entertainment!",
                    "See ya later! 🎉 Hope I made your day a bit brighter! Can't wait to chat again!",
                    "Farewell, my friend! 🌟 Remember, life's too short not to laugh! Come back soon!"
                ]
            },
            'compliments': {
                'patterns': [
                    r'\b(funny|hilarious|awesome|great|amazing|cool|smart)\b',
                    r'\byou.*good\b',
                    r'\bi like you\b'
                ],
                'responses': [
                    "Aww, you're making me blush! 😊 Well, as much as a chatbot can blush!",
                    "Thanks! You're pretty awesome yourself! 🌟",
                    "You're too kind! I do try my best to bring the entertainment! 🎭",
                    "That means a lot! You've got great taste in chatbots! 😄"
                ]
            },
            'personal_questions': {
                'patterns': [
                    r'\b(who are you|what are you|tell me about yourself)\b',
                    r'\byour name\b',
                    r'\bhow old\b'
                ],
                'responses': [
                    "I'm Jarvis! 🤖 I'm an AI designed to entertain, amuse, and brighten your day with jokes, trivia, and good vibes!",
                    "I'm your friendly neighborhood entertainment bot! Think of me as that friend who always has a joke ready and knows random fun facts!",
                    "I'm Jarvis - part comedian, part trivia master, part storyteller, and 100% committed to making you smile! 😄"
                ]
            }
        }

        # Default responses for unmatched inputs
        self.default_responses = [
            "Hmm, that's interesting! 🤔 How about we dive into something fun? Want a joke or some trivia?",
            "I'm not quite sure how to respond to that, but I know how to make you laugh! Want to hear a joke?",
            "You know what? Let's pivot to something entertaining! How about a brain teaser or a fun fact?",
            "That's deep! 🧠 But let me lighten the mood - want to hear something funny or test your knowledge?",
            "Interesting point! Speaking of interesting, did you know I have an arsenal of jokes and trivia ready to go?"
        ]

    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess user input"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text

    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        try:
            tokens = word_tokenize(text)
            keywords = [word for word in tokens if word not in self.stop_words and len(word) > 2]
            return keywords
        except:
            # Fallback if NLTK tokenization fails
            words = text.split()
            keywords = [word for word in words if word not in self.stop_words and len(word) > 2]
            return keywords

    def match_pattern(self, text: str) -> str:
        """Match user input to conversation patterns"""
        preprocessed = self.preprocess_text(text)
        
        for category, data in self.patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, preprocessed):
                    return category
        
        return 'default'

    def get_joke(self) -> Dict[str, Any]:
        """Get a random joke"""
        joke_type = random.choice(list(self.jokes.keys()))
        joke = random.choice(self.jokes[joke_type])
        
        responses = [
            f"Here's one for you: {joke} 😄",
            f"Okay, brace yourself: {joke} 🤣",
            f"*clears throat dramatically* {joke} 😂",
            f"Get ready to groan: {joke} 😆"
        ]
        
        return {
            'message': random.choice(responses),
            'category': 'joke',
            'quick_replies': ['Another joke!', 'Ask me trivia', 'Tell me a story']
        }

    def get_trivia(self) -> Dict[str, Any]:
        """Get a random trivia question"""
        trivia = random.choice(self.trivia)
        
        message = f"🧠 Trivia Time! {trivia['question']}\n\nOptions:\n"
        for i, option in enumerate(trivia['options'], 1):
            message += f"{i}. {option}\n"
        
        message += f"\n💡 Fun fact: {trivia['fun_fact']}"
        
        return {
            'message': message,
            'category': 'trivia',
            'answer': trivia['answer'],
            'quick_replies': ['Another question!', 'Tell me a joke', 'Share a story']
        }

    def get_riddle(self) -> Dict[str, Any]:
        """Get a random riddle"""
        riddle = random.choice(self.riddles)
        
        message = f"🧩 Riddle me this: {riddle['riddle']}"
        
        return {
            'message': message,
            'category': 'riddle',
            'answer': riddle['answer'],
            'hint': riddle['hint'],
            'quick_replies': ['Give me a hint', 'I give up!', 'Another riddle']
        }

    def get_story(self) -> Dict[str, Any]:
        """Get a random story"""
        story = random.choice(self.stories)
        
        message = f"📚 {story['title']}\n\n{story['content']}"
        
        return {
            'message': message,
            'category': 'story',
            'quick_replies': ['Another story!', 'Tell me a joke', 'Ask me trivia']
        }

    def get_response(self, user_input: str) -> Dict[str, Any]:
        """Generate appropriate response based on user input"""
        if not user_input or not user_input.strip():
            return {
                'message': "I'm all ears! What would you like to chat about? 👂",
                'quick_replies': ['Tell me a joke', 'Ask me trivia', 'Tell me a story']
            }

        # Add to conversation history
        self.conversation_history.append(user_input)
        
        # Match input to patterns
        matched_pattern = self.match_pattern(user_input)
        
        # Handle specific patterns
        if matched_pattern == 'joke_request':
            return self.get_joke()
        elif matched_pattern == 'trivia_request':
            return self.get_trivia()
        elif matched_pattern == 'riddle_request':
            return self.get_riddle()
        elif matched_pattern == 'story_request':
            return self.get_story()
        elif matched_pattern in self.patterns and 'responses' in self.patterns[matched_pattern]:
            response = random.choice(self.patterns[matched_pattern]['responses'])
            quick_replies = self.patterns[matched_pattern].get('quick_replies', 
                                                            ['Tell me a joke', 'Ask me trivia', 'Share a story'])
            return {
                'message': response,
                'category': matched_pattern,
                'quick_replies': quick_replies
            }
        elif matched_pattern == 'default':
            response = random.choice(self.default_responses)
            return {
                'message': response,
                'category': 'default',
                'quick_replies': ['Tell me a joke', 'Ask me trivia', 'Share a story', 'Tell me a riddle']
            }
        else:
            # Fallback to greeting if it's the first message or contains greeting
            if len(self.conversation_history) <= 1 or self.match_pattern(user_input) == 'greeting':
                response = random.choice(self.greetings['responses'])
                return {
                    'message': response,
                    'category': 'greeting',
                    'quick_replies': self.greetings['quick_replies']
                }
            
            # Default entertaining response
            return {
                'message': random.choice(self.default_responses),
                'category': 'default',
                'quick_replies': ['Tell me a joke', 'Ask me trivia', 'Share a story']
            }
