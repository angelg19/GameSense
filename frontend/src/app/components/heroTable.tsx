import { imageLinks } from "../lib/images";
import { HeroInfo } from "../types/types";

interface HeroTableProps {
  info: HeroInfo[];
}


export default function HeroTable({ info }: HeroTableProps) {
  return info.length >= 1? (
    <>

  <div className="overflow-x-auto rounded-xl shadow-lg border border-purple-400/30">
    <table className="min-w-full table-fixed text-left border-collapse">
      <thead className="bg-gray-800 text-purple-300 sticky top-0 shadow-md">
        <tr>
          <th className="p-3"></th>
          <th className="p-3 font-semibold">Hero</th>
          <th className="p-3 font-semibold">Matches</th>
          <th className="p-3 font-semibold">Wins</th>
          <th className="p-3 font-semibold">MVP</th>
          <th className="p-3 font-semibold">SVP</th>
          <th className="p-3 font-semibold">Accuracy</th>
          <th className="p-3 font-semibold">Kills</th>
          <th className="p-3 font-semibold">Deaths</th>
          <th className="p-3 font-semibold">Assists</th>
        </tr>
      </thead>

      <tbody>
        {info.map((hero) => (
          <tr
            key={hero.name}
            className="odd:bg-gray-900 even:bg-gray-850 hover:bg-gray-700 transition"
          >
            {/* Hero image */}
            <td className="p-3 w-20">
              {imageLinks[hero.name] && (
                <img
                  src={imageLinks[hero.name]}
                  alt={hero.name}
                  className="w-12 h-12 object-cover rounded-md border border-purple-300/40 shadow"
                />
              )}
            </td>

            {/* Hero name */}
            <td className="p-3 font-bold text-purple-200">
              {hero.name.charAt(0).toUpperCase() + hero.name.slice(1)}
            </td>

            {/* Stats */}
            <td className="p-3">{hero.matchesPlayed}</td>
            <td className="p-3">{hero.wins}</td>
            <td className="p-3">{hero.mvp}</td>
            <td className="p-3">{hero.svp}</td>
            <td className="p-3">{(hero.accuracy * 100).toFixed(1)}%</td>
            <td className="p-3">{hero.totalKills}</td>
            <td className="p-3">{hero.totalDeaths}</td>
            <td className="p-3">{hero.totalAssists}</td>
          </tr>
        ))}
      </tbody>
    </table>

    {/* Footer note */}
    <div className="flex justify-center mt-4 text-gray-300 text-sm mb-2">
      Note: Any hero with less than 10 matches played is generally not a good representation of your effectiveness with them.
    </div>
  </div>
</>

  ): (<div className="w-full flex flex-col items-center justify-center space-y-4 overflow-hidden mt-4">
  
  <img
    src="/gambit_rogue_img.avif"
    className="w-[80%] md:w-[40%] max-h-full object-contain opacity-80"
  />

  <div className="text-purple-300 text-3xl font-bold font-serif text-center">
    No Heroes Recorded!
  </div>

  <p className="text-gray-300 text-lg text-center max-w-md">
    Once you start playing more matches, your Hero stats will appear here after refreshing your stats.
  </p>
</div>


);
}