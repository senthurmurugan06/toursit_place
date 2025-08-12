import openai
from decouple import config
from .models import TouristPlace
import json
import re

class TouristChatbot:
    def __init__(self):
        self.api_key = config('OPENAI_API_KEY', default='')
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
    
    def get_place_context(self, place):
        """Get context information about a specific tourist place"""
        context = f"""
        Tourist Place Information:
        Name: {place.name}
        Category: {place.category}
        District: {place.district}
        Description: {place.short_description}
        """
        
        if place.detailed_description:
            context += f"Detailed Description: {place.detailed_description}\n"
        
        if place.how_to_reach:
            context += f"How to Reach: {place.how_to_reach}\n"
        
        if place.best_time_to_visit:
            context += f"Best Time to Visit: {place.best_time_to_visit}\n"
        
        if place.entry_fee:
            context += f"Entry Fee: {place.entry_fee}\n"
        
        if place.timings:
            context += f"Timings: {place.timings}\n"
        
        if place.nearby_attractions:
            context += f"Nearby Attractions: {place.nearby_attractions}\n"
        
        if place.accommodation:
            context += f"Accommodation: {place.accommodation}\n"
        
        return context
    
    def is_tourism_query(self, user_message):
        tourism_keywords = [
            
            'tourist', 'place', 'visit', 'travel', 'temple', 'beach', 'hill', 'station', 'monument', 'wildlife','hello'
            'waterfall', 'fort', 'garden', 'museum', 'accommodation', 'district', 'entry fee', 'timings',
            'attraction', 'accommodations', 'hotel', 'resort', 'stay', 'trip', 'route', 'how to reach', 'best time',
            'nearby', 'tamil nadu', 'ooty', 'kodaikanal', 'madurai', 'chennai', 'coimbatore', 'pondicherry',
            'tourism', 'guide', 'places', 'park', 'lake', 'mountain', 'festival', 'season', 'weather', 'distance',
            'map', 'directions', 'bus', 'train', 'airport', 'transport', 'food', 'cuisine', 'local', 'culture',
            'heritage', 'history', 'famous', 'popular', 'recommend', 'suggest', 'see', 'do', 'things to do', 'must see'
        ]
        user_message_lower = user_message.lower()
        return any(keyword in user_message_lower for keyword in tourism_keywords)

    def is_greeting(self, user_message):
        greetings = [
            r'^hello[.!?\\s]*$', r'^hi[.!?\\s]*$', r'^hey[.!?\\s]*$', r'^greetings[.!?\\s]*$',
            r'^good morning[.!?\\s]*$', r'^good afternoon[.!?\\s]*$', r'^good evening[.!?\\s]*$'
        ]
        user_message_lower = user_message.lower().strip()
        return any(re.match(pattern, user_message_lower) for pattern in greetings)

    def generate_response(self, user_message, place=None, chat_history=None):
        """Generate chatbot response using OpenAI API"""
        if self.is_greeting(user_message):
            return "Hello! I'm your Tourist Assistant. How can I help you with tourist places in Tamil Nadu?"
        if not self.api_key:
            return "I'm sorry, the chatbot service is not configured. Please contact the administrator."
        
        if not self.is_tourism_query(user_message):
            return "Sorry! I'm a Tourist Assistant and can't help you with that. Please ask me about tourist places in Tamil Nadu."

        try:
            # Build the system prompt
            system_prompt = """You are a helpful tourist guide for Tamil Nadu, India. You provide accurate, helpful, and friendly information about tourist places. 
            
            Your responses should be:
            - Informative and detailed
            - Friendly and welcoming
            - Focused on practical tourist information
            - Include tips for the best experience
            - Mention local customs and etiquette when relevant
            
            Always respond in a conversational tone and provide actionable advice."""
            
            # Add place-specific context if available
            if place:
                place_context = self.get_place_context(place)
                system_prompt += f"\n\nCurrent Place Context:\n{place_context}"
            
            # Build conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history if available
            if chat_history:
                # Convert QuerySet to list to support negative indexing
                chat_history_list = list(chat_history)
                for msg in chat_history_list[-5:]:  # Last 5 messages for context
                    messages.append({"role": "user", "content": msg.message})
                    messages.append({"role": "assistant", "content": msg.response})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response using new API format
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}. Please try again later."
    
    def get_general_response(self, user_message):
        """Generate response for general questions about Tamil Nadu tourism"""
        if self.is_greeting(user_message):
            return "Hello! I'm your Tourist Assistant. How can I help you with tourist places in Tamil Nadu?"
        if not self.api_key:
            return "I'm sorry, the chatbot service is not configured. Please contact the administrator."
        
        if not self.is_tourism_query(user_message):
            return "Sorry! I'm a Tourist Assistant and can't help you with that. Please ask me about tourist places in Tamil Nadu."

        try:
            system_prompt = """You are a helpful tourist guide for Tamil Nadu, India. You provide information about tourist places, travel tips, and general guidance for visitors to Tamil Nadu.
            
            Tamil Nadu is known for:
            - Ancient temples and religious sites
            - Beautiful beaches along the Coromandel Coast
            - Hill stations like Ooty and Kodaikanal
            - Rich cultural heritage and classical dance forms
            - Delicious South Indian cuisine
            - Wildlife sanctuaries and national parks
            
            Provide helpful, accurate, and friendly responses about Tamil Nadu tourism."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}. Please try again later." 