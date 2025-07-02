import React, { useState } from "react";
import { Button } from "../ui/button";
import { Card } from "../ui/card";
import DestinationSelect from "./DestinationSelect";
import CurrencySelect from "./CurrencySelect";
import AdultsInput from "./AdultsInput";
import IATAPairInput from "./IATAPairInput";
import NightsInput from "./NightsInput";
import DateRangeInput from "./DateRangeInput";
import SummaryDisplay from "./SummaryDisplay";
import ToolMessagesSummary from "./ToolMessagesSummary";

interface Destination {
  label: string;
  value: string;
  from: string;
  to: string;
}

interface Currency {
  label: string;
  value: string;
}

interface FormState {
  destination: string;
  currency: string;
  adults: number;
  from: string;
  to: string;
  nights: number;
  start_date: string;
  return_date: string;
}

// Sample of world cities/airports (expand as needed or load from a JSON file)
const worldAirports = [
  { city: "Delhi", code: "DEL" },
  { city: "Mumbai", code: "BOM" },
  { city: "Chennai", code: "MAA" },
  { city: "Hyderabad", code: "HYD" },
  { city: "Bengaluru", code: "BLR" },
  { city: "Kolkata", code: "CCU" },
  { city: "Ahmedabad", code: "AMD" },
  { city: "Pune", code: "PNQ" },
  { city: "Goa", code: "GOI" },
  { city: "Kochi", code: "COK" },
  { city: "Jaipur", code: "JAI" },
  { city: "Lucknow", code: "LKO" },
  { city: "Guwahati", code: "GAU" },
  { city: "Thiruvananthapuram", code: "TRV" },
  { city: "Nagpur", code: "NAG" },
  { city: "New York", code: "JFK" },
  { city: "London", code: "LHR" },
  { city: "Dubai", code: "DXB" },
  { city: "Singapore", code: "SIN" },
  { city: "Tokyo", code: "NRT" },
  { city: "Paris", code: "CDG" },
  { city: "Frankfurt", code: "FRA" },
  { city: "Bangkok", code: "BKK" },
  { city: "Sydney", code: "SYD" },
  { city: "Hong Kong", code: "HKG" },
  { city: "Toronto", code: "YYZ" },
  { city: "Los Angeles", code: "LAX" },
  { city: "Chicago", code: "ORD" },
  { city: "Istanbul", code: "IST" },
  { city: "Amsterdam", code: "AMS" },
  { city: "Zurich", code: "ZRH" },
  { city: "Doha", code: "DOH" },
  { city: "Seoul", code: "ICN" },
  { city: "Madrid", code: "MAD" },
  { city: "Rome", code: "FCO" },
  { city: "San Francisco", code: "SFO" },
  { city: "Beijing", code: "PEK" },
  { city: "Shanghai", code: "PVG" },
  { city: "Cape Town", code: "CPT" },
  { city: "Johannesburg", code: "JNB" },
  { city: "Mexico City", code: "MEX" },
  { city: "Sao Paulo", code: "GRU" },
  { city: "Moscow", code: "SVO" },
  { city: "Vienna", code: "VIE" },
  { city: "Munich", code: "MUC" },
  { city: "Brussels", code: "BRU" },
  { city: "Copenhagen", code: "CPH" },
  { city: "Stockholm", code: "ARN" },
  { city: "Oslo", code: "OSL" },
  { city: "Helsinki", code: "HEL" },
  { city: "Lisbon", code: "LIS" },
  { city: "Vienna", code: "VIE" },
  { city: "Warsaw", code: "WAW" },
  { city: "Budapest", code: "BUD" },
  { city: "Prague", code: "PRG" },
  { city: "Athens", code: "ATH" },
  { city: "Dublin", code: "DUB" },
  { city: "Brisbane", code: "BNE" },
  { city: "Auckland", code: "AKL" },
  { city: "Kuala Lumpur", code: "KUL" },
  { city: "Jakarta", code: "CGK" },
  { city: "Manila", code: "MNL" },
  { city: "Bangkok", code: "BKK" },
  { city: "Abu Dhabi", code: "AUH" },
  { city: "Doha", code: "DOH" },
  // ...add more as needed
];

const destinations: Destination[] = worldAirports.map((a) => ({
  label: a.city,
  value: a.city,
  from: a.code,
  to: a.code,
}));

const currencies: Currency[] = [
  { label: "INR", value: "INR" },
  { label: "USD", value: "USD" },
  { label: "EUR", value: "EUR" },
];

function ThemeToggle() {
  const [dark, setDark] = useState(() =>
    document.documentElement.classList.contains("dark")
  );
  const toggle = () => {
    document.documentElement.classList.toggle("dark");
    setDark(document.documentElement.classList.contains("dark"));
  };
  return (
    <Button
      type="button"
      variant="outline"
      className="absolute top-4 right-4"
      onClick={toggle}
    >
      {dark ? "🌙 Dark" : "☀️ Light"}
    </Button>
  );
}

