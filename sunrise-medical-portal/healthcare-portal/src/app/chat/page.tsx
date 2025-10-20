import { Suspense } from "react";
import ChatClient from "./ChatClient";

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="p-6 text-gray-500">Loading chat...</div>}>
      <ChatClient />
    </Suspense>
  );
}
