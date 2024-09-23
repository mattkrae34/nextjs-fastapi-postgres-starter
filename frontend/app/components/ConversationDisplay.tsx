import React from 'react';
import { format } from 'date-fns';
import { Conversation, Message } from '../types';

interface ConversationDisplayProps {
    currentConversation: Conversation | null;
}

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
    return (
        <div className="mb-4">
            <div className="bg-blue-100 rounded-lg p-3 inline-block max-w-[70%]">
                <p className="text-gray-800">{message.content}</p>
            </div>
            <div className="text-xs text-gray-500 mt-1">
                {format(new Date(message.timestamp), 'MMM d, yyyy HH:mm')}
            </div>
        </div>
    );
};

export const ConversationDisplay: React.FC<ConversationDisplayProps> = ({ currentConversation }) => {
    if (!currentConversation) {
        return (
            <div className="w-full max-w-4xl mx-auto p-4 bg-white rounded-lg shadow">
                <p className="text-gray-500 italic">Please start a conversation...</p>
            </div>
        );
    }

    return (
        <div className="w-full max-w-4xl mx-auto p-4 bg-white rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Conversation</h2>
            <div className="space-y-4">
                {currentConversation.messages.map((message) => (
                    <MessageBubble key={message.id} message={message} />
                ))}
            </div>
        </div>
    );
};

export default ConversationDisplay;