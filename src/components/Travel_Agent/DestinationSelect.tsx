import React from "react";
import { Label } from "../ui/label";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "../ui/select";

interface Destination {
  label: string;
  value: string;
  from: string;
  to: string;
}

interface Props {
  value: string;
  onChange: (value: string) => void;
  destinations: Destination[];
}

const DestinationSelect: React.FC<Props> = ({
  value,
  onChange,
  destinations,
}) => (
  <div>
    <Label className="mb-2">Destination</Label>
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger>
        <SelectValue placeholder="Select destination" />
      </SelectTrigger>
      <SelectContent>
        {destinations.map((d) => (
          <SelectItem key={d.value} value={d.value}>
            {d.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  </div>
);

export default DestinationSelect;
