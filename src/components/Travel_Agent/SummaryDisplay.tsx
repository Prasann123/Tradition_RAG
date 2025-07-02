import React, { useState } from "react";
import { CardContent } from "../ui/card";

interface Props {
  summary: string;
}

// Helper to split summary into sections by headings (e.g., **Dates**, **Flights**, **Hotel**, **Itinerary**)
function splitSections(summary: string) {
  const sectionRegex =
    /\*\*(.+?)\*\*\s*\n([\s\S]*?)(?=(?:\*\*.+?\*\*\s*\n)|$)/g;
  const sections: { title: string; content: string }[] = [];
  let match;
  while ((match = sectionRegex.exec(summary)) !== null) {
    // Merge all Day X sections into the previous 'Attractions and Itinerary' or 'Itinerary' section
    if (/^Day \d+/i.test(match[1]) && sections.length > 0) {
      sections[sections.length - 1].content +=
        "\n\n" + `**${match[1]}**\n${match[2]}`;
    } else {
      sections.push({ title: match[1].trim(), content: match[2].trim() });
    }
  }
  return sections;
}

const sectionEmojis: Record<string, string> = {
  Dates: "📅",
  "Travel Dates": "📅",
  "Onward Flight": "🛫",
  "Return Flight": "🛬",
  Hotel: "🏨",
  "Stay Location": "🏨",
  Itinerary: "🗺️",
  "Attractions and Itinerary": "🗺️",
  Weather: "🌤️",
  Budget: "💰",
  Currency: "💱",
  "Day 1": "📄",
  "Day 2": "📄",
  "Day 3": "📄",
  "Day 4": "📄",
  "Day 5": "📄",
  Restaurant: "🍽️",
  Transport: "🚗",
  "Check-in": "🛎️",
  "Check-out": "🏁",
};

const SummaryDisplay: React.FC<Props> = ({ summary }) => {
  const [page, setPage] = useState(0);
  const sections = splitSections(summary);
  // Group all non-itinerary sections on page 1, itinerary on page 2
  const itinerarySections = sections.filter(
    (s) => /itinerary/i.test(s.title) || /attractions/i.test(s.title)
  );
  const nonItinerarySections = sections.filter(
    (s) => !(/itinerary/i.test(s.title) || /attractions/i.test(s.title))
  );
  const screens = [nonItinerarySections, itinerarySections];

  function renderSection(
    section: { title: string; content: string },
    idx: number
  ) {
    // Assign emoji based on section title
    let emoji = sectionEmojis[section.title] || "📄";
    if (/^Day \d+/i.test(section.title)) emoji = "🗓️";
    else if (/plan|summary|vacation|trip/i.test(section.title)) emoji = "🧳";
    else if (/weather/i.test(section.title)) emoji = "🌤️";
    else if (/flight/i.test(section.title)) emoji = "✈️";
    else if (/hotel|stay/i.test(section.title)) emoji = "🏨";
    else if (/date/i.test(section.title)) emoji = "📅";
    else if (/budget|cost|price/i.test(section.title)) emoji = "💰";
    else if (/currency/i.test(section.title)) emoji = "💱";
    else if (/itinerary|attraction/i.test(section.title)) emoji = "🗺️";
    else if (/restaurant/i.test(section.title)) emoji = "🍽️";
    else if (/transport/i.test(section.title)) emoji = "🚗";
    else if (/check-in/i.test(section.title)) emoji = "🛎️";
    else if (/check-out/i.test(section.title)) emoji = "🏁";
    return (
      <div key={idx} className="mb-6">
        <div className="font-bold text-lg flex items-center gap-2 mb-2 text-blue-800 dark:text-blue-200">
          <span>{emoji}</span>
          <span>{section.title}</span>
        </div>
        <div className="whitespace-pre-line text-sm leading-relaxed text-left">
          {section.content.replace(/\*\*/g, "").trim()}
        </div>
      </div>
    );
  }

  return (
    <CardContent className="mt-6">
      {screens[page].length > 0 ? (
        screens[page].map(renderSection)
      ) : (
        <div className="whitespace-pre-line text-sm text-left">
          {summary.replace(/\*\*/g, "")}
        </div>
      )}
      {screens[1].length > 0 && (
        <div className="flex justify-center gap-4 mt-4">
          <button
            type="button"
            className="px-4 py-2 rounded bg-muted text-foreground font-medium disabled:opacity-50"
            onClick={() => setPage(0)}
            disabled={page === 0}
          >
            Previous
          </button>
          <button
            type="button"
            className="px-4 py-2 rounded bg-muted text-foreground font-medium disabled:opacity-50"
            onClick={() => setPage(1)}
            disabled={page === 1}
          >
            Next
          </button>
        </div>
      )}
    </CardContent>
  );
};

export default SummaryDisplay;
