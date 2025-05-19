import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "..";
import { user,session,account,verification } from "@/db/schema";
 
export const auth = betterAuth({
    database: drizzleAdapter(db, {
        provider: "sqlite", 
	schema: {
	  user,
	  account,
	  session,
	  verification
	}
    }),
    emailAndPassword: {
      enabled: true
    }
});
