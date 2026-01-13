"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Loader2 } from "lucide-react";

function CallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [error, setError] = useState("");

    useEffect(() => {
        const token = searchParams.get("token");
        if (token) {
            localStorage.setItem("token", token);
            router.push("/dashboard");
        } else {
            setError("Falha na autenticação. Token não fornecido.");
            setTimeout(() => router.push("/"), 3000);
        }
    }, [searchParams, router]);

    return (
        <div className="flex-1 flex flex-col items-center justify-center">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20 text-center">
                {error ? (
                    <div className="text-red-300 mb-2">{error}</div>
                ) : (
                    <>
                        <Loader2 className="w-10 h-10 text-emerald-500 animate-spin mx-auto mb-4" />
                        <h2 className="text-xl font-semibold text-gray-700">Autenticando...</h2>
                        <p className="text-gray-400 text-sm mt-2">Por favor aguarde.</p>
                    </>
                )}
            </div>
        </div>
    );
}

export default function AuthCallback() {
    return (
        <Suspense fallback={
            <div className="flex-1 flex items-center justify-center">
                <Loader2 className="w-10 h-10 text-emerald-500 animate-spin" />
            </div>
        }>
            <CallbackContent />
        </Suspense>
    );
}
