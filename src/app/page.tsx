"use client";
import { getWorldNews } from "@/lib/articles";
import { AlignLeft, RefreshCw, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { getSession, signOut } from "better-auth/api";

function ArticleCard({ article }) {
  const cardRef = useRef(null);
  const titleRef = useRef(null);
  const router = useRouter();

  function handleMouseEnter() {
    if (titleRef.current) {
      gsap.to(titleRef.current, {
        duration: 0.3,
      });
    }
  }

  function handleMouseLeave() {
    if (titleRef.current) {
    }
  }

  return (
    <div
      ref={cardRef}
      className="flex flex-col space-y-3 cursor-pointer overflow-hidden"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={() => {
        router.push("/articles/" + article.id);
      }}
    >
      {article.thumbnail_url != "" && (
        <img
          className="w-full h-48 object-cover rounded"
          src={article.thumbnail_url}
          alt={article.title}
        />
      )}
      <a
        className="font-inter font-bold text-base/5 text-primary line-clamp-3"
        ref={titleRef}
      >
        {article.title}
      </a>
      <p className="font-inter text-xs/4 line-clamp-2">{article.summary}</p>
    </div>
  );
}

export default function Home() {
  const { data: session, error } = authClient.useSession();
  console.log(session);
  const SideMenuRef = useRef(null);
  const router = useRouter();
  const [articles, setArticles] = useState([]);
  const [lfArticles, setlfArticles] = useState(false);
  async function handleRefresh() {
    setlfArticles((e) => true);
    const articleResults = await getWorldNews();
    articleResults.reverse();
    console.log(articleResults);
    setArticles((a) => articleResults);
    setlfArticles((e) => false);
  }
  async function initialFetchArticles() {
    await handleRefresh();
  }
  useEffect(() => {
    initialFetchArticles();
  }, []);
  function handleSideMenuOpen() {
    gsap.to(SideMenuRef.current, {
      left: 0,
      duration: 0.5,
      ease: "power2.out",
    });
  }
  function handleSideMenuClose() {
    gsap.to(SideMenuRef.current, {
      left: -1000,
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
    <div className="relative p-4 px-8 flex flex-col space-y-8 h-screen">
      <div
        ref={SideMenuRef}
        className="p-8 absolute top-0 -left-[100%] w-full h-screen bg-primary translate flex flex-col h-full"
      >
        <div className="flex w-full justify-end">
          <X
            color="#FFFFFF"
            size={28}
            strokeWidth={2.5}
            className="cursor-pointer"
            onClick={handleSideMenuClose}
          />
        </div>
        <div className="flex flex-grow flex-col space-y-24 items-center justify-center w-full">
          {sidemenulinks.map((e) => (
            <a
              key={e}
              className="font-instrument text-4xl text-white cursor-pointer"
            >
              {e[0]}
            </a>
          ))}
          <a
            className="font-instrument text-4xl text-white cursor-pointer"
            onClick={signOut}
          >
            Logout
          </a>
        </div>
      </div>
      <div className="flex w-full justify-between items-center">
        <AlignLeft
          color="#2D2D34"
          size={18}
          strokeWidth={2.5}
          className="cursor-pointer"
          onClick={handleSideMenuOpen}
        />
        <p className="font-instrument text-xl">WeaveSynth</p>
        <RefreshCw
          onClick={handleRefresh}
          size={16}
          color="#2D2D34"
          className="cursor-pointer"
        />
      </div>
      <div className="flex flex-grow flex-col space-y-6 ">
        {lfArticles && (
          <div className="flex flex-grow items-center justify-center">
            <p className="font-inter font-bold">
              Fetching New Articles! It will take time.
            </p>
          </div>
        )}
        {lfArticles != true && articles.length == 0 && (
          <div className="flex flex-grow items-center justify-center">
            <p className="font-inter font-bold">OOPs! No Articles Found</p>
          </div>
        )}
        {lfArticles != true &&
          articles.length != 0 &&
          articles.map((article) => (
            <ArticleCard key={article.title} article={article} />
          ))}
      </div>
    </div>
  );
}
