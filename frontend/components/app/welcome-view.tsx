"use client";

import React, { useState } from "react";
import { Button } from "@/components/livekit/button";

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ...divProps
}: React.ComponentProps<"div"> & WelcomeViewProps) => {
  const [name, setName] = useState("");

  const handleStart = () => {
    // Say your name into the voice after connecting
    onStartCall();
  };

  return (
    <div
      {...divProps}
      className="min-h-screen w-full flex flex-col items-center justify-center px-6 py-10
                 bg-gradient-to-br from-gray-950 via-red-950 to-black text-red-50"
    >
      {/* Badge */}
      <div className="mb-6 inline-block bg-red-900/30 px-4 py-2 rounded-full border border-red-600/50">
        <p className="text-[11px] tracking-[0.35em] uppercase text-red-400 font-bold">
          ⚠️ Welcome to the Games · Squid Game Edition ⚠️
        </p>
      </div>

      {/* Header */}
      <div className="max-w-2xl text-center space-y-4 mb-10">
        <h1 className="text-5xl md:text-7xl font-black tracking-tight">
          <span className="bg-gradient-to-r from-red-500 via-red-600 to-red-700 bg-clip-text text-transparent">
            IMPROV BATTLE
          </span>
        </h1>
        <h2 className="text-2xl md:text-3xl font-bold text-red-300">
          Squid Game Edition
        </h2>
        <p className="text-sm md:text-base text-gray-300 leading-relaxed">
          You are the contestant. The AI host sets the scene. You must step into character 
          and perform three intense improvisation scenarios. The host will react—sometimes 
          with praise, sometimes with critique. Commit fully and discover what kind of improviser you truly are.
        </p>
      </div>

      {/* Symbols */}
      <div className="flex justify-center gap-6 mb-10">
        <div className="w-10 h-10 rounded-full bg-red-600 shadow-lg shadow-red-600/50 animate-pulse"></div>
        <div className="w-10 h-10 rounded bg-red-600 shadow-lg shadow-red-600/50 animate-pulse" style={{ animationDelay: '0.2s' }}></div>
        <div className="w-10 h-10 bg-red-600 shadow-lg shadow-red-600/50 animate-pulse" style={{ clipPath: 'polygon(50% 0%, 100% 100%, 0% 100%)', animationDelay: '0.4s' }}></div>
      </div>

      {/* Join card */}
      <div className="w-full max-w-md bg-gray-900/70 border border-red-900/50 rounded-3xl p-8 shadow-xl backdrop-blur">
        <h3 className="text-xl font-bold text-red-400 mb-6 text-center">
          Join the Games as a Contestant
        </h3>

        <label className="flex flex-col gap-3 text-left mb-6">
          <span className="text-xs font-bold text-red-300 uppercase tracking-wide">
            Contestant Name
          </span>
          <input
            type="text"
            placeholder="What should the host call you?"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-2xl border border-red-900/50 bg-gray-800/50 px-4 py-3 text-sm
                       text-white placeholder-gray-500 outline-none 
                       focus:border-red-600 focus:ring-2 focus:ring-red-600/30 
                       transition duration-200"
          />
          <span className="text-[11px] text-gray-400">
            💡 Tip: Say your name when the host greets you to lock it in officially.
          </span>
        </label>

        <Button
          onClick={handleStart}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-red-600 to-red-700 
                     hover:from-red-700 hover:to-red-800 text-white font-bold text-lg
                     uppercase tracking-wider shadow-lg shadow-red-600/50
                     transition transform hover:scale-105 active:scale-95"
        >
          {startButtonText || "START IMPROV BATTLE"}
        </Button>

        <div className="mt-6 p-4 bg-red-900/20 rounded-lg border border-red-900/30">
          <p className="text-xs text-red-300/80 leading-relaxed">
            <span className="font-bold text-red-400">⚡ Remember:</span> You will face 3 intense scenarios. 
            Commit fully to your character. When done, say "end scene" to proceed.
          </p>
        </div>
      </div>

      {/* Footer tips */}
      <div className="mt-8 max-w-xl text-center text-[11px] md:text-xs text-gray-400 space-y-2 border-t border-red-900/30 pt-6">
        <p>
          🎤 <span className="text-red-400">Say "end scene"</span> when you finish your improv.
        </p>
        <p>
          🛑 <span className="text-red-400">Say "stop game" or "end show"</span> at any time to exit early.
        </p>
        <p>
          🎭 The host will judge your performance and move to the next scenario.
        </p>
      
      </div>
    </div>
  );
};

export default WelcomeView;