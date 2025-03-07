import React from "react";
import { StatusBar } from "@/components/layout/StatusBar";
import { Logo } from "@/components/layout/Logo";
import { RegisterForm } from "@/components/auth/RegisterForm";

const Index = () => {
  return (
    <div className="w-full min-h-screen bg-white">
      <StatusBar />
      <main className="px-[51px] py-0 max-md:px-[30px] max-md:py-0 max-sm:px-5 max-sm:py-0">
        <Logo />
        <h1 className="text-2xl mt-24 mb-10">Register</h1>
        <RegisterForm />
      </main>
    </div>
  );
};

export default Index;
