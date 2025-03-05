import { StatusBar } from "../common/StatusBar";
import { Logo } from "../common/Logo";
import { AuthButton } from "./AuthButton";

export const AuthScreen = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="bg-white max-w-[480px] w-full overflow-hidden text-black font-medium mx-auto rounded-[50px]">
        <div className="flex flex-col relative aspect-[0.492] mt-1 pt-[33px] pb-[211px] px-[45px]">
          <img
            src="https://cdn.builder.io/api/v1/image/assets/1280e979146e48758c1d81d3737a2d7e/b2f06eb4c1f7f4d9ec5c5439d0a3a3023eddb7c3d9abfb923dee0d1408cf578c?placeholderIfAbsent=true"
            alt="Background"
            className="absolute h-full w-full object-cover inset-0"
          />

          <StatusBar />

          <div className="relative mt-[19px]">
            <Logo />
          </div>

          <h2 className="relative text-3xl leading-[30px] tracking-[2px] text-center mt-[229px]">
            Welcome to <span className="font-bold">i</span>mpulse
            <br />
            <br />
            Where students meet connection
          </h2>

          <div className="flex flex-col items-center gap-[27px] mt-[34px]">
            <AuthButton
              onClick={() => console.log("Register clicked")}
              variant="register"
            >
              Register
            </AuthButton>

            <AuthButton
              onClick={() => console.log("Sign in clicked")}
              variant="signin"
              className="mb-[-42px]"
            >
              Sign in
            </AuthButton>
          </div>
        </div>
      </div>
    </div>
  );
};
