import { ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface AuthButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "register" | "signin";
}

export const AuthButton = ({
  children,
  className,
  variant = "register",
  ...props
}: AuthButtonProps) => {
  return (
    <button
      className={cn(
        "relative bg-[rgba(255,233,107,0.29)] w-[265px] max-w-full text-xs text-center tracking-[-0.41px] leading-loose pt-2 pb-6 px-[70px] rounded-[50px] transition-all hover:bg-[rgba(255,233,107,0.4)]",
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
};
