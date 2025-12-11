"use client";

import { useEffect, useRef } from "react";
import { useChatStore } from "@/lib/store";
import { ChatMessage } from "@/components/chat/ChatMessage";
import { InputArea } from "@/components/chat/InputArea";
import { Sparkles, History, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const { messages, isLoading, startResearchSession } = useChatStore();
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, messages[messages.length - 1]?.content]);

  return (
    <div className="flex flex-col min-h-screen aurora-bg font-sans selection:bg-primary/20">
      {/* Header */}
      <header className="sticky top-0 z-50 h-16 border-b border-white/5 bg-black/20 backdrop-blur-xl supports-[backdrop-filter]:bg-black/20">
        <div className="container mx-auto max-w-5xl px-4 h-full flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative h-9 w-9 flex items-center justify-center rounded-xl bg-gradient-to-tr from-primary to-purple-600 shadow-lg shadow-primary/20">
              <Sparkles className="h-5 w-5 text-white" />
              <div className="absolute inset-0 bg-white/20 rounded-xl animate-pulse" />
            </div>
            <div>
              <h1 className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60 tracking-tight">
                Agentic Research
              </h1>
              <p className="text-[10px] text-muted-foreground font-mono uppercase tracking-widest -mt-1">
                BVA507E Project
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* ITU Logo */}
            <div className="h-10 w-10 relative overflow-hidden bg-white rounded-md">
              <img src="/itu-logo.jpg" alt="ITU" className="h-full w-full object-contain" />
            </div>
            <Button variant="ghost" size="icon" className="text-white/60 hover:text-white hover:bg-white/10">
              <History className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 w-full relative">
        <div className="container mx-auto max-w-5xl px-4 py-8 pb-48 min-h-full">
          <AnimatePresence mode="wait">
            {messages.length === 0 ? (
              // Empty State Hero
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="flex flex-col items-center justify-center min-h-[60vh] text-center space-y-8"
              >
                <div className="relative group">
                  <div className="absolute -inset-1 bg-gradient-to-r from-primary to-purple-600 rounded-full blur opacity-40 group-hover:opacity-75 transition duration-1000" />
                  <div className="relative h-24 w-24 rounded-full bg-black/50 backdrop-blur-md flex items-center justify-center border border-white/10 shadow-2xl">
                    <Sparkles className="h-12 w-12 text-primary" />
                  </div>
                </div>

                <div className="space-y-4 max-w-2xl">
                  <h2 className="text-4xl md:text-6xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-white via-white/80 to-white/40">
                    Uncover the Unknown.
                  </h2>
                  <p className="text-lg md:text-xl text-muted-foreground/80 leading-relaxed font-light">
                    Autonomous Multi-Agent Research System
                    <br className="hidden md:block" />
                    Business Analytics for Managers (BVA507E)
                  </p>
                </div>

                {/* Quick Prompts */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-lg">
                  {["Latest AI Developments this week", "Market Analysis of EVs 2025", "Impact of Quantum Computing on Finance"].map((text, i) => (
                    <button
                      key={i}
                      onClick={() => startResearchSession(text, { depth: 'deep', tone: 'professional' })}
                      className="px-4 py-3 text-sm text-left bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 rounded-xl transition-all hover:scale-[1.02] text-white/80"
                    >
                      <span className="text-primary opacity-50 mr-2">/</span>
                      {text}
                    </button>
                  ))}
                </div>
              </motion.div>
            ) : (
              // Chat Thread
              <div className="space-y-6">
                {messages.map((msg) => (
                  <ChatMessage key={msg.id} message={msg} />
                ))}
                <div ref={bottomRef} />
              </div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Input Area (Sticky) */}
      <div className="fixed bottom-0 left-0 right-0 z-40 bg-gradient-to-t from-black via-black/80 to-transparent pt-10 pb-2">
        <div className="container mx-auto max-w-5xl px-4">
          <InputArea onSend={startResearchSession} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}
