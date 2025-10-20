import type { NextConfig } from "next";

const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true, // ✅ Skip ESLint errors in production builds
  },
  typescript: {
    ignoreBuildErrors: true, // ✅ Skip TypeScript type errors during build
  },
};

export default nextConfig;
