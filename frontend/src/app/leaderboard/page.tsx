"use client";

import { useState, useEffect } from "react";
import { LeaderboardHero } from "../types/types";
import axios from "axios";
import { imageLinks } from "../lib/images";

type SortKey =
  | "win_rate"
  | "kpg"
  | "apg"
  | "dpg"
  | "mvp_rate"
  | "svp_rate";

export default function LeaderboardPage() {

  let [heroData, setHeroData] = useState<LeaderboardHero[]>([]);
  const [sortKey, setSortKey] = useState<SortKey>("win_rate");

  useEffect(() => {
    // Fetch user data when the component mounts
    getStats();
  }, []);

  const getStats = () => {
    axios.get('http://127.0.0.1:5000/api/leaderboard/')
      .then(res => {
        setHeroData(res.data.leaderboard);
      })
      .catch(err => console.error(err));

  };

  const sortOptions = [
    { label: "Win Rate", key: "win_rate" },
    { label: "Kills per game", key: "kpg" },
    { label: "Assists per game", key: "apg" },
    { label: "Deaths per game", key: "dpg" },
    { label: "MVP Rate", key: "mvp_rate" },
    { label: "SVP Rate", key: "svp_rate" },
  ];

  const sortedData = [...heroData].sort((a, b) => {
    console.log("Sorting by key: %s", sortKey);
    // if (sortKey === "dpg") {
    //   // reverse sort for deaths (smallest is better)
    //   return a[sortKey] - b[sortKey];
    // }
    if (sortKey === "win_rate") {
      console.log("Comparing win rates: a=%f, b=%f", a[sortKey], b[sortKey]);
    }

    return b[sortKey] - a[sortKey];
  });

  const medals = ["🥇", "🥈", "🥉"];

  const getColors = (winRate: number, thresholds: number[]) => {
    if (thresholds.length !== 2) {
      return "text-white";
    }
    if (thresholds[0] <= thresholds[1]) {
      if (winRate <= thresholds[0]) {
        return "text-green-400 font-semibold";
      } else if (winRate <= thresholds[1]) {
        return "text-yellow-300 font-semibold";
      }
      return "text-red-400 font-semibold";
    }

    if (winRate >= thresholds[0]) {
      return "text-green-400 font-semibold";
    } else if (winRate >= thresholds[1]) {
      return "text-yellow-300 font-semibold";
    }
    return "text-red-400 font-semibold";
  };


  return (
    <div className="font-sans min-h-screen w-full bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-10">
      {/* Title */}
      <div className="flex flex-col md:flex-row w-full justify-between items-left max-w-6xl mx-auto mb-10 space-y-2">
        <span></span>
        <h1 className="text-4xl font-extrabold tracking-wide text-purple-300 drop-shadow-lg md:ms-48">
          Hero Leaderboard
        </h1>


        {/* Sorting Dropdown */}
        <select
          value={sortKey}
          onChange={(e) => {

            setSortKey(e.target.value as SortKey)
          }}
          className="px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-purple-300 font-semibold max-w-48
          shadow-sm hover:border-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-400 ms-4"
        >
          {sortOptions.map((opt) => (
            <option key={opt.key} value={opt.key}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <p className="text-white mt-2 mx-auto text-center">
        This leaderboard highlights hero performance using match data from the top 50 players for each hero.
      </p>
      <p className="text-white mt-2 mb-4 mx-auto text-center">
        Provides insight to the most effective heroes at the top level of Marvel Rivals' competitive scene.
      </p>

      {/* Refresh Button 
      <div className="flex justify-center mb-10">
        <button
          onClick={getStats}
          className="px-6 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold shadow-md hover:shadow-purple-500/40 transition-all"
        >
          Refresh Leaderboard
        </button>
      </div>
      */}
      {/* Leaderboard */}
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedData.length === 0 ? (
          <div className="col-span-full text-center text-gray-400 text-lg">
            No stats available yet. Click refresh!
          </div>
        ) : (
          sortedData.map((player, i) => (
            <div
              key={player.name + i}
              className="p-5 rounded-xl bg-gray-800/70 backdrop-blur border border-gray-700 shadow-xl hover:shadow-purple-500/20 transition-all"
            >
              {/* Rank & Name */}
              <div className="flex justify-between items-center mb-3">
                <span className="text-3xl">
                  {i < 3 ? medals[i] : `#${i + 1}`}
                </span>


              </div>

              <div className="flex flex-col justify-center items-center mb-3">
                <img
                  src={imageLinks[player.name] || 'https://marvelrivalsapi.com/rivals/players/heads/player_head_30000001.png'}
                  alt={player.name}
                  className="w-24 h-24 object-cover rounded-full border-2 border-purple-300/50 shadow-lg mb-2"
                />
                <h2 className="text-xl font-bold text-purple-300 truncate">
                  {player.name.substring(0, 1).toUpperCase() + player.name.substring(1)}
                </h2>
              </div>
              {/* Stats */}
              <div className="text-sm space-y-1 text-gray-300">
                <p className={getColors(Math.round(player.win_rate * 100), [60, 50])}><span className="font-semibold">Win Rate:</span> {Math.round(player.win_rate * 100)}%</p>
                <p className={getColors(player.kpg, [22, 15])}><span className="font-semibold">Kills per game:</span> {player.kpg}</p>
                <p className={getColors(player.dpg, [5, 7])}><span className="font-semibold">Deaths per game:</span> {player.dpg}</p>
                <p className={getColors(player.apg, [15, 5])}><span className="font-semibold">Assists per game:</span> {player.apg}</p>
                <p className={getColors(Math.round(player.mvp_rate * 100), [25, 15])}><span className="font-semibold ">MVP Rate:</span> {Math.round(player.mvp_rate * 100)}%</p>
                <p className={getColors(Math.round(player.svp_rate * 100), [25, 15])}><span className="font-semibold">SVP Rate:</span> {Math.round(player.svp_rate * 100)}%</p>

              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
/*
<div className="font-sans flex flex-col items-center justify-items-center min-h-screen p-8 space-y-8">
            <h1 className="text-xl font-bold">Leaderboard page</h1>
            <div className="flex flex-row items-center justify-items-center space-x-4">

                <button
                onClick={() => getStats()}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Get Stats
              </button>
              </div>
              <h2 className="text-lg mb-4 mt-8">Player Stats:</h2>
            
      </div>*/