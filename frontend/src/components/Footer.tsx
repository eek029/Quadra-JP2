import Link from "next/link";
import { Send, Twitter } from "lucide-react"; // Using Lucide icons for cleaner look

export function Footer() {
    return (
        <footer className="w-full text-[10px] text-gray-400 py-6 mb-16 text-center">
            <div className="mx-auto max-w-sm px-6 flex flex-col items-center gap-2">
                <span className="select-none leading-relaxed">
                    © 2026 eek029 Sistemas e Automação.<br />Todos os direitos reservados.
                </span>

                {/* Social Links */}
                <div className="flex items-center gap-4 mt-1">
                    <Link
                        href="https://t.me/eek029"
                        className="flex items-center gap-1 hover:text-indigo-500 transition-colors"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <Send className="w-3 h-3" />
                        <span>Telegram</span>
                    </Link>
                    <span className="text-gray-300">•</span>
                    <Link
                        href="https://x.com/eek029"
                        className="flex items-center gap-1 hover:text-indigo-500 transition-colors"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        {/* X logo fallback using text or custom svg if preferred, using text for simplicity or Twitter icon */}
                        <span className="font-bold text-xs">X</span>
                        <span>Twitter</span>
                    </Link>
                </div>
            </div>
        </footer>
    );
}
