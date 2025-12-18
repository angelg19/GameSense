"use client";

import { useEffect, useState } from "react";

import { PlayerInfo, HomepageProps, SwitcherProps } from "../types/types";
import { rankImageLinks } from "../lib/rankImages";
import HomepageContents from './components/homepageMain'
import PageSwitcher from "./components/pageSwitcher";
import useLLM from './hooks/useLLM'
import useStats from './hooks/useStats'


export default function Homepage() {
  const [inputValue, setInputValue] = useState("");

  const [showHeroGraphic, setShowHeroGraphic] = useState("default");
  const [showGraphic, setShowGraphic] = useState("kd");
  const [playerInfo, setPlayerInfo] = useState<PlayerInfo | null>(null);

  const [size, setSize] = useState({ width: 0, height: 0 });
  const [profileImage, setProfileImage] = useState("https://marvelrivalsapi.com/rivals/players/heads/player_head_30000001.png");

  const {
    disabled,
    llmResponseCode,
    llmConversation,
    llmResponse,
    llmQuestions,
    setllmInputValue,
    setDisabled,
    setllmResponse,
    setllmResponseCode,
    genLLM,
    askLLM
  } = useLLM(playerInfo);

  const {
    responseStatus,
    getStats,
    refreshStats,
  } = useStats(playerInfo, setPlayerInfo, setllmResponse)

  let props: HomepageProps = {
    contents: showHeroGraphic,
    playerInfo: playerInfo,
    showGraphic: showGraphic,
    llmResponseCode: llmResponseCode,
    disabled: disabled,
    llmResponse: llmResponse,
    llmConversation: llmConversation,
    llmQuestions: llmQuestions,

    genLLM: genLLM,
    askLLM: askLLM,
    setShowGraphic: setShowGraphic,
    setllmInputValue: setllmInputValue
  }

  let switcherProps: SwitcherProps = {
    showHeroGraphic: showHeroGraphic,
    setShowHeroGraphic: setShowHeroGraphic
  }


  useEffect(() => {
    const update = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    update(); // set initial size
    window.addEventListener("resize", update);

    return () => window.removeEventListener("resize", update);
  }, []);

  useEffect(() => {
    setDisabled(false);
    setllmResponse([]);
    setllmResponseCode(0);

    if (playerInfo?.icon) {
      setProfileImage('https://marvelrivalsapi.com/rivals' + playerInfo.icon)
    }

  }, [playerInfo])


  const defaultPage = (<>
    <h2 className="text-2xl text-purple-300 font-serif pt-20">How to use:</h2>
    <div className="space-y-2 pb-8">
      <li>Ensure your profile is set to public.</li>
      <li>Enter your Marvel Rivals uid to view your stats.</li>
      <li>If your stats seem outdated click the update button next to your name!</li>
      <li>It may take up to 30 minutes to succesfully update your stats</li>
      <li>Click generate tips to receive personalized tips based on your profile to improve your gameplay!</li>
    </div>
  </>
  );


  const getRankImage = () => {
    if (playerInfo?.rank) {
      if (rankImageLinks[playerInfo.rank]) { return rankImageLinks[playerInfo.rank] }
      if (rankImageLinks[playerInfo.rank.split(" ")[0]]) { return rankImageLinks[playerInfo.rank.split(" ")[0]] }
    }
    return rankImageLinks['Unranked']
  }


  return (
    <div className="font-sans flex flex-col items-center justify-items-center min-h-screen space-y-8 pb-1 pt-2">
      {/* Blurred background image */}
      {/* <div
        className="fixed inset-0 -z-10 bg-cover bg-center blur-sm opacity-40"
        style={{ backgroundImage: "url('/rivals_home.webp')" }}
      /> */}
      <div className="fixed inset-0 -z-10">
        <div
          className="absolute inset-0 bg-cover bg-center blur-sm"
          style={{ backgroundImage: "url('/rivals_home.webp')" }}
        />
        <div className="absolute inset-0 bg-black/60" />
      </div>
      {!playerInfo && (<div className="flex flex-col items-center justify-items-center w-full space-y-4 p-8 pt-20">
        <div className="bg-gray-900/60 backdrop-blur-lg rounded-2xl shadow-2xl">

          {/* Optional: subtle animated overlay */}
          <div className="absolute inset-0 bg-gradient-to-tr from-purple-900 via-gray-800 to-black 
                  opacity-20 animate-gradient-x pointer-events-none"></div>

          <div className="relative z-10 flex flex-row items-center justify-center w-full max-w-5xl">
            {size.width > 11750 && (
              <img src='/rogue_home.jpg'
                className="w-1/3 h-1/3 object-cover blur-[.5px] rounded-lg" // Tailwind blur-sm, blur, blur-md, etc.
              />
            )}

            <div className="flex flex-col items-center justify-center ms-12 me-12 pt-8">
              <h1 className="text-3xl md:text-4xl font-serif text-purple-300 font-extrabold">Find Your Stats!</h1>
              <div className="flex flex-col md:flex-row md:space-x-4 pt-4">
                <input
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Enter Player uid"
                  className="w-72 p-2 border rounded space-y-8 text-black focus:outline-none"
                />
                <button
                  onClick={() => getStats(inputValue)}
                  className="bg-purple-400 text-black rounded hover:bg-purple-500 px-4 py-2 mt-2 md:mt-0 md:ms-0"
                >
                  Get Stats
                </button>
              </div>
              {defaultPage}
              {responseStatus === 403 && (<>
                <h2 className="text-2xl text-red-500 font-serif mt-4">Your Account is private, stats could not be retrieved.</h2>
                <h2 className=" mt-10">If you recently made an update to your account privacy it may take up to 30 minutes to reflect changes.</h2>
              </>)
              }

              {responseStatus === 404 && (<>
                <h2 className="text-2xl text-red-500 font-serif mt-4">We could not find an account associated with this UID, stats could not be retrieved</h2>
                <h2 className=" mt-4">Make sure you typed the uid correctly!</h2>
              </>)
              }
            </div>
            {size.width > 11750 && (
              <img src='/gambit_home.jpg'
                className="w-1/3 h-1/3 object-cover blur-[.5px] rounded-lg"
              />)}

          </div>
        </div>
      </div>)}



      {playerInfo && (
        <>
          <div className="flex items-center justify-between min-w-fit w-8/12 h-20 border-2 border-purple-300 p-2 rounded-lg bg-gray-800 mt-10 relative z-10">
            <div className="flex items-center space-x-2">
              <img src={profileImage} className="w-16 h-16 border-2 border-solid border-white rounded" />
              <div className="flex flex-col">
                <span className="font-bold  text-2xl">
                  {`${playerInfo.name}`}
                </span>
                <span>Lv. {playerInfo.level}</span>
              </div>
            </div>
            {size.width > 850 && (<>
              <div className="flex items-center">
                <span className="font-bold">
                  {playerInfo.rank === 'Invalid level' ? 'Unranked' : playerInfo.rank}
                </span>
                <img src={getRankImage()} className="w-16 h-16" />
              </div>

              <button className='bg-purple-400 text-black rounded hover:bg-purple-500 px-4 py-2' onClick={refreshStats}>
                Refresh Stats
              </button>
            </>)}
          </div>

          {/* Page Switcher */}
          <PageSwitcher {...switcherProps} />

          {/* Main Content */}
          <div className="relative flex flex-col w-[90%] flex-grow items-center rounded-xl 
                bg-gradient-to-br from-gray-900 via-gray-800 to-black shadow-inner p-6 overflow-hidden m-[5px]">

            {/* Optional: subtle animated overlay */}
            <div className="absolute inset-0 bg-gradient-to-tr from-purple-900 via-gray-800 to-black 
                  opacity-20 animate-gradient-x pointer-events-none"></div>

            <div className="relative w-full">
              <HomepageContents {...props} />
            </div>
          </div>

        </>
      )}
      <div></div>
    </div>
  );
}

