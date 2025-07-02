import React from "react";

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
  { city: "Abu Dhabi", code: "AUH" },
  // ...add more as needed
];

interface Props {
  from: string;
  to: string;
  onFromChange: (value: string) => void;
  onToChange: (value: string) => void;
}

const IATAPairInput: React.FC<Props> = ({
  from,
  to,
  onFromChange,
  onToChange,
}) => (
  <div>
    <div className="flex-1">
      <label className="mb-1">From</label>
      <select
        className="w-full rounded border px-2 py-2 bg-background dark:bg-[#232326] text-foreground dark:text-white"
        value={from}
        onChange={(e) => onFromChange(e.target.value)}
      >
        <option value="">Select city/airport</option>
        {worldAirports.map((a) => (
          <option key={a.code} value={a.code}>
            {a.city} ({a.code})
          </option>
        ))}
      </select>
    </div>
    <div className="flex-1">
      <label className="mb-1">To</label>
      <select
        className="w-full rounded border px-2 py-2 bg-background dark:bg-[#232326] text-foreground dark:text-white"
        value={to}
        onChange={(e) => onToChange(e.target.value)}
      >
        <option value="">Select city/airport</option>
        {worldAirports.map((a) => (
          <option key={a.code} value={a.code}>
            {a.city} ({a.code})
          </option>
        ))}
      </select>
    </div>
  </div>
);

export default IATAPairInput;
