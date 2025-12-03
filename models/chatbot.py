"""
Chatbot Model - Rule-based intelligent responses
"""

import re
from datetime import datetime

class Chatbot:
    """Rule-based chatbot for Medilink Hospital"""
    
    @staticmethod
    def get_response(message, user_context=None):
        """
        Get chatbot response based on message and user context
        
        Args:
            message: User's message
            user_context: Dict with user_type, user_id, user_name
        
        Returns:
            String response
        """
        message_lower = message.lower().strip()
        
        # Greeting patterns
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            if user_context and user_context.get('user_name'):
                return f"Hello {user_context['user_name']}! How can I help you today?"
            return "Hello! Welcome to Medilink Hospital. How can I assist you today?"
        
        # Appointment booking
        if any(word in message_lower for word in ['book', 'appointment', 'schedule', 'doctor']):
            if user_context and user_context.get('user_type') == 'patient':
                return "To book an appointment, click on 'Book Appointment' in your dashboard or <a href='/patient/book-appointment'>click here</a>. You can choose your preferred doctor, date, and time!"
            return "To book an appointment, please <a href='/patient/login'>login as a patient</a> or <a href='/patient/register'>register here</a>."
        
        # Finding doctors
        if any(word in message_lower for word in ['find doctor', 'doctors', 'specialist', 'cardiologist', 'surgeon']):
            return "You can view all our doctors and their specializations on the <a href='/patient/book-appointment'>Book Appointment</a> page. We have specialists in various fields including Cardiology, Neurology, Orthopedics, and more!"
        
        # Cancel appointment
        if any(word in message_lower for word in ['cancel', 'cancellation']):
            if user_context and user_context.get('user_type') == 'patient':
                return "To cancel an appointment, go to <a href='/patient/appointments'>My Appointments</a> and click the 'Cancel Appointment' button next to your scheduled appointment."
            return "Please login to manage your appointments."
        
        # Medical records
        if any(word in message_lower for word in ['medical record', 'history', 'prescription', 'diagnosis']):
            if user_context and user_context.get('user_type') == 'patient':
                return "You can view your complete medical history at <a href='/patient/medical-records'>My Medical Records</a>. This includes all diagnoses, prescriptions, and doctor's notes."
            return "Medical records are available after you login as a patient."
        
        # Password reset
        if any(word in message_lower for word in ['forgot password', 'reset password', 'password']):
            return "You can reset your password by clicking 'Forgot Password?' on the login page, or <a href='/forgot-password'>click here</a> to reset it now."
        
        # Hospital hours
        if any(word in message_lower for word in ['hours', 'open', 'timing', 'time']):
            return "Medilink Hospital is open 24/7 for emergencies. Regular OPD hours are 9:00 AM to 8:00 PM, Monday to Saturday. Emergency services are available round the clock!"
        
        # Contact information
        if any(word in message_lower for word in ['contact', 'phone', 'email', 'address', 'location']):
            return "Phone: +880-XXX-XXXXXX<br>Email: info@medilink.com<br>Address: Dhaka, Bangladesh<br>For emergencies, call our 24/7 helpline!"
        
        # Help/Features
        if any(word in message_lower for word in ['help', 'what can you do', 'features', 'how']):
            return """I can help you with:
            <ul>
                <li>Booking appointments</li>
                <li>Finding doctors</li>
                <li>Viewing medical records</li>
                <li>Cancelling appointments</li>
                <li>Resetting passwords</li>
                <li>Hospital information</li>
            </ul>
            Just ask me anything!"""
        
        # Thank you
        if any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome! Is there anything else I can help you with?"
        
        # Goodbye
        if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'exit']):
            return "Goodbye! Take care and stay healthy! Feel free to chat anytime you need help."
        
        # Default response
        return """I'm here to help! You can ask me about:
        <ul>
            <li>Booking appointments</li>
            <li>Finding doctors</li>
            <li>Medical records</li>
            <li>Hospital hours and contact info</li>
        </ul>
        What would you like to know?"""
    
    @staticmethod
    def save_message(mysql, user_id, user_type, message, response):
        """Save chat message to database"""
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO chat_messages (user_id, user_type, message, response)
                VALUES (%s, %s, %s, %s)
            """, (user_id, user_type, message, response))
            mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error saving chat message: {e}")
            return False
    
    @staticmethod
    def get_history(mysql, user_id, user_type, limit=10):
        """Get chat history for a user"""
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT message, response, created_at
                FROM chat_messages
                WHERE user_id = %s AND user_type = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (user_id, user_type, limit))
            messages = cursor.fetchall()
            cursor.close()
            return list(reversed(messages))  # Return in chronological order
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
