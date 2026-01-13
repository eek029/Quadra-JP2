import { cn } from "@/lib/utils";

const DAYS = [
    { label: "DOM", date: "10" },
    { label: "SEG", date: "11" },
    { label: "TER", date: "12" },
    { label: "QUA", date: "13" },
    { label: "QUI", date: "14", active: true },
    { label: "SEX", date: "15" },
    { label: "SÁB", date: "16" },
];

const MOCK_SLOTS = [
    { name: "Manhã", status: ["green", "green", "green", "green", "green", "green"] },
    { name: "Tarde", status: ["green", "green", "red", "yellow", "green", "green"] },
    { name: "Noite", status: ["green", "green", "green", "green", "red", "green"] },
];

export function CourtStatusGrid() {
    return (
        <div className="bg-white rounded-3xl p-4 shadow-sm mb-6">
            <div className="grid grid-cols-7 gap-2 mb-4 text-center">
                {DAYS.map((day) => (
                    <div key={day.label} className="flex flex-col items-center gap-1">
                        <span className="text-[10px] font-bold text-gray-400 uppercase">{day.label}</span>
                        <div
                            className={cn(
                                "w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-colors",
                                day.active
                                    ? "bg-blue-500 text-white shadow-md shadow-blue-200"
                                    : "text-gray-700 hover:bg-gray-100"
                            )}
                        >
                            {day.date}
                        </div>
                    </div>
                ))}
            </div>

            <div className="space-y-2">
                {MOCK_SLOTS.map((period, idx) => (
                    <div key={idx} className="flex gap-2 items-center">
                        <span
                            className={cn(
                                "text-[10px] font-medium w-12 text-left",
                                idx === 0 ? "text-emerald-600" :
                                    idx === 1 ? "text-emerald-500" : "text-orange-400"
                            )}
                        >
                            {period.name}
                        </span>
                        <div className="grid grid-cols-7 gap-2 flex-1">
                            {period.status.map((status, i) => (
                                <div
                                    key={i}
                                    className={cn(
                                        "h-8 rounded-lg w-full",
                                        status === "green" && "bg-emerald-400",
                                        status === "red" && "bg-red-500",
                                        status === "yellow" && "bg-amber-400"
                                    )}
                                />
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
