"use client";
import { Loading, NavbarNo } from "@/components/ui";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Authentication() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [siu, setSiu] = useState(true);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  async function signUp() {
    setLoading(true);
    const { error } = await authClient.signUp.email(
      { email, password, name, callbackURL: "/" },
      {
        onSuccess: () => {
          setLoading(false);
          router.push("/");
        },
        onError: (ctx) => {
          setLoading(false);
          setError(ctx.error.code);
        },
      }
    );
  }

  async function signIn() {
    setLoading(true);
    const { error } = await authClient.signIn.email(
      { email, password, callbackURL: "/" },
      {
        onSuccess: () => {
          setLoading(false);
          router.push("/");
        },
        onError: (ctx) => {
          setLoading(false);
          setError(ctx.error.code);
        },
      }
    );
  }

  return (
    <div className="h-screen w-screen flex font-inter auth-container">

      {/* Left Half - Typing Animation */}
<div className="w-2/3 relative bg-white text-black overflow-hidden left-half">

  <img
    src="https://st.depositphotos.com/2046901/3389/i/950/depositphotos_33898493-stock-photo-newspaper-border.jpg"
    alt="news background"
    className="absolute top-0 left-0 w-full h-full z-0 opacity-80"
  />
  <div className="absolute inset-0 bg-white/80 z-10" />
  <div className="relative z-20 h-full w-full flex flex-col justify-center items-center px-4 py-8 space-y-6">
    <h1
  className="text-6xl font-bold z-20"
  style={{ fontFamily: "'Instrument Serif', 'serif'" }}
>
  Welcome to WeaveSynth
</h1>
  <h2 className="text-xl sm:text-2xl md:text-3xl font-black text-black text-center max-w-2xl">
  <span className="hidden md:inline-block typing-animation border-r-4 pr-1 border-black">
    Weave your personalized news tapestry
  </span>
  <span className="inline-block md:hidden">
    Weave your personalized news tapestry
  </span>
</h2>

  </div>
</div>



      {/* Right Half - Form */}
      <div className="w-1/3 bg-black text-white flex flex-col justify-center px-10 right-half">

        {/* <NavbarNo /> */}
        <div className="max-w-md w-full space-y-6">
          <h2 className="text-3xl font-bold text-white text-center">
            {siu ? "Sign In" : "Create an Account"}
          </h2>
          {loading && <Loading />}
          {error && <p className="text-red-500 font-bold text-sm">{error}</p>}
          {!siu && (
            <div>
              <label className="block text-sm font-light">Name</label>
              <input
                type="text"
                className="w-full p-2 rounded bg-white/10 border border-white/30 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          )}
          <div>
            <label className="block text-sm font-light">Email</label>
            <input
              type="email"
              className="w-full p-2 rounded bg-white/10 border border-white/30 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-light">Password</label>
            <input
              type="password"
              className="w-full p-2 rounded bg-white/10 border border-white/30 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="flex justify-between items-center mt-4">
            <button
              onClick={siu ? signIn : signUp}
              className="w-28 h-10 rounded bg-white hover:bg-blue-900 transition text-sm text-black font-bold"
            >
              {siu ? "Sign In" : "Sign Up"}
            </button>
            <p
              className="text-sm underline cursor-pointer hover:text-blue-400"
              onClick={() => setSiu(!siu)}
            >
              {siu ? "Go to Sign Up" : "Go to Sign In"}
            </p>
          </div>
        </div>
      </div>

      {/* Infinite Typing Animation Style */}
 <style jsx>{`
 .typing-animation {
    overflow: hidden;
    white-space: nowrap;
    display: inline-block;
    animation: typing 2s steps(60, end) infinite alternate, blink 0.75s step-end infinite;
  }

  @keyframes typing {
    from {
      width: 0;
    }
    to {
      width: 100%;
    }
  }

  @keyframes blink {
    0%, 100% {
      border-color: black;
    }
    50% {
      border-color: transparent;
    }
  }

  @media screen and (max-width: 1024px) {
  .auth-container {
    flex-direction: column;
  }
    
  .left-half {
    width: 100%;
    height: 40vh;
  }

  .right-half {
    width: 100%;
    min-height: 60vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }

  .left-half h1 {
    font-size: 2.5rem;
    text-align: center;
  }

  .left-half h2 {
    font-size: 1.25rem;
    text-align: center;
    padding: 0 1rem;
  }
}

@media screen and (max-width: 640px) {
  .left-half {
    height: 40vh;
  }

  .right-half {
    background-color: transparent !important; /* Remove black bg */  
    min-height: 75vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
   
  }

  .typing-animation {
    display: none !important;
  }

  .left-half h1 {
    font-size: 3rem;
    line-height: 3.5rem;
    margin-top:2rem;
  }

  .left-half h2 {
  font-style: italic;
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  .right-half > div {
    width: 100%;
    max-width: 360px;
    background-color: black;
    padding: 1.5rem;
    border-radius: 8px;
    
  }
}

`}</style>
{loading && (
  <div className="fixed inset-0 bg-white flex items-center justify-center z-50">
    <Loading />
  </div>
)}
    </div>
  );
}
