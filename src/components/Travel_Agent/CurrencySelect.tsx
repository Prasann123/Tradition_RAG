import React from "react";
import { Label } from "../ui/label";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "..//ui/select";

interface Currency {
  label: string;
  value: string;
}

interface Props {
  value: string;
  onChange: (value: string) => void;
  currencies: Currency[];
}

const CurrencySelect: React.FC<Props> = ({ value, onChange, currencies }) => (
  <div>
    <Label className="mb-2">Currency</Label>
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger>
        <SelectValue placeholder="Select currency" />
      </SelectTrigger>
      <SelectContent>
        {currencies.map((c) => (
          <SelectItem key={c.value} value={c.value}>
            {c.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  </div>
);

export default CurrencySelect;
