"use client";
import { Loading, Navbar, NavbarNo } from "@/components/ui";
import { authClient } from "@/lib/auth-client";
import { router } from "better-auth/api";
import { Inbox, LockOpen, User } from "lucide-react";
import { redirect } from "next/dist/server/api-utils";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { gsap } from "gsap";
import { Flip } from "gsap/Flip";

gsap.registerPlugin(Flip);

export default function authentication() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [siu, setSiu] = useState(true);
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function signUp() {
    setLoading((e) => true);
    const { data, error } = await authClient.signUp.email(
      {
        email,
        password,
        name,
        callbackURL: "/",
      },
      {
        onSuccess: (ctx) => {
          setLoading((e) => false);
          router.push("/");
          console.log("Success");
        },
        onError: (ctx) => {
          setLoading((e) => false);
          console.log(ctx);
          setError(ctx.error.code);
        },
      },
    );
    setLoading((e) => false);
  }
  async function signIn() {
    setLoading((e) => true);
    const { data, error } = await authClient.signIn.email(
      {
        email,
        password,
        callbackURL: "/",
      },
      {
        onSuccess: (ctx) => {
          setLoading((e) => false);
          router.push("/");
          console.log("Success");
        },
        onError: (ctx) => {
          setLoading((e) => false);
          console.log(ctx);
          setError(ctx.error.code);
        },
      },
    );
    setLoading((e) => false);
  }
  useEffect(() => {}, [siu]);
  useEffect(() => {}, [loading]);
  return (
    <div className="flex flex-col px-8 p-4 h-screen">
      <NavbarNo />
      <div className="flex flex-grow flex-col justify-center items-left h-screen space-y-4 md:mx-[30%]">
        {loading && (
          <div>
            <Loading />
          </div>
        )}
        {loading == false && (
          <div className="flex flex-col space-y-8">
            {error && error.length != 0 && (
              <p className="font-inter text-red-500 font-bold">{error}</p>
            )}
            {siu == true && (
              <div className="flex flex-col space-y-4 font-inter font-bold text-primary">
                <p className="font-inter text-primary text-3xl font-medium">
                  Welcome Back! <br />
                  Sign in to continue
                </p>
                <div className="relative w-full h-full flex flex-col justify-center">
                  <input
                    type="email"
                    className="w-full border p-2 text-sm rounded bg-white focus:z-50"
                    onChange={(e) => {
                      setEmail((x) => e.target.value);
                    }}
                  />
                  {email == "" && (
                    <div className="ml-2 flex space-x-2 items-center justify-center absolute left-0 font-inter">
                      <Inbox size={16} color="#2D2D34" strokeWidth={1} />
                      <p className="text-xs font-normal">Email</p>
                    </div>
                  )}
                </div>
                <div className="relative w-full h-full flex flex-col justify-center">
                  <input
                    type="password"
                    className="w-full border p-2 text-sm rounded bg-white focus:z-50"
                    onChange={(e) => {
                      setPassword(e.target.value);
                    }}
                  />
                  {password == "" && (
                    <div className="ml-2 flex space-x-2 items-center justify-center absolute left-0 font-inter">
                      <LockOpen size={16} color="#2D2D34" strokeWidth={1} />
                      <p className="text-xs font-normal">Password</p>
                    </div>
                  )}
                </div>
                <div className="flex justify-between items-center">
                  <div
                    onClick={signIn}
                    className="flex justify-center items-center bg-primary w-20 h-10 rounded cursor-pointer"
                  >
                    <p className="font-inter text-white font-bold text-sm">
                      Sign In
                    </p>
                  </div>
                  <p
                    className="font-inter underline cursor-pointer"
                    onClick={() => {
                      setSiu(false);
                    }}
                  >
                    Go to Sign Up
                  </p>
                </div>
              </div>
            )}
            {siu == false && (
              <div className="flex flex-col space-y-4 font-inter font-bold text-primary">
                <p className="font-inter text-primary text-3xl font-medium">
                  Create Account! <br />
                  Join us today!
                </p>
                <div className="relative w-full h-full flex flex-col justify-center">
                  <input
                    type="text"
                    className="w-full border p-2 text-sm rounded bg-white focus:z-50"
                    onChange={(e) => {
                      setName(e.target.value);
                    }}
                  />
                  {name == "" && (
                    <div className="ml-2 flex space-x-2 items-center justify-center absolute left-0 font-inter">
                      <User size={16} color="#2D2D34" strokeWidth={1} />
                      <p className="text-xs font-normal">Name</p>
                    </div>
                  )}
                </div>

                <div className="relative w-full h-full flex flex-col justify-center">
                  <input
                    type="email"
                    className="w-full border p-2 text-sm rounded bg-white focus:z-50"
                    onChange={(e) => {
                      setEmail((x) => e.target.value);
                    }}
                  />
                  {email == "" && (
                    <div className="ml-2 flex space-x-2 items-center justify-center absolute left-0 font-inter">
                      <Inbox size={16} color="#2D2D34" strokeWidth={1} />
                      <p className="text-xs font-normal">Email</p>
                    </div>
                  )}
                </div>
                <div className="relative w-full h-full flex flex-col justify-center">
                  <input
                    type="password"
                    className="w-full border p-2 text-sm rounded bg-white focus:z-50"
                    onChange={(e) => {
                      setPassword(e.target.value);
                    }}
                  />
                  {password == "" && (
                    <div className="ml-2 flex space-x-2 items-center justify-center absolute left-0 font-inter">
                      <LockOpen size={16} color="#2D2D34" strokeWidth={1} />
                      <p className="text-xs font-normal">Password</p>
                    </div>
                  )}
                </div>
                <div className="flex justify-between items-center">
                  <div
                    onClick={signUp}
                    className="flex justify-center items-center bg-primary w-20 h-10 rounded cursor-pointer"
                  >
                    <p className="font-inter text-white font-bold text-sm">
                      Sign Up
                    </p>
                  </div>
                  <p
                    className="font-inter underline cursor-pointer"
                    onClick={() => {
                      setSiu(true);
                    }}
                  >
                    Go to Sign In
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
