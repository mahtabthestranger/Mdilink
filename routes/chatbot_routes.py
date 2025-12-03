# Chatbot API Route
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chatbot messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get user context
        user_context = None
        if session.get('user_type'):
            user_context = {
                'user_type': session.get('user_type'),
                'user_id': session.get('user_id'),
                'user_name': session.get('user_name', 'User')
            }
        
        # Get chatbot response
        response = Chatbot.get_response(message, user_context)
        
        # Save to database if user is logged in
        if user_context:
            Chatbot.save_message(
                mysql,
                user_context['user_id'],
                user_context['user_type'],
                message,
                response
            )
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Failed to process message'}), 500
