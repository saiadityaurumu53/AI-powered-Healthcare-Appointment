"use client";

import { useEffect, useState } from "react";
import DoctorCard from "@/components/DoctorCard";

export default function DoctorsPage() {
  const [doctors, setDoctors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchDoctors() {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/doctors`);
        const data = await response.json();
        if (data.status === "success") {
          setDoctors(data.doctors);
        } else {
          setError("Failed to load doctors.");
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchDoctors();
  }, []);

  if (loading) return <div className="text-center mt-20 text-gray-600">Loading doctors...</div>;
  if (error) return <div className="text-center mt-20 text-red-600">⚠️ {error}</div>;

  return (
    <main className="min-h-screen bg-sky-50 py-12 px-6">
      <h1 className="text-3xl font-bold text-center text-sky-900 mb-2">
        Our Doctors
      </h1>
      <p className="text-center text-gray-600 mb-10">
        Meet our team of specialists at Sunrise Medical Center.
      </p>

      <div className="grid md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-6 max-w-7xl mx-auto">
        {doctors.map((doctor) => (
          <DoctorCard key={doctor.doctor_id} doctor={doctor} />
        ))}
      </div>
    </main>
  );
}
