import React from "react";
import { Card } from "../ui/card";

interface ToolMessagesSummaryProps {
  messages: Array<{
    tool_name?: string;
    role?: string;
    content?: string;
    result?: string | number | object;
    summary?: string;
  }>;
}

function renderToolMarkdown(text: string) {
  if (!text) return "";
  return text
    .replace(
      /^#### (.*)$/gm,
      '<h4 class="font-bold text-base mt-2 mb-1">$1</h4>'
    )
    .replace(/^### (.*)$/gm, '<h3 class="font-bold text-lg mt-2 mb-1">$1</h3>')
    .replace(/^## (.*)$/gm, '<h2 class="font-bold text-xl mt-2 mb-1">$1</h2>')
    .replace(/^# (.*)$/gm, '<h1 class="font-bold text-2xl mt-2 mb-1">$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(
      /(^|<br \/?>)\s*- (.*?)(?=<br \/?>|$)/g,
      '$1<li class="ml-4 list-disc">$2</li>'
    )
    .replace(/((<li[\s\S]*?<\/li>)+)/g, '<ul class="mb-2">$1</ul>')
    .replace(/\n/g, "<br />");
}

const ToolMessagesSummary: React.FC<ToolMessagesSummaryProps> = ({
  messages,
}) => {
  if (!messages || messages.length === 0) {
    return (
      <Card className="p-4 mb-4 bg-muted/40 w-full md:w-[420px] overflow-x-auto max-h-[70vh]">
        <div className="font-semibold text-base mb-2 text-left">
          Tool Messages
        </div>
        <div className="text-muted-foreground text-sm text-left">
          No tool messages available.
        </div>
      </Card>
    );
  }
  return (
    <Card className="p-4 mb-4 bg-muted/40 w-full md:w-[420px] overflow-x-auto max-h-[70vh]">
      <div className="font-semibold text-base mb-2 text-left">
        Tool Messages
      </div>
      <div className="space-y-3">
        {messages.map((msg, idx) => (
          <div key={idx} className="border-b pb-2 last:border-b-0 text-left">
            <div className="font-medium text-sm mb-1">
              <span className="text-gray-500">{msg.role}</span>
              {msg.tool_name && (
                <span className="ml-2 text-blue-700 dark:text-blue-300">
                  [{msg.tool_name}]
                </span>
              )}
            </div>
            {msg.content && (
              <div
                className="text-xs whitespace-pre-line mb-1"
                dangerouslySetInnerHTML={{
                  __html: renderToolMarkdown(msg.content),
                }}
              />
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ToolMessagesSummary;
