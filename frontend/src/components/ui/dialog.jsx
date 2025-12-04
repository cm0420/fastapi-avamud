import React from 'react';
import { X } from 'lucide-react';
import { cn } from './utils';

const Dialog = ({ open, onOpenChange, children }) => {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="fixed inset-0 bg-black/50"
        onClick={() => onOpenChange(false)}
      />
      <div className="relative z-50">{children}</div>
    </div>
  );
};

const DialogContent = ({ className, children, ...props }) => {
  return (
    <div
      className={cn(
        "bg-white rounded-lg shadow-lg p-6 w-full max-w-lg max-h-[85vh] overflow-y-auto",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

const DialogHeader = ({ className, children, ...props }) => {
  return (
    <div className={cn("mb-4", className)} {...props}>
      {children}
    </div>
  );
};

const DialogTitle = ({ className, children, ...props }) => {
  return (
    <h2
      className={cn("text-lg font-semibold text-gray-900", className)}
      {...props}
    >
      {children}
    </h2>
  );
};

const DialogDescription = ({ className, children, ...props }) => {
  return (
    <p className={cn("text-sm text-gray-600 mt-1", className)} {...props}>
      {children}
    </p>
  );
};

export { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription };