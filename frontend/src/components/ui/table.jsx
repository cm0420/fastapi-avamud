import React from 'react';
import { cn } from './utils';

const Table = ({ className, ...props }) => {
  return (
    <div className="relative w-full overflow-auto">
      <table
        className={cn("w-full caption-bottom text-sm", className)}
        {...props}
      />
    </div>
  );
};

const TableHeader = ({ className, ...props }) => {
  return (
    <thead className={cn("[&_tr]:border-b", className)} {...props} />
  );
};

const TableBody = ({ className, ...props }) => {
  return (
    <tbody
      className={cn("[&_tr:last-child]:border-0", className)}
      {...props}
    />
  );
};

const TableRow = ({ className, ...props }) => {
  return (
    <tr
      className={cn(
        "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
        className
      )}
      {...props}
    />
  );
};

const TableHead = ({ className, ...props }) => {
  return (
    <th
      className={cn(
        "h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0",
        className
      )}
      {...props}
    />
  );
};

const TableCell = ({ className, ...props }) => {
  return (
    <td
      className={cn("p-4 align-middle [&:has([role=checkbox])]:pr-0", className)}
      {...props}
    />
  );
};

export {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
};