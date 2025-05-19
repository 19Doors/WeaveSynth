"use server"

import { articles } from "@/db/schema"
import { db } from ".."

export async function getWorldNews() {
  const result = await db.select().from(articles)
  return result
}
