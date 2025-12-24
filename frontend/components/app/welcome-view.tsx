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
                 bg-gradient-to-br from-green-950 via-slate-900 to-gray-900 text-green-50"
    >
      {/* Badge */}
      <div className="mb-6 inline-block bg-green-900/30 px-4 py-2 rounded-full border border-green-600/50">
        <p className="text-[11px] tracking-[0.35em] uppercase text-green-400 font-bold">
          🌿 Wellness Companion 🌿
        </p>
      </div>

      {/* Header */}
      <div className="max-w-2xl text-center space-y-4 mb-10">
        <h1 className="text-5xl md:text-7xl font-black tracking-tight">
          <span className="bg-gradient-to-r from-green-500 via-green-600 to-green-700 bg-clip-text text-transparent whitespace-nowrap">
            WELLNESS CHECK-IN
          </span>
        </h1>
        <h2 className="text-2xl md:text-3xl font-bold text-green-300">
          Health & Wellness Voice Companion
        </h2>
        <p className="text-sm md:text-base text-gray-300 leading-relaxed">
          Welcome to your daily wellness check-in. Our AI companion will help you track your mood, set goals, and maintain your well-being. 
          Share how you're feeling today and let's work together on your health journey. 
          Your wellness is our priority.
        </p>
      </div>

      {/* Symbols */}
      <div className="flex justify-center gap-6 mb-10">
        <div className="w-10 h-10 rounded-full bg-green-600 shadow-lg shadow-green-600/50 animate-pulse flex items-center justify-center text-white font-bold">🌿</div>
        <div className="w-10 h-10 rounded bg-green-600 shadow-lg shadow-green-600/50 animate-pulse flex items-center justify-center text-white font-bold" style={{ animationDelay: '0.2s' }}>🧘‍♀️</div>
        <div className="w-10 h-10 bg-green-600 shadow-lg shadow-green-600/50 animate-pulse flex items-center justify-center text-white font-bold" style={{ clipPath: 'polygon(50% 0%, 100% 100%, 0% 100%)', animationDelay: '0.4s' }}>💚</div>
      </div>

      {/* Wellness Tips */}
      <div className="max-w-xl text-center text-sm text-gray-300 space-y-3 mb-10 bg-green-900/10 rounded-2xl p-6 border border-green-900/20">
        <h4 className="text-green-400 font-semibold mb-4">Your Wellness Journey Starts Here</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <p className="flex items-center gap-2">
            🌿 <span>Share your current mood</span>
          </p>
          <p className="flex items-center gap-2">
            🎯 <span>Set 1-3 achievable goals</span>
          </p>
          <p className="flex items-center gap-2">
            📝 <span>Review your progress</span>
          </p>
          <p className="flex items-center gap-2">
            💚 <span>Take it one step at a time</span>
          </p>
        </div>
      </div>

      {/* Join card */}
      <div className="w-full max-w-md bg-gray-900/70 border border-green-900/50 rounded-3xl p-8 shadow-xl backdrop-blur">
        <h3 className="text-xl font-bold text-green-400 mb-6 text-center">
          Connect with Wellness Companion
        </h3>

        <label className="flex flex-col gap-3 text-left mb-6">
          <span className="text-xs font-bold text-green-300 uppercase tracking-wide">
            Your Name
          </span>
          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-2xl border border-green-900/50 bg-gray-800/50 px-4 py-3 text-sm
                       text-white placeholder-gray-500 outline-none 
                       focus:border-green-600 focus:ring-2 focus:ring-green-600/30 
                       transition duration-200"
          />
        </label>

        <Button
          onClick={handleStart}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-green-600 to-green-700 
                     hover:from-green-700 hover:to-green-800 text-white font-bold text-lg
                     uppercase tracking-wider shadow-lg shadow-green-600/50
                     transition transform hover:scale-105 active:scale-95"
        >
          {startButtonText || "START WELLNESS SESSION"}
        </Button>

        <div className="mt-6 p-4 bg-green-900/20 rounded-lg border border-green-900/30">
          <p className="text-xs text-green-300/80 leading-relaxed">
            <span className="font-bold text-green-400">🌿 Remember:</span> Take a moment to reflect on your mood and goals. 
            Your wellness journey starts with honest self-assessment.
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeView;