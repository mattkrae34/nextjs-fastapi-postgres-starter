"use client";

import { useEffect, useState } from "react";
import MessageInput from "./components/MessageInput";
import { Conversation, User } from "./types";
import ConversationDisplay from "./components/ConversationDisplay";
import { useRouter, useSearchParams } from "next/navigation";


const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [user, setUser] = useState<User | null>(null)
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null)
  const router = useRouter();
  const searchParams = useSearchParams();
  useEffect(() => {
    async function fetchData() {
      try {
        const user: User = await fetch(`${apiUrl}/users/me`).then((res) =>
          res.json()
        );
        setUser(user);
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    }

    fetchData();
  }, []);

  useEffect(() => {
    async function loadConversation() {
      const conversationId = searchParams.get('conversationId');
      if (conversationId && typeof conversationId === 'string') {
        try {
          const conversation: Conversation = await fetch(`${apiUrl}/conversations/${conversationId}`).then((res) =>
            res.json()
          );
          setCurrentConversation(conversation);
        } catch (error) {
          console.error("Error fetching conversation:", error);
        }
      }
    }

    loadConversation();
  }, [searchParams]);

  const handleNewConversation = (newConversation: Conversation) => {
    setCurrentConversation(newConversation);
    router.push(`/?conversationId=${newConversation.id}`);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      Hello, {user?.name ?? ''}!
      <div>
        <ConversationDisplay currentConversation={currentConversation} />
      </div>
      <div>
        <MessageInput currentConversation={currentConversation} setCurrentConversation={handleNewConversation} />
      </div>
    </main>
  );
}