export default function TravelPlanner() {
  const [form, setForm] = useState<FormState>({
    destination: "",
    currency: "INR",
    adults: 1,
    from: "",
    to: "",
    nights: 3,
    start_date: "",
    return_date: "",
  });
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [toolMessages, setToolMessages] = useState<
    Array<{
      tool_name?: string;
      role?: string;
      content?: string;
      result?: string | number | object;
      summary?: string;
    }>
  >([]);

  const handleChange = (field: keyof FormState, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    // Auto-fill from/to when destination changes
    if (field === "destination") {
      const dest = destinations.find((d) => d.value === value);
      if (dest) setForm((prev) => ({ ...prev, from: dest.from, to: dest.to }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSummary("");
    try {
      const res = await fetch("http://localhost:5000/api/travelsgent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: form }),
      });
      const data = await res.json();
      let summaryText = "";
      if (typeof data === "string") {
        summaryText = data;
      } else if (data.final_answer) {
        summaryText = data.final_answer;
      } else if (data.summary) {
        summaryText = data.summary;
      } else {
        summaryText = JSON.stringify(data, null, 2);
      }
      setSummary(summaryText);
      if (data.messages && Array.isArray(data.messages)) {
        setToolMessages(data.messages);
      }
    } catch (err) {
      setSummary("Error fetching summary.");
    }
    setLoading(false);
  };

  // Helper to extract flight details from summary (if JSON)
  let flightDetails = null;
  try {
    const parsed = JSON.parse(summary);
    if (parsed && (parsed.flights_onward || parsed.flights_return)) {
      flightDetails = (
        <div className="space-y-2">
          {parsed.flights_onward && (
            <div>
              <div className="font-semibold">Flights Onward:</div>
              <pre className="bg-muted rounded p-2 text-xs whitespace-pre-wrap">
                {JSON.stringify(parsed.flights_onward, null, 2)}
              </pre>
            </div>
          )}
          {parsed.flights_return && (
            <div>
              <div className="font-semibold">Flights Return:</div>
              <pre className="bg-muted rounded p-2 text-xs whitespace-pre-wrap">
                {JSON.stringify(parsed.flights_return, null, 2)}
              </pre>
            </div>
          )}
        </div>
      );
    }
  } catch {}

  return (
    <div className="flex flex-col md:flex-row gap-8 items-start justify-center md:w-[1420px] min-h-screen bg-background dark:bg-[#18181b] transition-colors">
      <ThemeToggle />
      {/* Tool messages summary panel, far left, does not affect other columns */}
      <div className="hidden md:block  flex-shrink-0">
        <ToolMessagesSummary messages={toolMessages} />
      </div>
      <div className="w-full md:w-[420px] flex-shrink-0">
        <Card className="p-6 shadow-lg bg-white dark:bg-[#232326] dark:text-white">
          <h1 className="text-3xl font-bold mb-8 text-center tracking-tight dark:text-white">
            Travel Planner
          </h1>
          {loading && (
            <div className="flex justify-center items-center mb-4">
              <span className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900 dark:border-white mr-2"></span>
              <span>Loading...</span>
            </div>
          )}
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex gap-4">
              <div className="flex-1">
                <DestinationSelect
                  value={form.destination}
                  onChange={(v: string) => handleChange("destination", v)}
                  destinations={destinations}
                />
              </div>
              <div className="flex-1">
                <CurrencySelect
                  value={form.currency}
                  onChange={(v: string) => handleChange("currency", v)}
                  currencies={currencies}
                />
              </div>
            </div>
            <AdultsInput
              value={form.adults}
              onChange={(v: number) => handleChange("adults", v)}
            />
            <IATAPairInput
              from={form.from}
              to={form.to}
              onFromChange={(v: string) => handleChange("from", v)}
              onToChange={(v: string) => handleChange("to", v)}
            />
            <NightsInput
              value={form.nights}
              onChange={(v: number) => handleChange("nights", v)}
            />
            <DateRangeInput
              start_date={form.start_date}
              return_date={form.return_date}
              onStartChange={(v: string) => handleChange("start_date", v)}
              onReturnChange={(v: string) => handleChange("return_date", v)}
            />
            <Button
              type="submit"
              disabled={loading}
              className="w-full dark:bg-[#333] dark:text-white mt-2"
            >
              {loading ? "Planning..." : "Plan My Trip"}
            </Button>
          </form>
        </Card>
      </div>
      <div className="w-full md:w-[500px] flex-shrink-0">
        <Card className="p-6 shadow-lg bg-white dark:bg-[#232326] dark:text-white">
          <h2 className="text-xl font-semibold mb-4 text-center dark:text-white">
            Summary
          </h2>
          <SummaryDisplay summary={summary} />
          {flightDetails && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-2 dark:text-white">
                Flight Booking Details
              </h3>
              {flightDetails}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
