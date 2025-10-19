"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const links = [
    { name: "Home", href: "/" },
    { name: "Doctors", href: "/doctors" },
    { name: "Book Appointment", href: "/chat" },
    { name: "Contact", href: "#footer" },
  ];

  return (
    <nav className="w-full bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-sky-700">
          🌅 Sunrise Medical Center
        </Link>
        <div className="flex gap-6 text-gray-700">
          {links.map((link) => (
            <Link
              key={link.name}
              href={link.href}
              className={`hover:text-sky-700 transition ${
                pathname === link.href ? "text-sky-700 font-semibold" : ""
              }`}
            >
              {link.name}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
