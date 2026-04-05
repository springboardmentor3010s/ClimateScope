import { useState, useMemo, useCallback } from "react";
import { getWeatherData, getDataForLocations, getDataInRange, type VariableKey, LOCATIONS } from "@/data/weatherData";
import { ControllerPanel, type Season, SEASONS } from "@/components/dashboard/ControllerPanel";
import { ExecutiveOverview } from "@/components/dashboard/ExecutiveOverview";
import { TemperatureIntelligence } from "@/components/dashboard/TemperatureIntelligence";
import { PrecipWindIntelligence } from "@/components/dashboard/PrecipWindIntelligence";
import { ExtremeEventsMonitor } from "@/components/dashboard/ExtremeEventsMonitor";
import { RegionalComparison } from "@/components/dashboard/RegionalComparison";
import { ClimateRiskIntelligence } from "@/components/dashboard/ClimateRiskIntelligence";
import {
  LayoutDashboard, Thermometer, CloudRain, AlertTriangle, Globe, Shield,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

type PageKey = "overview" | "temperature" | "precip-wind" | "extreme" | "regional" | "risk";

const PAGES = [
  { key: "overview" as PageKey, label: "Executive Overview", icon: LayoutDashboard },
  { key: "temperature" as PageKey, label: "Temperature", icon: Thermometer },
  { key: "precip-wind" as PageKey, label: "Precip & Wind", icon: CloudRain },
  { key: "extreme" as PageKey, label: "Extreme Events", icon: AlertTriangle },
  { key: "regional" as PageKey, label: "Regional Compare", icon: Globe },
  { key: "risk" as PageKey, label: "Climate Risk", icon: Shield },
];

const Index = () => {
  const [activePage, setActivePage] = useState<PageKey>("overview");
  const [selectedLocations, setSelectedLocations] = useState<string[]>(["Mauna Loa Observatory", "Tokyo", "London"]);
  const [activeVariables, setActiveVariables] = useState<VariableKey[]>(["temperature_celsius", "humidity"]);
  const [timeRange, setTimeRange] = useState<[number, number]>([0, 364]);
  const [currentDayIndex, setCurrentDayIndex] = useState(180);
  const [selectedSeason, setSelectedSeason] = useState<Season>("all");

  const baseDate = new Date("2024-01-01");
  const formatDayISO = (idx: number) => {
    const d = new Date(baseDate);
    d.setDate(d.getDate() + idx);
    return d.toISOString().split("T")[0];
  };

  const startDate = formatDayISO(timeRange[0]);
  const endDate = formatDayISO(timeRange[1]);

  const filteredData = useMemo(() => {
    const locationData = getDataForLocations(selectedLocations);
    const rangeData = getDataInRange(locationData, startDate, endDate);
    if (selectedSeason === "all") return rangeData;
    const seasonMonths = SEASONS.find(s => s.key === selectedSeason)!.months;
    return rangeData.filter(r => {
      const month = parseInt(r.date.substring(5, 7), 10);
      return seasonMonths.includes(month);
    });
  }, [selectedLocations, startDate, endDate, selectedSeason]);

  const handleToggleLocation = useCallback((city: string) => {
    setSelectedLocations((prev) =>
      prev.includes(city) ? prev.filter((c) => c !== city) : [...prev, city]
    );
  }, []);

  const handleSelectAllLocations = useCallback(() => {
    setSelectedLocations((prev) =>
      prev.length === LOCATIONS.length ? [] : LOCATIONS.map(l => l.city)
    );
  }, []);

  const handleToggleVariable = useCallback((key: VariableKey) => {
    setActiveVariables((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
    );
  }, []);

  const renderPage = () => {
    switch (activePage) {
      case "overview":
        return <ExecutiveOverview data={filteredData} selectedLocations={selectedLocations} onToggleLocation={handleToggleLocation} />;
      case "temperature":
        return <TemperatureIntelligence data={filteredData} selectedLocations={selectedLocations} />;
      case "precip-wind":
        return <PrecipWindIntelligence data={filteredData} selectedLocations={selectedLocations} />;
      case "extreme":
        return <ExtremeEventsMonitor data={filteredData} selectedLocations={selectedLocations} />;
      case "regional":
        return <RegionalComparison data={filteredData} selectedLocations={selectedLocations} />;
      case "risk":
        return <ClimateRiskIntelligence data={filteredData} selectedLocations={selectedLocations} />;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-canvas">
      {/* Left: Controller + Nav */}
      <div className="w-80 min-w-[320px] h-screen flex flex-col border-r border-border bg-card overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-primary flex items-center justify-center">
              <Globe className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="font-mono text-sm font-bold tracking-wider uppercase text-foreground">
                Terraforma
              </h1>
              <p className="font-body text-[11px] text-muted-foreground">
                Global Weather Observatory
              </p>
            </div>
          </div>
        </div>

        {/* Page Navigation */}
        <div className="px-3 pt-4 pb-1">
          <label className="px-2 font-body text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">
            Dashboard
          </label>
          <nav className="mt-2 space-y-0.5">
            {PAGES.map((page) => {
              const Icon = page.icon;
              const isActive = activePage === page.key;
              return (
                <button
                  key={page.key}
                  onClick={() => setActivePage(page.key)}
                  className={`w-full flex items-center gap-2.5 px-3 py-2.5 text-[13px] font-body rounded-lg transition-all duration-150 ${
                    isActive
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "text-foreground hover:bg-hover"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{page.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Embedded mini controller */}
        <div className="flex-1 overflow-y-auto">
          <ControllerPanel
            selectedLocations={selectedLocations}
            onToggleLocation={handleToggleLocation}
            onSelectAllLocations={handleSelectAllLocations}
            activeVariables={activeVariables}
            onToggleVariable={handleToggleVariable}
            timeRange={timeRange}
            onTimeRangeChange={setTimeRange}
            currentDayIndex={currentDayIndex}
            onCurrentDayChange={setCurrentDayIndex}
            selectedSeason={selectedSeason}
            onSeasonChange={setSelectedSeason}
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 h-screen overflow-y-auto bg-canvas">
        <AnimatePresence mode="wait">
          <motion.div
            key={activePage}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
          >
            {renderPage()}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Index;
