"use client";

import { motion } from "framer-motion";
import { Cpu, Search, Terminal, Loader2 } from "lucide-react";
import { ResearchState } from "@/types/research";

export const ThinkingIndicator = ({ state }: { state?: ResearchState }) => {
    const logs = state?.progress_updates || [];
    const lastLog = logs[logs.length - 1] || "Initializing agent swarm...";

    const isAnalyzing = lastLog.toLowerCase().includes('analyzing') || lastLog.toLowerCase().includes('technical');
    const isWriting = lastLog.toLowerCase().includes('synthesizing') || lastLog.toLowerCase().includes('report');

    return (
        <div className="w-full max-w-md my-4">
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="relative overflow-hidden rounded-xl border border-primary/20 bg-background/50 backdrop-blur-md p-4 shadow-lg shadow-primary/5"
            >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/5 to-transparent w-[200%] animate-shimmer pointer-events-none" />

                <div className="flex items-start gap-4 relative z-10">
                    <div className="relative flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
                        {isWriting ? (
                            <Terminal className="h-5 w-5 text-primary animate-pulse" />
                        ) : isAnalyzing ? (
                            <Cpu className="h-5 w-5 text-primary animate-pulse" />
                        ) : (
                            <Search className="h-5 w-5 text-primary animate-pulse" />
                        )}

                        <div className="absolute -bottom-1 -right-1 flex gap-0.5">
                            {[0, 1, 2].map((i) => (
                                <motion.span
                                    key={i}
                                    className="h-1 w-1 rounded-full bg-primary"
                                    animate={{ opacity: [0.3, 1, 0.3] }}
                                    transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
                                />
                            ))}
                        </div>
                    </div>

                    <div className="flex-1 space-y-2 min-w-0">
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-semibold text-primary">
                                {isWriting ? 'Synthesizing Intelligence' :
                                    isAnalyzing ? 'Analyzing Data Patterns' :
                                        'Deep Research Active'}
                            </span>
                            <span className="text-xs font-mono text-muted-foreground tabular-nums">
                                {logs.length > 0 ? `${Math.min(logs.length * 5, 99)}%` : '0%'}
                            </span>
                        </div>

                        {/* Progress Bar */}
                        <div className="h-1.5 w-full bg-primary/10 rounded-full overflow-hidden">
                            <motion.div
                                className="h-full bg-primary shadow-[0_0_10px_rgba(var(--primary),0.5)]"
                                initial={{ width: "0%" }}
                                animate={{ width: `${Math.min(logs.length * 5, 100)}%` }}
                                transition={{ type: "spring", stiffness: 40 }}
                            />
                        </div>

                        <div className="flex items-center gap-2">
                            <Loader2 className="h-3 w-3 animate-spin text-muted-foreground" />
                            <p className="text-xs text-muted-foreground font-mono truncate">
                                {lastLog}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Collapsible Terminal Logs */}
                {logs.length > 0 && (
                    <div className="mt-3 border-t border-white/5 pt-3">
                        <div className="flex flex-col gap-1 max-h-32 overflow-y-auto scrollbar-hide font-mono text-[10px] text-muted-foreground/80">
                            {logs.map((log, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    className="flex gap-2"
                                >
                                    <span className="text-primary/40 text-[9px] shrink-0 pt-0.5">{`>`}</span>
                                    <span>{log}</span>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                )}
            </motion.div>
        </div>
    );
};
