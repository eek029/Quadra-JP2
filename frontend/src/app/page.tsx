import { Calendar, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { Footer } from "@/components/Footer";

export default function Home() {
  const googleLoginUrl = process.env.NEXT_PUBLIC_API_URL
    ? `${process.env.NEXT_PUBLIC_API_URL}/auth/login/google`
    : "http://localhost:8000/api/v1/auth/login/google";

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
        <div className="bg-white rounded-3xl p-8 sm:p-12 shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 max-w-md w-full">
          <div className="mb-6 flex justify-center">
            <div className="p-4 bg-emerald-50 rounded-full">
              <Calendar className="w-12 h-12 text-emerald-500" />
            </div>
          </div>

          <h1 className="text-2xl font-bold text-gray-900 mb-2">Quadra do Condomínio</h1>
          <p className="text-gray-500 mb-8">
            Agende seu horário, gerencie reservas e receba notificações.
          </p>

          <Link
            href={googleLoginUrl}
            className="group relative w-full flex justify-center py-3 px-4 border border-gray-200 text-sm font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all shadow-sm"
          >
            <span className="absolute left-0 inset-y-0 flex items-center pl-3">
              <ShieldCheck className="h-5 w-5 text-emerald-500 group-hover:text-emerald-600" aria-hidden="true" />
            </span>
            Entrar com Google
          </Link>

          <div className="mt-6 text-xs text-gray-400">
            Acesso restrito a moradores e administração.
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
