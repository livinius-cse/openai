import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ForgeAI | Engineering intelligence",
  description: "Transform real-world problems into engineering opportunities.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
