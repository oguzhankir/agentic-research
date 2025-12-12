"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, User, Copy, Check, ChevronDown, ChevronUp, Download } from "lucide-react";
import { ChatMessage as ChatMessageType } from "@/types/research";
import { cn } from "@/lib/utils";
import { ThinkingIndicator } from "./ThinkingIndicator";
import { SourceCard } from "./SourceCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export const ChatMessage = ({ message }: { message: ChatMessageType }) => {
    const isUser = message.type === 'user';
    const [sourcesExpanded, setSourcesExpanded] = useState(false);
    const [copied, setCopied] = useState(false);

    // Auto-expand sources if there are few
    const sources = message.sources || [];

    const handleCopy = () => {
        navigator.clipboard.writeText(message.content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const handleDownload = () => {
        if (!message.researchState?.html_output) return;
        const blob = new Blob([message.researchState.html_output], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `agentic-report-${new Date().toISOString().split('T')[0]}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
                "flex gap-4 md:gap-6 w-full max-w-4xl mx-auto py-6 group",
                isUser ? "flex-row-reverse" : "flex-row"
            )}
        >
            {/* Avatar */}
            <div className={cn(
                "flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-lg border shadow-sm",
                isUser
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-muted text-foreground border-border bg-gradient-to-b from-white/10 to-transparent"
            )}>
                {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
            </div>

            <div className={cn("flex-1 space-y-4 overflow-hidden", isUser ? "items-end" : "items-start")}>
                {/* Thinking State (Assistant Only) */}
                {!isUser && message.isThinking && (
                    <ThinkingIndicator state={message.researchState} />
                )}

                {/* Message Content */}
                {message.content && (
                    <div className={cn(
                        "relative text-sm md:text-base leading-relaxed max-w-none",
                        isUser
                            ? "bg-primary text-primary-foreground px-5 py-3.5 rounded-2xl rounded-tr-sm ml-auto w-fit shadow-md"
                            : "prose prose-invert prose-p:leading-7 prose-pre:bg-background/50 prose-pre:border prose-pre:border-white/10"
                    )}>
                        {!isUser ? (
                            <ReactMarkdown
                                remarkPlugins={[remarkGfm]}
                                rehypePlugins={[rehypeHighlight]}
                                components={{
                                    a: (props) => <a {...props} target="_blank" className="text-primary hover:underline font-medium" />
                                }}
                            >
                                {message.content}
                            </ReactMarkdown>
                        ) : (
                            <p className="whitespace-pre-wrap">{message.content}</p>
                        )}

                        {/* Copy Button (Assistant) */}
                        {!isUser && (
                            <div className="absolute -bottom-8 left-0 opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                                <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground" onClick={handleCopy}>
                                    {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                                </Button>
                            </div>
                        )}
                    </div>
                )}

                {/* Sources Grid */}
                {!isUser && sources.length > 0 && (
                    <div className="mt-4 animate-in fade-in slide-in-from-bottom-2">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setSourcesExpanded(!sourcesExpanded)}
                            className="gap-2 h-8 text-xs bg-background/50 backdrop-blur-sm border-white/10 hover:bg-white/5"
                        >
                            {sourcesExpanded ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
                            {sourcesExpanded ? 'Hide Sources' : `View ${sources.length} Sources`}
                        </Button>

                        <AnimatePresence>
                            {sourcesExpanded && (
                                <motion.div
                                    initial={{ height: 0, opacity: 0 }}
                                    animate={{ height: "auto", opacity: 1 }}
                                    exit={{ height: 0, opacity: 0 }}
                                    className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 mt-3 overflow-hidden"
                                >
                                    {sources.map((source, i) => (
                                        <SourceCard key={i} source={source} />
                                    ))}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                )}

                {/* Download Report Action */}
                {!isUser && message.researchState?.html_output && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="pt-2">
                        <Button
                            onClick={handleDownload}
                            className="gap-2 bg-emerald-600/20 text-emerald-500 hover:bg-emerald-600/30 border-emerald-600/20"
                            variant="outline"
                        >
                            <Download className="h-4 w-4" />
                            Download Full Interactive Report
                        </Button>
                    </motion.div>
                )}
            </div>
        </motion.div>
    );
};
