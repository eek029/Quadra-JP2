import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Footer } from "@/components/Footer";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Quadra do Condomínio",
  description: "Sistema de reservas da quadra",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className={cn(
        inter.className,
        "min-h-screen bg-gray-50 text-gray-900 antialiased"
      )}>
        <main className="min-h-screen flex flex-col">
          {children}
        </main>
        {/* Footer is now included inside dashboard/page for mobile flow, or globally here. 
            For the mockup style, the footer was at the very bottom. 
            We'll leave it global but style it to fit the new theme. */}
        {/* <Footer /> rendered conditionally or inside pages if strictly mobile layout is desired 
            Since we switched to a 'mobile app' layout, the footer might look weird fixed at bottom of viewport 
            if content scrolls. Let's put it in the flow. */}
      </body>
    </html>
  );
}
