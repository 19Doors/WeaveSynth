"use server"

export async function getWorldNews() {
  const res = await fetch("http://127.0.0.1:8000/getArticles",{
    signal: AbortSignal.timeout(900000),
  });
  if (!res.ok) throw new Error('Failed to fetch articles');
  return res.json()
}
