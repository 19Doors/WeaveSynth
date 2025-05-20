import { Navbar, NavbarNo } from "@/components/ui";
import { fetchArticleById } from "@/lib/articles";
import Markdown from "react-markdown";

export default async function ArticlePage({
  params,
}: {
  params: Promise<{ articleId: string }>;
}) {
  const { articleId } = await params;
  let article = await fetchArticleById(articleId);
  article = article[0];
  console.log(article);
  return (
    <div className="p-4 flex flex-col space-y-4">
      <NavbarNo />
      <div className="font-inter flex flex-col space-y-4">
        <Markdown
          components={{
            p(props) {
              const { node, children, ...rest } = props;
              return <p className="text-sm">{children}</p>;
            },
            h1(props) {
              const { node, children, ...rest } = props;
              return <h1 className="font-bold text-lg">{children}</h1>;
            },
            h2(props) {
              const { node, children, ...rest } = props;
              return <h2 className="font-bold text-base">{children}</h2>;
            },
            h3(props) {
              const { node, children, ...rest } = props;
              return <h3 className="font-bold text-sm">{children}</h3>;
            },
            ul: ({ node, ordered, className, children, ...rest }) => {
              const classes = ordered
                ? "list-decimal list-inside my-2 text-sm" // For <ol>
                : "list-disc list-inside my-2 text-sm"; // For <ul>
              return (
                <ul className={`${classes} ${className || ""}`} {...rest}>
                  {children}
                </ul>
              );
            },
            ol: ({ node, ordered, className, children, ...rest }) => {
              // For ordered lists (numbers)
              const classes = "list-decimal list-inside my-2 text-sm";
              return (
                <ol className={`${classes} ${className || ""}`} {...rest}>
                  {children}
                </ol>
              );
            },
            li: ({ node, ordered, className, children, index, ...rest }) => {
              // You might want to add margin to list items if your ul/ol doesn't handle it
              return (
                <li className={`mb-1 ${className || ""}`} {...rest}>
                  {children}
                </li>
              );
            },
          }}
        >
          {article.content}
        </Markdown>
      </div>
    </div>
  );
}
