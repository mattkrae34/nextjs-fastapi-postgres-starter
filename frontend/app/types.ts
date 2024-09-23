export type User = {
    id: string;
    name: string;
};

export type Message = {
    id: string;
    content: string;
    conversationId: string;
    timestamp: string;
};

export type Conversation = {
    id: string;
    createdAt: string;
    updatedAt: string;
    messages: Message[];
};