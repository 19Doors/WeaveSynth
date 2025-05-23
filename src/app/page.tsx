"use client";
import { getWorldNews } from "@/lib/articles";
import { AlignLeft, RefreshCw, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

function ArticleCard({ article }) {
  const cardRef = useRef(null);
  const titleRef = useRef(null);
  const router = useRouter();

  return (
    <div
      ref={cardRef}
      className="flex flex-col space-y-3 cursor-pointer overflow-hidden transition-transform duration-300 hover:scale-105 hover:shadow-xl bg-white rounded-xl p-2"
      onClick={() => router.push("/articles/" + article.id)}
    >
      {article.thumbnail_url && (
        <div className="w-full aspect-[16/9] bg-gray-100 rounded overflow-hidden">
          <img
            className="w-full h-full object-contain"
            src={article.thumbnail_url}
            alt={article.title}
          />
        </div>
      )}
      <a className="font-inter font-bold text-base md:text-lg text-primary line-clamp-3" ref={titleRef}>
        {article.title}
      </a>
      <p className="font-inter text-sm md:text-base line-clamp-2">{article.summary}</p>
    </div>
  );
}

export default function Home() {
  const { data: session, error } = authClient.useSession();
  const SideMenuRef = useRef(null);
  const router = useRouter();
  const [articles, setArticles] = useState([]);
  const [lfArticles, setlfArticles] = useState(false);

  async function handleRefresh() {
    setlfArticles(true);
    const articleResults = await getWorldNews();
    articleResults.reverse();
    setArticles(articleResults);
    setlfArticles(false);
  }

  useEffect(() => {
    handleRefresh();
  }, []);

  function handleSideMenuOpen() {
    gsap.to(SideMenuRef.current, {
      x: 0,
      duration: 0.5,
      ease: "power2.out",
    });
  }

  function handleSideMenuClose() {
    gsap.to(SideMenuRef.current, {
      x: "-100%",
      duration: 0.5,
      ease: "power2.in",
    });
  }

  async function signOut() {
    await authClient.signOut({
      fetchOptions: {
        onSuccess: () => {
          router.push("/authentication");
        },
      },
    });
  }

  const sidemenulinks = [
    ["Global", "/"],
    ["National", "/"],
    ["Nature", "/"],
    ["Sports", "/"],
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Desktop Navbar */}
      <div className="hidden lg:flex justify-between items-center px-8 py-4 bg-white text-black">
        <p className="font-instrument text-2xl">WeaveSynth</p>
        <div className="flex space-x-8 items-center">
          {sidemenulinks.map(([label, path]) => (
            <a key={label} className="hover:underline cursor-pointer font-instrument text-lg">
              {label}
            </a>
          ))}
        <a
  className="font-instrument text-1.5xl px-2 py-1 bg-primary text-white rounded-lg shadow-md cursor-pointer hover:bg-gray-100 transition-all duration-200"
  onClick={signOut}
>
  Logout
</a>
          <RefreshCw onClick={handleRefresh} size={20} color="black" className="cursor-pointer" />
        </div>
      </div>

      {/* Mobile/Tablet Header */}
      <div className="lg:hidden flex justify-between items-center px-6 py-4 bg-white">
        <AlignLeft onClick={handleSideMenuOpen} size={24} className="cursor-pointer" />
        <p className="font-instrument text-xl">WeaveSynth</p>
        <RefreshCw onClick={handleRefresh} size={20} className="cursor-pointer" />
      </div>

      {/* Sidebar for Mobile/Tablet */}
      <div
        ref={SideMenuRef}
        className="fixed top-0 left-0 -translate-x-full w-2/3 max-w-xs h-screen bg-primary z-50 flex flex-col p-8 md:hidden"
      >
        <div className="flex w-full justify-end">
          <X size={28} color="white" className="cursor-pointer" onClick={handleSideMenuClose} />
        </div>
        <div className="flex flex-grow flex-col space-y-24 items-center justify-center w-full">
          {sidemenulinks.map(([label, path]) => (
            <a key={label} className="font-instrument text-3xl text-white cursor-pointer hover:underline">
              {label}
            </a>
          ))}
          <a onClick={signOut} className="font-instrument text-3xl text-white cursor-pointer hover:underline">
            Logout
          </a>
        </div>
      </div>

      {/* Articles Section */}
      <div className="px-6 py-6">
        {lfArticles ? (
          <div className="flex justify-center items-center min-h-[60vh]">
            <p className="font-inter font-bold animate-pulse">Fetching New Articles! It will take time.</p>
          </div>
        ) : articles.length === 0 ? (
          <div className="flex justify-center items-center min-h-[60vh]">
            <p className="font-inter font-bold">OOPs! No Articles Found</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <ArticleCard key={article.title} article={article} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
