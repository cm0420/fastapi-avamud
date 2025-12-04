import React from "react";
import { cn } from "./utils";

export function Select({ value, onValueChange, children, ...props }) {
  return (
    <div className="relative">
      <select
        value={value}
        onChange={(e) => onValueChange?.(e.target.value)}
        className={cn(
          "flex h-9 w-full rounded-md border border-gray-300 bg-white px-3 py-1 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50",
        )}
        {...props}
      >
        {children}
      </select>
    </div>
  );
}

export function SelectTrigger({ className, children, ...props }) {
  return children;
}

export function SelectContent({ children, ...props }) {
  return children;
}

export function SelectItem({ value, children, ...props }) {
  return (
    <option value={value} {...props}>
      {children}
    </option>
  );
}

export function SelectValue({ placeholder, ...props }) {
  return (
    <option value="" disabled>
      {placeholder}
    </option>
  );
}
