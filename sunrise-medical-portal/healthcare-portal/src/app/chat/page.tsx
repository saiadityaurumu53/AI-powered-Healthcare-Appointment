"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function ChatPage() {
  const searchParams = useSearchParams();
  const doctorPrefill = searchParams.get("doctor");

  const [messages, setMessages] = useState<{ role: string; content: string }[]>([
    { role: "ai", content: "👋 Hello! I’m your AI healthcare assistant. How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (doctorPrefill) {
      setMessages((prev) => [
        ...prev,
        { role: "user", content: `I’d like to book an appointment with ${doctorPrefill}.` },
      ]);
      handleSend(`I’d like to book an appointment with ${doctorPrefill}.`);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [doctorPrefill]);

  const handleSend = async (message?: string) => {
    const userMessage = message || input.trim();
    if (!userMessage) return;

    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage, user_id: "guest" }),
      });

      const data = await response.json();
      const reply = data.reply || "⚠️ Sorry, I didn’t get that. Please try again.";

      setMessages((prev) => [...prev, { role: "ai", content: reply }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: "⚠️ Network error. Please try again later." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col h-screen bg-sky-50">
      <header className="bg-sky-700 text-white py-4 px-6 text-center font-semibold text-lg">
        Sunrise Medical Center — AI Assistant
      </header>

      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`rounded-2xl px-4 py-2 max-w-xs sm:max-w-md ${
                msg.role === "user"
                  ? "bg-sky-700 text-white rounded-br-none"
                  : "bg-white border border-gray-200 rounded-bl-none"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-gray-500 text-sm italic">AI is typing...</div>
        )}
      </div>

      <div className="p-4 bg-white shadow-md flex gap-3">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-sky-600"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <Button onClick={() => handleSend()} className="bg-sky-700 hover:bg-sky-800 text-white">
          Send
        </Button>
      </div>
    </main>
  );
}

