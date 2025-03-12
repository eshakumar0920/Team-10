import { useEffect, useState } from "react";

export const StatusBar = () => {
  const [time, setTime] = useState<string>("00:00");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes().toString().padStart(2, "0");
      setTime(`${hours}:${minutes}`);
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="text-[#010101] text-center text-[17px] font-semibold leading-none tracking-[-0.41px]">
      {time}
    </div>
  );
};
