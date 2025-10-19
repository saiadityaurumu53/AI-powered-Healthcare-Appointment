"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function CTASection() {
  const router = useRouter();
  return (
    <section className="bg-sky-700 text-white py-16 text-center">
      <h2 className="text-2xl font-semibold mb-4">
        Ready to book your appointment?
      </h2>
      <p className="mb-6 text-gray-100">
        Experience healthcare made simple with Sunrise AI Assistant.
      </p>
      <Button
        onClick={() => router.push("/chat")}
        className="bg-white text-sky-700 hover:bg-gray-100"
      >
        💬 Start Chat
      </Button>
    </section>
  );
}
