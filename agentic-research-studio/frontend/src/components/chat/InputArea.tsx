"use client";

import { useState, useRef, useEffect } from "react";
import { ArrowUp, Globe, FileText, Sparkles, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { Customization } from "@/types/research";
import { Badge } from "@/components/ui/badge";

interface InputAreaProps {
    onSend: (message: string, customization: Customization) => void;
    isLoading: boolean;
}

export const InputArea = ({ onSend, isLoading }: InputAreaProps) => {
    const [input, setInput] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const [customization, setCustomization] = useState<Customization>({
        depth: 'comprehensive',
        tone: 'professional'
    });

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const handleSubmit = () => {
        if (!input.trim() || isLoading) return;
        onSend(input, customization);
        setInput("");
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    const toggleDepth = () => {
        setCustomization(prev => ({
            ...prev,
            depth: prev.depth === 'deep' ? 'basic' : 'deep'
        }));
    };

    const toggleTone = () => {
        setCustomization(prev => ({
            ...prev,
            tone: prev.tone === 'professional' ? 'academic' : 'professional'
        }));
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-4 pb-8">
            <div className="relative group">
                {/* Animated Glow Border */}
                <div className="absolute -inset-0.5 bg-gradient-to-r from-primary/30 via-purple-500/30 to-primary/30 rounded-3xl opacity-20 group-focus-within:opacity-100 transition duration-500 blur-md" />

                <div className="relative flex flex-col gap-2 bg-background/80 backdrop-blur-xl border border-white/10 rounded-3xl p-3 shadow-2xl transition-all">
                    <Textarea
                        ref={textareaRef}
                        value={input}
                        onChange={(e) => {
                            setInput(e.target.value);
                            e.target.style.height = 'auto';
                            e.target.style.height = `${Math.min(e.target.scrollHeight, 200)}px`;
                        }}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask anything... (e.g. 'Future of Quantum Computing')"
                        className="min-h-[50px] max-h-[200px] border-none shadow-none resize-none bg-transparent text-base focus-visible:ring-0 scrollbar-hide py-3 md:text-lg text-foreground placeholder:text-muted-foreground/50"
                        disabled={isLoading}
                    />

                    <div className="flex items-center justify-between px-2 pb-1">
                        <div className="flex items-center gap-2">
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={toggleDepth}
                                className={cn(
                                    "h-8 rounded-full text-xs gap-1.5 transition-colors border border-transparent",
                                    customization.depth === 'deep' ? "bg-primary/10 text-primary border-primary/20" : "text-muted-foreground hover:bg-white/5"
                                )}
                            >
                                <Globe className="h-3 w-3" />
                                {customization.depth === 'deep' ? 'Deep Search' : 'Quick Search'}
                            </Button>

                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={toggleTone}
                                className={cn(
                                    "h-8 rounded-full text-xs gap-1.5 transition-colors border border-transparent sm:flex hidden",
                                    customization.tone === 'academic' ? "bg-purple-500/10 text-purple-400 border-purple-500/20" : "text-muted-foreground hover:bg-white/5"
                                )}
                            >
                                <FileText className="h-3 w-3" />
                                {customization.tone === 'academic' ? 'Academic' : 'Pro'}
                            </Button>
                        </div>

                        <Button
                            onClick={handleSubmit}
                            disabled={!input.trim() || isLoading}
                            size="icon"
                            className={cn(
                                "h-9 w-9 rounded-xl transition-all duration-300",
                                input.trim()
                                    ? "bg-primary text-primary-foreground shadow-lg shadow-primary/25 hover:scale-105"
                                    : "bg-muted text-muted-foreground opacity-50"
                            )}
                        >
                            {isLoading ? (
                                <Sparkles className="h-4 w-4 animate-spin" />
                            ) : (
                                <ArrowUp className="h-4 w-4" />
                            )}
                        </Button>
                    </div>
                </div>

                <div className="text-center mt-3">
                    <p className="text-[10px] text-muted-foreground/40 font-mono tracking-widest uppercase">
                        Agentic Research Studio v2.0
                    </p>
                </div>
            </div>
        </div>
    );
};
