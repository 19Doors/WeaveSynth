"use client";
import { AlignLeft, RefreshCw } from "lucide-react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { TextPlugin } from "gsap/TextPlugin";
import { ScrambleTextPlugin } from "gsap/ScrambleTextPlugin";
import { useRef } from "react";

export function Navbar() {
  return (
    <div className="flex w-full justify-between items-center">
      <AlignLeft
        color="#2D2D34"
        size={18}
        strokeWidth={2.5}
        className="cursor-pointer"
      />
      <a className="font-instrument text-xl" href="/">
        WeaveSynth
      </a>
      <RefreshCw size={16} color="#2D2D34" className="cursor-pointer" />
    </div>
  );
}

export function NavbarNo() {
  return (
    <div className="flex w-full justify-center items-center">
      <a className="font-instrument text-xl" href="/">
        WeaveSynth
      </a>
    </div>
  );
}

export function Loading() {
  gsap.registerPlugin(useGSAP, TextPlugin, ScrambleTextPlugin);
  const loadingText = useRef(null);
  useGSAP(() => {
    gsap.to(loadingText.current, {
      duration: 2.0,
      scrambleText: {
        text: "LOADING",
        chars: "XO123",
        speed: 0.3,
      },
      ease: "sine.out",
    });
  });
  return (
    <div className="w-full h-screen flex items-center justify-center">
      <p ref={loadingText} className="font-bold font-spaceG text-4xl"></p>
    </div>
  );
}
