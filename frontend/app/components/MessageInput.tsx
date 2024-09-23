import React, { useState, KeyboardEvent, Dispatch, SetStateAction, useCallback } from 'react';
import { Conversation } from '../types';

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export const MessageInput = (props: { 
    currentConversation: Conversation | null;
    setCurrentConversation: (newConversation: Conversation) => void
 }): JSX.Element => {
    const [message, setMessage] = useState('');

    const handleSubmit = useCallback(async () => {        
        console.log("message", message);
        if (message.trim() === '') return;

        const url = props.currentConversation?.id ? `${apiUrl}/conversations/${props.currentConversation.id}/messages` : `${apiUrl}/conversations`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: message }),
            });

            if (response.ok) {
                setMessage('');
                const conversation = await response.json();
                props.setCurrentConversation(conversation);
                console.log('Message sent successfully');
            } else {
                console.error('Failed to send message');
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    }, [message, props.setCurrentConversation]);


    return (
        <div style={{width: "800px"}} className="w-full max-w-4xl mx-auto p-4">
          <div className="flex flex-col space-y-3">
            <textarea
              className="w-full p-3 border border-gray-300 rounded-md resize-none text-lg"
              rows={4}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message here..."
            />
            <button
              className="w-full px-6 py-3 bg-blue-500 text-white rounded-md hover:bg-blue-600 text-lg font-semibold"
              onClick={handleSubmit}
            >
              Send
            </button>
          </div>
        </div>
      );
};

export default MessageInput;