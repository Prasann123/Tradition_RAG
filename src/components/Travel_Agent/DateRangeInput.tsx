import React from "react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";

interface Props {
  start_date: string;
  return_date: string;
  onStartChange: (value: string) => void;
  onReturnChange: (value: string) => void;
}

const DateRangeInput: React.FC<Props> = ({
  start_date,
  return_date,
  onStartChange,
  onReturnChange,
}) => (
  <div className="flex gap-4">
    <div className="flex-1">
      <Label className="mb-2">Start Date</Label>
      <Input
        type="date"
        value={start_date}
        onChange={(e) => onStartChange(e.target.value)}
      />
    </div>
    <div className="flex-1">
      <Label className="mb-2">Return Date</Label>
      <Input
        type="date"
        value={return_date}
        onChange={(e) => onReturnChange(e.target.value)}
      />
    </div>
  </div>
);

export default DateRangeInput;
