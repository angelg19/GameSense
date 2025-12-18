
import { MapInfo } from "../types/types";
import { mapImageLinks } from "../lib/mapImages";

export interface MapTableProps {
  info: MapInfo[];
}

export default function MapTable({ info }: MapTableProps) {
  return info.length >= 1 ? (
    <>

  <div className="overflow-x-auto rounded-xl shadow-lg border border-purple-400/30">
    <table className="min-w-full table-fixed text-left border-collapse">
      <thead className="bg-gray-800 text-purple-300 sticky top-0 shadow-md">
        <tr>
          <th className="p-3"></th>
          <th className="p-3 font-semibold">Map</th>
          <th className="p-3 font-semibold">Matches</th>
          <th className="p-3 font-semibold">Wins</th>
          <th className="p-3 font-semibold">Kills</th>
          <th className="p-3 font-semibold">Deaths</th>
          <th className="p-3 font-semibold">Assists</th>
        </tr>
      </thead>

      <tbody>
        {info.map((map) => {
          const details = mapImageLinks[map.map_id];
          if (!details) return null;

          return (
            <tr
              key={map.map_id}
              className="odd:bg-gray-900 even:bg-gray-850 hover:bg-gray-700 transition"
            >
              <td className="p-3">
                <img
                  src={details.image_url}
                  alt={`${details.name} - ${details.location}`}
                  className="w-32 h-20 object-cover rounded-md border border-purple-300/40 shadow"
                />
              </td>

              <td className="p-3 font-bold text-purple-200">
                {details.name} – {details.location}
              </td>

              <td className="p-3">{map.matches}</td>
              <td className="p-3">{map.wins}</td>
              <td className="p-3">{map.kills}</td>
              <td className="p-3">{map.deaths}</td>
              <td className="p-3">{map.assists}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  </div>
</>

  ) : (<div className="w-full flex flex-col items-center justify-center space-y-4 overflow-hidden mt-4">
  
  <img
    src="/gambit_rogue_img.avif"
    className="w-[80%] md:w-[40%] max-h-full object-contain opacity-80"
  />

  <div className="text-purple-300 text-3xl font-bold font-serif text-center">
    No Maps Recorded!
  </div>

  <p className="text-gray-300 text-lg text-center max-w-md">
    Once you start playing more matches, your Map stats will appear here after refreshing your stats.
  </p>
</div>);
}