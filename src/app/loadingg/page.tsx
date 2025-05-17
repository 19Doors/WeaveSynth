"use client";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { TextPlugin } from "gsap/TextPlugin";
import { ScrambleTextPlugin } from "gsap/ScrambleTextPlugin";
import { useRef } from "react";

export default function loading() {
  gsap.registerPlugin(useGSAP, TextPlugin, ScrambleTextPlugin);
  const loadingText = useRef(null);
  useGSAP(() => {
    gsap.to(loadingText.current, {
      duration: 2.0, scrambleText: {
	text: "LOADING",
	chars: "XO123",
	speed: 0.3,
      },
      ease: "sine.out"
    })
  })
  return (
    <div className="w-full h-screen flex items-center justify-center">
      <p ref={loadingText} className="font-bold font-spaceG text-4xl"></p>
    </div>
  );
}
