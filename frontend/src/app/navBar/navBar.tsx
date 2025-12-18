"use client";

import Link from "next/link";

export default function Navbar() {
  const text = "GameSense".split("");
  const colors = [
    "text-purple-500",
    "text-white",
  ];

  return (
    <nav className="w-full h-16 flex items-center px-6 bg-gray-950 border-b border-gray-700 shadow-lg">
      <div className="flex w-full justify-between items-center">

        {/* Logo */}
        <Link
          href="/"
          className="text-xl font-bold flex items-center gap-1 hover:text-purple-300 transition"
        >
          {text.map((char, i) => (
            <span
              key={i}
              className={`${colors[i % colors.length]} transition drop-shadow-[0_0_4px_rgba(168,85,247,0.5)]`}
            >
              {char}
            </span>
          ))}

        </Link>

        {/* Menu */}
        <div className="flex space-x-2 md:space-x-7 text-white text-sm font-semibold">
          <Link
            href="/home"
            className="hover:text-purple-300 hover:underline underline-offset-4 transition max-w-14 md:max-w-none"
          >
            Player Search
          </Link>
          <Link
            href="/leaderboard"
            className="hover:text-purple-300 hover:underline underline-offset-4 transition max-w-24 md:max-w-none"
          >
            View Leaderboard
          </Link>
        </div>

      </div>
    </nav>


  );
}

