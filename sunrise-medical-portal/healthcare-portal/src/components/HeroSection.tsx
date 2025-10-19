// components/HeroSection.tsx
"use client";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

export default function HeroSection() {
  const router = useRouter();
  return (
    <section className="flex flex-col items-center justify-center text-center py-24 bg-gradient-to-b from-blue-50 to-white">
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-4xl font-bold text-sky-900 mb-4"
      >
        Welcome to Sunrise Medical Center
      </motion.h1>
      <p className="text-lg text-gray-600 max-w-xl mb-8">
        Your AI-powered assistant is here to help you find doctors and book
        appointments with ease.
      </p>
      <div className="flex gap-4">
        <Button onClick={() => router.push("/chat")} className="bg-sky-700 text-white hover:bg-sky-800">
          💬 Start Chat
        </Button>
        <Button
          onClick={() => router.push("/doctors")}
          variant="outline"
          className="border-sky-700 text-sky-700 hover:bg-sky-50"
        >
          👨‍⚕️ View Doctors
        </Button>
      </div>
    </section>
  );
}
