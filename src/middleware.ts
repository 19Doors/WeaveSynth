import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { auth } from './lib/auth'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
 
export async function middleware(request: NextRequest) {
  const protectedURLs = ["/"]
  for(let p of protectedURLs) {
    if(request.url.endsWith(p)) {
      const session = await auth.api.getSession({
	headers: await headers()
      })
      if(!session) {
	console.log("[WARN] Not Allowed to "+p)
	return NextResponse.redirect("http://localhost:3000/authentication")
      }
    }
  }
  return NextResponse.next();
}
 
export const config = {
  matcher: '/:path*',
}
