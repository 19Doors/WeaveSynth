import { AlignLeft, RefreshCw } from "lucide-react";

export function Navbar() {
  return(
      <div className="flex w-full justify-between items-center">
        <AlignLeft
          color="#2D2D34"
          size={18}
          strokeWidth={2.5}
          className="cursor-pointer"
        />
        <p className="font-instrument text-xl">WeaveSynth</p>
        <RefreshCw
          size={16}
          color="#2D2D34"
          className="cursor-pointer"
        />
      </div>
  )
}

export function NavbarNo() {
  return(
      <div className="flex w-full justify-center items-center">
        <p className="font-instrument text-xl">WeaveSynth</p>
      </div>
  )
}
