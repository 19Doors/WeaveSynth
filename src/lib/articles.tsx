"use server"

import { articles } from "@/db/schema"
import { db } from ".."
import { eq } from "drizzle-orm"

export async function getWorldNews() {
  const result = await db.select().from(articles)
  return result
}

export async function getNatureNews() {
  const result = await db.select().from(articles).where(eq(articles.category,"nature"));
  return result
}

export async function getSportsNews() {
  const result = await db.select().from(articles).where(eq(articles.category,"sports"));
  return result
}

export async function fetchArticleById(id) {
  const result = await db.select().from(articles).where(eq(articles.id,id))
  return result
}
