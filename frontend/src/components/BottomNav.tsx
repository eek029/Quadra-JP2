import Link from "next/link";
import { Home, Calendar, User, Menu } from "lucide-react";

export function BottomNav() {
    return (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-6 py-3 flex justify-between items-center z-50 rounded-t-3xl shadow-[0_-5px_20px_rgba(0,0,0,0.05)] text-gray-400">
            <Link href="/dashboard" className="flex flex-col items-center gap-1 text-indigo-600">
                <Home className="w-6 h-6 fill-current" />
            </Link>
            <Link href="/dashboard/calendar" className="flex flex-col items-center gap-1 hover:text-indigo-600 transition-colors">
                <Calendar className="w-6 h-6" />
            </Link>
            <Link href="/dashboard/profile" className="flex flex-col items-center gap-1 hover:text-indigo-600 transition-colors">
                <User className="w-6 h-6" />
            </Link>
            <button className="flex flex-col items-center gap-1 hover:text-indigo-600 transition-colors">
                <Menu className="w-6 h-6" />
            </button>
        </div>
    );
}
