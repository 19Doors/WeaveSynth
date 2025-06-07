import { Navbar, NavbarNo } from "@/components/ui";
import { fetchArticleById } from "@/lib/articles";
import Markdown from "react-markdown";

function convertUTCToLocalDateTime(utcTimestamp: string): string {
  // Parse the UTC timestamp
  const utcDate = new Date(utcTimestamp);
  
  // Convert to local time
  const localDate = new Date(utcDate.getTime());
  
  // Extract components
  const day = localDate.getDate();
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  const monthName = monthNames[localDate.getMonth()];
  const year = localDate.getFullYear();
  
  // Format time (12-hour format with AM/PM)
  const hours = localDate.getHours();
  const minutes = localDate.getMinutes().toString().padStart(2, '0');
  const seconds = localDate.getSeconds().toString().padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours % 12 || 12;
  
  const localTime = `${displayHours}:${minutes}:${seconds} ${ampm}`;
  
  return `${day} ${monthName} ${year}, ${localTime}`;
}
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
      <div className="font-inter flex flex-col space-y-3 sm:mx-20 md:mx-[25%]">
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
                ? "list-decimal list-inside text-sm flex flex-col space-y-1" // For <ol>
                : "list-disc list-inside text-sm flex flex-col space-y-1"; // For <ul>
              return (
                <ul className={`${classes} ${className || ""}`} {...rest}>
                  {children}
                </ul>
              );
            },
            ol: ({ node, ordered, className, children, ...rest }) => {
              // For ordered lists (numbers)
              const classes = "list-decimal list-inside text-sm";
              return (
                <ol className={`${classes} ${className || ""}`} {...rest}>
                  {children}
                </ol>
              );
            },
            li: ({ node, ordered, className, children, index, ...rest }) => {
              // You might want to add margin to list items if your ul/ol doesn't handle it
              return (
                <li className={`${className || ""}`} {...rest}>
                  {children}
                </li>
              );
            },
          }}
        >
          {article.content}
        </Markdown>
	<p className="font-inter text-xs font-bold text-center">{convertUTCToLocalDateTime(article.publishedDT)}</p>
      </div>
    </div>
  );
}
