import { CourtStatusGrid } from "@/components/CourtStatusGrid";
import { BottomNav } from "@/components/BottomNav";
import Image from "next/image";

export default function Dashboard() {
    return (
        <div className="flex-1 bg-gray-50 pb-20"> {/* pb-20 for bottom nav space */}
            {/* Header Mobile Title */}
            <header className="pt-12 pb-6 px-6 bg-white">
                <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-emerald-400 rounded-full flex items-center justify-center p-2.5 shadow-lg shadow-emerald-200">
                        {/* Icon Placeholder (Court Icon) */}
                        <svg viewBox="0 0 24 24" fill="none" className="w-full h-full text-white" stroke="currentColor" strokeWidth="2">
                            <path d="M3 3h18v18H3z" />
                            <path d="M12 3v18" />
                            <path d="M3 12h18" />
                        </svg>
                    </div>
                    <h1 className="text-xl font-bold text-gray-800 leading-tight">
                        Reserva Quadra de<br /> Esportes JP
                    </h1>
                </div>
            </header>

            <main className="px-6 space-y-6">
                {/* Calendar Grid Widget */}
                <CourtStatusGrid />

                {/* Featured Court Image */}
                <div className="relative w-full h-48 rounded-3xl overflow-hidden shadow-sm">
                    {/* Fallback mock image if no real image available */}
                    <div className="w-full h-full bg-blue-100 flex items-center justify-center">
                        <span className="text-blue-300 font-bold">Foto da Quadra</span>
                    </div>
                    {/* <Image 
            src="/court-photo.jpg" 
            alt="Quadra" 
            fill 
            className="object-cover"
          /> */}
                </div>

                {/* Action Buttons Row */}
                <div className="grid grid-cols-3 gap-3">
                    <button className="bg-emerald-400 hover:bg-emerald-500 text-white p-4 rounded-2xl shadow-lg shadow-emerald-200 flex flex-col items-center justify-center gap-1 transition-transform active:scale-95">
                        <span className="text-sm font-bold leading-tight">Nova<br />Reserva</span>
                    </button>
                    <button className="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-2xl shadow-lg shadow-blue-200 flex flex-col items-center justify-center gap-1 transition-transform active:scale-95">
                        <span className="text-sm font-bold leading-tight">Minhas<br />Reservas</span>
                    </button>
                    <button className="bg-orange-500 hover:bg-orange-600 text-white p-4 rounded-2xl shadow-lg shadow-orange-200 flex flex-col items-center justify-center gap-1 transition-transform active:scale-95">
                        <span className="text-sm font-bold">Calendário</span>
                    </button>
                </div>

                {/* Upcoming Reservations List */}
                <div className="grid grid-cols-2 gap-4">
                    {/* Card 1 */}
                    <div className="bg-white p-4 rounded-3xl shadow-sm border border-gray-100">
                        <div className="inline-block px-3 py-1 bg-emerald-400 text-white text-[10px] font-bold rounded-full mb-2">SEXTA, 14 ABRIL</div>
                        <div className="text-lg font-bold text-gray-800">10:00 - 11:00</div>
                        <div className="text-xs text-blue-500 font-medium mb-3">Quadra poliesportiva</div>
                        <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-gray-200 rounded-full" />
                            <span className="text-xs text-gray-600 font-medium">Pedro Sousa</span>
                        </div>
                    </div>

                    {/* Card 2 */}
                    <div className="bg-white p-4 rounded-3xl shadow-sm border border-gray-100">
                        <div className="inline-block px-3 py-1 bg-orange-400 text-white text-[10px] font-bold rounded-full mb-2">QUINTA, 1N ABRIL</div>
                        <div className="text-lg font-bold text-gray-800">18:00 - 19:00</div>
                        <div className="text-xs text-blue-500 font-medium mb-3">Quadra poliesportiva</div>
                        <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-gray-200 rounded-full" />
                            <span className="text-xs text-gray-600 font-medium">Ana Martins</span>
                        </div>
                    </div>
                </div>
            </main>

            <BottomNav />
        </div>
    );
}
