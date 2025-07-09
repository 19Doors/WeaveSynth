# 🚀 WeaveSynth: Your Personalized AI News Tapestry

![Next.js](https://img.shields.io/badge/Next.js-Black?style=for-the-badge&logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Drizzle ORM](https://img.shields.io/badge/Drizzle%20ORM-F6B61F?style=for-the-badge&logo=drizzle&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=for-the-badge&logo=gsap&logoColor=white)

WeaveSynth is an innovative, AI-powered news aggregator built to revolutionize how you consume news. Born during a Perplexity hackathon, this project dynamically fetches and synthesizes news content, creating a unique and personalized "news tapestry" tailored to your interests. By leveraging advanced AI capabilities and intelligent scraping, WeaveSynth delivers relevant and engaging articles directly to you.

## ✨ Features

WeaveSynth is packed with features designed to provide a seamless and insightful news experience:

*   **🧠 AI-Powered Aggregation:** Utilizes Perplexity's powerful AI to intelligently gather and process news from diverse sources, ensuring relevant and comprehensive content.
*   **📰 Personalized News Categories:** Explore various news domains, including `Global`, `National`, `Nature`, and `Sports`, with dedicated sections for easy navigation.
*   **🔐 Secure User Authentication:** Seamless sign-up and sign-in experiences powered by `better-auth`, ensuring your personalized news feed is secure and private.
*   **⚡ Dynamic Content Loading:** Enjoy a smooth user experience with custom loading animations using `GSAP`, indicating when new articles are being fetched.
*   **📱 Fully Responsive Design:** Crafted with `Tailwind CSS`, WeaveSynth provides an optimal viewing experience across all devices, from desktops to mobile phones.
*   **🖼️ Rich Article Previews:** Articles feature vibrant thumbnail images (when available) and concise summaries for quick browsing.
*   **📖 Immersive Article View:** Dive deep into articles with a clean, Markdown-rendered content display, ensuring readability and focus.
*   **🔄 Instant Refresh:** Easily refresh your news feed to get the latest updates with a single click.
*   **🗄️ Robust Database Schema:** Built with `Drizzle ORM` and `Turso DB`, ensuring efficient storage and retrieval of user data and article information.

## 📂 Project Structure

```
.
└── 19doors-weavesynth/
    ├── README.md
    ├── drizzle.config.ts         # Drizzle ORM configuration for database migrations
    ├── next.config.ts            # Next.js specific configurations
    ├── package.json              # Project dependencies and scripts
    ├── postcss.config.mjs        # PostCSS configuration, includes TailwindCSS
    ├── tsconfig.json             # TypeScript compiler settings
    ├── drizzle/                  # Drizzle ORM migration files and snapshots
    │   ├── 0000_flimsy_ogun.sql
    │   └── meta/
    │       ├── 0000_snapshot.json
    │       └── _journal.json
    └── src/
        ├── index.ts              # Drizzle ORM database client initialization
        ├── middleware.ts         # Next.js middleware for authentication protection
        ├── app/                  # Next.js App Router structure
        │   ├── globals.css       # Global styles and font imports
        │   ├── layout.tsx        # Root layout for the application
        │   ├── loading.tsx       # Global loading component
        │   ├── page.tsx          # Home page displaying global news
        │   ├── api/              # API routes
        │   │   └── auth/
        │   │       └── [...all]/
        │   │           └── route.ts # Authentication API endpoint
        │   ├── articles/         # Dynamic article pages
        │   │   └── [articleId]/
        │   │       ├── loading.tsx
        │   │       └── page.tsx
        │   ├── authentication/   # User authentication (Sign In/Sign Up) page
        │   │   └── page.tsx
        │   ├── loadingg/         # Additional loading component (can be consolidated)
        │   │   └── page.tsx
        │   ├── nature/           # Nature news category page
        │   │   └── page.tsx
        │   └── sports/           # Sports news category page
        │       └── page.tsx
        ├── components/           # Reusable UI components
        │   └── ui.tsx
        ├── db/                   # Database schema definitions
        │   └── schema.ts
        └── lib/                  # Utility functions and external integrations
            ├── articles.tsx      # Server actions for fetching news articles
            ├── auth-client.ts    # Better Auth client-side initialization
            └── auth.ts           # Better Auth server-side configuration
```

## 🛠️ Technologies Used

*   **Next.js 15:** A React framework for production.
*   **TypeScript:** Type-safe JavaScript for robust development.
*   **Drizzle ORM:** A modern TypeScript ORM for database interactions.
*   **Turso (via `libsql/client`):** Edge-friendly SQLite database.
*   **Better Auth:** Flexible authentication library for Next.js.
*   **Tailwind CSS:** A utility-first CSS framework for rapid UI development.
*   **GSAP:** Powerful JavaScript animation library for smooth UI transitions.
*   **Lucide React:** Beautifully simple and consistent open-source icon toolkit.
*   **Zustand:** A small, fast, and scalable bearbones state-management solution.
*   **React Markdown:** Render Markdown as React components.
*   **Vercel Analytics:** For performance and usage monitoring.

## 🚀 Getting Started

To get WeaveSynth up and running on your local machine, follow these steps:

### Prerequisites

Make sure you have Node.js (v18 or higher) and npm/yarn/pnpm/bun installed.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/19doors-weavesynth.git
    cd 19doors-weavesynth
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    # or
    pnpm install
    # or
    bun install
    ```
3.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your database credentials for Turso, as configured in `drizzle.config.ts`:
    ```
    DATABASE_URL="your_turso_database_url"
    DATABASE_AUTH_TOKEN="your_turso_auth_token"
    ```
    *(Note: For development, you might use a local SQLite database or a test Turso instance.)*

### Running the Development Server

Once installed, you can run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result. The page auto-updates as you edit the files.


Made with ❤️ during the Perplexity Hackathon.
```
