"use client";
import { Loading, Navbar, NavbarNo } from "@/components/ui";
import { authClient } from "@/lib/auth-client";
import { router } from "better-auth/api";
import { redirect } from "next/dist/server/api-utils";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

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
          <div>
            <p className="font-inter text-primary text-2xl font-black">
              Weave your personalized news tapestry
            </p>
            {error && error.length != 0 && (
              <p className="font-inter text-red-500 font-bold">{error}</p>
            )}
            {siu == true && (
              <div className="flex flex-col space-y-4 font-inter font-bold text-primary">
                <div>
                  <p className="font-light">Email</p>
                  <input
                    type="email"
                    className="w-full border p-1 text-sm rounded"
                    onChange={(e) => {
                      setEmail(e.target.value);
                    }}
                  />
                </div>
                <div>
                  <p className="font-light">Password</p>
                  <input
                    type="password"
                    className="w-full border p-1 text-sm rounded"
                    onChange={(e) => {
                      setPassword(e.target.value);
                    }}
                  />
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
                <div>
                  <p className="font-light">Name</p>
                  <input
                    type="text"
                    className="w-full border p-1 text-sm rounded"
                    onChange={(e) => {
                      setName(e.target.value);
                    }}
                  />
                </div>
                <div>
                  <p className="font-light">Email</p>
                  <input
                    type="email"
                    className="w-full border p-1 text-sm rounded"
                    onChange={(e) => {
                      setEmail(e.target.value);
                    }}
                  />
                </div>
                <div>
                  <p className="font-light">Password</p>
                  <input
                    type="password"
                    className="w-full border p-1 text-sm rounded"
                    onChange={(e) => {
                      setPassword(e.target.value);
                    }}
                  />
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
