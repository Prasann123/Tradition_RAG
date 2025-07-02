import React from "react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";

interface Props {
  value: number;
  onChange: (value: number) => void;
}

const AdultsInput: React.FC<Props> = ({ value, onChange }) => (
  <div>
    <Label className="mb-2">Adults</Label>
    <Input
      type="number"
      min={1}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
    />
  </div>
);

export default AdultsInput;
