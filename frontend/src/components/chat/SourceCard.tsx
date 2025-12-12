"use client";

import { Globe } from "lucide-react";
import { Finding } from "@/types/research";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";

export const SourceCard = ({ source }: { source: Finding }) => {
    let domain = 'Unknown Source';
    let faviconUrl = '';

    try {
        if (source.url) {
            const urlObj = new URL(source.url);
            domain = urlObj.hostname.replace('www.', '');
            faviconUrl = `https://www.google.com/s2/favicons?domain=${domain}&sz=64`;
        }
    } catch (e) {
        domain = source.source || 'Source';
    }

    return (
        <motion.a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.02, y: -2 }}
            className="block group"
        >
            <Card className="h-full bg-background/40 hover:bg-background/60 border-white/5 hover:border-primary/20 transition-colors overflow-hidden group-hover:shadow-md group-hover:shadow-primary/5">
                <CardContent className="p-3 flex flex-col gap-2 h-full">
                    <div className="flex items-center gap-2">
                        {source.url ? (
                            <img
                                src={faviconUrl}
                                alt=""
                                className="w-4 h-4 rounded-sm opacity-70 group-hover:opacity-100 transition-opacity"
                                onError={(e) => e.currentTarget.style.display = 'none'}
                            />
                        ) : <Globe className="w-4 h-4 text-muted-foreground" />}

                        <span className="text-xs text-muted-foreground font-medium truncate flex-1 group-hover:text-primary transition-colors">
                            {domain}
                        </span>
                    </div>

                    <p className="text-xs text-foreground/80 line-clamp-3 leading-relaxed">
                        {source.content || source.raw_content.slice(0, 150)}...
                    </p>
                </CardContent>
            </Card>
        </motion.a>
    );
};
