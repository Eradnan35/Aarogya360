"use client";

import React from "react";
import { useLiveQueue } from "@/hooks/use-dashboard";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";

export default function LiveQueue() {
  const { data: queue, isLoading } = useLiveQueue();

  return (
    <Card className="border-border shadow-sm bg-card overflow-hidden flex flex-col justify-between h-[380px]">
      {/* Title Header Section */}
      <div className="px-6 py-4 border-b border-border flex justify-between items-center shrink-0 select-none">
        <h4 className="font-bold text-lg text-foreground">Live Patient Queue</h4>
        <span className="px-2 py-0.5 bg-primary/10 text-primary text-[10px] font-black uppercase tracking-wider rounded-md animate-pulse">
          Live Now
        </span>
      </div>

      {/* Table Section */}
      <div className="flex-grow overflow-y-auto no-scrollbar">
        {isLoading ? (
          <div className="p-6 space-y-4">
            {Array.from({ length: 3 }).map((_, idx) => (
              <div key={idx} className="h-10 bg-surface-low rounded-lg animate-pulse" />
            ))}
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead>Queue ID</TableHead>
                <TableHead>Patient Name</TableHead>
                <TableHead>Doctor</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Waiting Time</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {queue?.map((item) => (
                <TableRow key={item.queueId} className="cursor-pointer">
                  <TableCell className="font-bold">{item.queueId}</TableCell>
                  <TableCell className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-surface-container-high text-foreground flex items-center justify-center text-[11px] font-bold shrink-0">
                      {item.patientInitials}
                    </div>
                    <span className="font-semibold text-sm">{item.patientName}</span>
                  </TableCell>
                  <TableCell className="text-muted-foreground font-medium">{item.doctorName}</TableCell>
                  <TableCell>
                    <Badge 
                      variant={
                        item.status === "Consulting" ? "warning" :
                        item.status === "Next Up" ? "success" : "default"
                      }
                      className="text-[10px] px-2 py-0.5"
                    >
                      {item.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right font-semibold text-muted-foreground">{item.waitingTime}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </Card>
  );
}
