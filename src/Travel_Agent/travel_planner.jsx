import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import DestinationSelect from "./components/DestinationSelect";
import CurrencySelect from "./components/CurrencySelect";
import AdultsInput from "./components/AdultsInput";
import IATAPairInput from "./components/IATAPairInput";
import NightsInput from "./components/NightsInput";
import DateRangeInput from "./components/DateRangeInput";
import SummaryDisplay from "./components/SummaryDisplay";

const destinations = [
  { label: "Tokyo", value: "Tokyo", from: "DEL", to: "NRT" },
  { label: "New York", value: "New York", from: "DEL", to: "JFK" },
  // Add more destinations as needed
];

const currencies = [
  { label: "INR", value: "INR" },
  { label: "USD", value: "USD" },
  { label: "EUR", value: "EUR" },
];

export default function TravelPlanner() {
  const [form, setForm] = useState({
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

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    // Auto-fill from/to when destination changes
    if (field === "destination") {
      const dest = destinations.find((d) => d.value === value);
      if (dest) setForm((prev) => ({ ...prev, from: dest.from, to: dest.to }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSummary("");
    try {
      const res = await fetch("/api/your-travel-endpoint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: form }),
      });
      const data = await res.json();
      setSummary(data.summary || JSON.stringify(data, null, 2));
    } catch (err) {
      setSummary("Error fetching summary.");
    }
    setLoading(false);
  };

  return (
    <Card className="max-w-xl mx-auto mt-8 p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <DestinationSelect
          value={form.destination}
          onChange={(v) => handleChange("destination", v)}
          destinations={destinations}
        />
        <CurrencySelect
          value={form.currency}
          onChange={(v) => handleChange("currency", v)}
          currencies={currencies}
        />
        <AdultsInput
          value={form.adults}
          onChange={(v) => handleChange("adults", v)}
        />
        <IATAPairInput
          from={form.from}
          to={form.to}
          onFromChange={(v) => handleChange("from", v)}
          onToChange={(v) => handleChange("to", v)}
        />
        <NightsInput
          value={form.nights}
          onChange={(v) => handleChange("nights", v)}
        />
        <DateRangeInput
          start_date={form.start_date}
          return_date={form.return_date}
          onStartChange={(v) => handleChange("start_date", v)}
          onReturnChange={(v) => handleChange("return_date", v)}
        />
        <Button type="submit" disabled={loading}>
          {loading ? "Planning..." : "Plan My Trip"}
        </Button>
      </form>
      <SummaryDisplay summary={summary} />
    </Card>
  );
}
