
import React from "react";
import { useForm } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

interface RegisterFormData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

export const RegisterForm: React.FC = () => {
  const { register, handleSubmit } = useForm<RegisterFormData>();

  const onSubmit = (data: RegisterFormData) => {
    console.log(data);
    // Handle form submission
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="mb-8">
        <Label htmlFor="email" className="text-xs mb-3">
          UTD email
        </Label>
        <Input
          id="email"
          type="email"
          className="h-11 w-full bg-[#D9D9D9]"
          {...register("email")}
        />
      </div>

      <div className="mb-8">
        <Label htmlFor="password" className="text-xs mb-3">
          Password
        </Label>
        <Input
          id="password"
          type="password"
          className="h-11 w-full bg-[#D9D9D9]"
          {...register("password")}
        />
      </div>

      <div className="mb-8">
        <Label htmlFor="firstName" className="text-xs mb-3">
          First Name
        </Label>
        <Input
          id="firstName"
          type="text"
          className="h-11 w-full bg-[#D9D9D9]"
          {...register("firstName")}
        />
      </div>

      <div className="mb-8">
        <Label htmlFor="lastName" className="text-xs mb-3">
          Last Name
        </Label>
        <Input
          id="lastName"
          type="text"
          className="h-11 w-full bg-[#D9D9D9]"
          {...register("lastName")}
        />
      </div>

      <Button
        type="submit"
        className="text-xs w-[265px] h-[45px] bg-[rgba(255,233,107,0.29)] mt-[39px] mb-0 mx-auto rounded-[50px] max-sm:w-4/5 block hover:bg-[rgba(255,233,107,0.4)] text-black"
      >
        Sign in
      </Button>
    </form>
  );
};
