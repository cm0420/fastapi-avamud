import React from "react";
import { cn } from "./utils";

const buttonVariants = {
  default: "bg-blue-600 text-white hover:bg-blue-700",
  destructive: "bg-red-600 text-white hover:bg-red-700",
  outline: "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50",
  secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
  ghost: "hover:bg-gray-100 text-gray-700",
  link: "text-blue-600 underline-offset-4 hover:underline",
};

const buttonSizes = {
  default: "h-9 px-4 py-2",
  sm: "h-8 px-3 text-sm",
  lg: "h-10 px-6",
  icon: "h-9 w-9",
};

export function Button({ 
  className, 
  variant = "default", 
  size = "default", 
  ...props 
}) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50",
        buttonVariants[variant],
        buttonSizes[size],
        className
      )}
      {...props}
    />
  );
}
