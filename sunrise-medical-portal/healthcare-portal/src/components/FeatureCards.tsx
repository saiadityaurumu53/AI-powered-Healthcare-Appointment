import { Card, CardHeader, CardContent, CardTitle, CardDescription } from "@/components/ui/card";
import { HeartPulse, Mic, Clock } from "lucide-react";

export default function FeatureCards() {
  const features = [
    {
      icon: <HeartPulse className="text-sky-700 w-10 h-10" />,
      title: "AI Appointment Assistant",
      desc: "Book appointments naturally through chat or voice.",
    },
    {
      icon: <Mic className="text-sky-700 w-10 h-10" />,
      title: "Accessibility First",
      desc: "Voice and translation support for all users.",
    },
    {
      icon: <Clock className="text-sky-700 w-10 h-10" />,
      title: "Instant Availability",
      desc: "See real-time doctor schedules and time slots.",
    },
  ];

  return (
    <section className="grid md:grid-cols-3 gap-6 px-8 py-16 bg-white">
      {features.map((f, idx) => (
        <Card key={idx} className="shadow-md hover:shadow-lg transition">
          <CardHeader className="flex flex-col items-center">
            {f.icon}
            <CardTitle className="mt-2 text-xl">{f.title}</CardTitle>
          </CardHeader>
          <CardContent className="text-center text-gray-600">
            <CardDescription>{f.desc}</CardDescription>
          </CardContent>
        </Card>
      ))}
    </section>
  );
}
