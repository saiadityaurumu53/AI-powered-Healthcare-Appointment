"use client";

import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

interface Doctor {
  doctor_id: string;
  doctor_name: string;
  specialization: string;
  hospital_name: string;
  room_number: string;
  contact_number: string;
  email: string;
}

export default function DoctorCard({ doctor }: { doctor: Doctor }) {
  const router = useRouter();

  return (
    <Card className="shadow-md hover:shadow-lg transition bg-white border-sky-100">
      <CardHeader>
        <CardTitle className="text-sky-800 font-semibold">{doctor.doctor_name}</CardTitle>
        <CardDescription>{doctor.specialization}</CardDescription>
      </CardHeader>
      <CardContent className="text-sm text-gray-700 space-y-1">
        <p><strong>Hospital:</strong> {doctor.hospital_name}</p>
        <p><strong>Room:</strong> {doctor.room_number}</p>
        <p><strong>Contact:</strong> {doctor.contact_number}</p>
        <p><strong>Email:</strong> {doctor.email}</p>
      </CardContent>
      <CardFooter>
        <Button
          onClick={() => router.push(`/chat?doctor=${encodeURIComponent(doctor.doctor_name)}`)}
          className="bg-sky-700 text-white hover:bg-sky-800"
        >
          Book Appointment
        </Button>
      </CardFooter>
    </Card>
  );
}
