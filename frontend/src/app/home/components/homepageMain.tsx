import { Bar } from 'react-chartjs-2';

import HeroCard from "../../components/heroTable";

import { HomepageProps } from "../../types/types";
import MapTable from "../../components/mapTable";
import { BarData, options } from "../../chart/heroChart";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function HomepageContents(props: HomepageProps) {

    const llmResponseDisplay = () => {
        if (props.llmResponseCode === 2 && props.llmResponse) {
            if (props.llmResponse.length === 0) {
                return <div>No tips available.</div>;
            }

            return (
                <div className="flex flex-col justify-center">
                    <h2 className="text-2xl items-center text-purple-300 font-serif mt-4">Personalized Tips to Improve Your Gameplay:</h2>

                    {props.llmResponse.map((tip, index) => (
                        <li className="ms-16 max-w-[90%]" key={`tip_${index}`}>{tip}</li>
                    ))}

                </div>
            )
        }
        if (props.llmResponseCode === 1) {
            return (<div className="flex justify-center items-center w-full h-full mx-auto pt-40">
                <p className="text-xl font-semibold flex space-x-1">
                    <span>Generating Your Tips</span>
                    <span className="dot-1">.</span>
                    <span className="dot-2">.</span>
                    <span className="dot-3">.</span>
                </p>
            </div>)
        }
        if (props.llmResponseCode === -1) {
            return <div>Error generating tips. Please try again later.</div>
        }
        return <></>;

    }

    if (!props.playerInfo) {
        return <></>
    }

    if (props.contents === "hero") {
        return (<HeroCard info={props.playerInfo.topHeroes} />)

    }

    if (props.contents === "map") {
        return (<MapTable info={props.playerInfo.topMaps} />)
    }

    if (props.contents === "charts") {
        return (<>
            {/* Header row */}
            <div className="relative w-full flex flex-col md:flex-row space-y-1 items-left justify-between mt-4 mb-4">
                <span></span>
                {/* Centered title */}
                <div className="text-purple-300 text-3xl font-serif md:ms-40">
                    Your Hero Stats Vs Top 1000 Players:
                </div>

                {/* Dropdown positioned on the right */}
                <div className="me-8">
                    <select
                        value={props.showGraphic}
                        onChange={(e) => props.setShowGraphic(e.target.value)}
                        className="px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-purple-300 font-semibold max-w-44
                            shadow-sm hover:border-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-400 ms-4">

                        <option value={"accuracy"}>
                            Accuracy
                        </option>
                        <option value={"kd"}>
                            K/D
                        </option>
                        <option value={"assists"}>
                            Assists
                        </option>

                    </select>
                </div>
            </div>

            {/* Chart */}
            <div className="w-[90%] md:w-[80%] h-[50vh] md:h-[70vh] mx-auto mt-6">
                {props.showGraphic === "accuracy" && (
                    <Bar
                        data={BarData(props.playerInfo.topHeroes.slice(0, 5), "accuracy")}
                        options={options("Accuracy")}
                    />
                )}
                {props.showGraphic === "kd" && (
                    <Bar
                        data={BarData(props.playerInfo.topHeroes.slice(0, 5), "kd")}
                        options={options("K/D Ratio")}
                    />
                )}
                {props.showGraphic === "assists" && (
                    <Bar
                        data={BarData(props.playerInfo.topHeroes.slice(0, 5), "assists")}
                        options={options("Assists per Game")}
                    />
                )}
            </div>

            {/* Footer note */}
            <div className="flex justify-center mt-4 text-gray-300 text-sm">
                Note: Top 1000 averages get refreshed weekly on Sunday
            </div>
        </>
        )
    }

    return (<>
        {/* ——— Initial Prompt (Before Generating Tips) ——— */}
        {props.llmResponseCode === 0 && !props.disabled && (
            <div className="w-full max-w-2xl text-center bg-gray-700 p-6 rounded-xl shadow-lg mx-auto mt-6">
                <p className="font-serif font-bold text-2xl text-gray-100">
                    Ready to level up your Marvel Rivals gameplay?
                </p>
                <p className="mt-3 text-gray-300 text-lg">
                    Click below to generate personalized improvement tips and begin chatting with your AI Rivals Expert.
                </p>

                <button
                    onClick={() => { props.genLLM() }}
                    className="mt-6 bg-purple-500 text-black font-semibold rounded-xl hover:bg-purple-600 px-6 py-3 transition shadow"
                >
                    Generate Tips
                </button>
            </div>
        )}

        {/* ——— Notice Section ——— */}
        {props.disabled && props.playerInfo && (
            <div className="w-full max-w-3xl bg-gray-700 p-5 rounded-xl shadow text-purple-200 mx-auto">
                <h2 className="text-2xl font-serif mb-3">Keep in Mind:</h2>

                <ul className="list-disc list-inside space-y-2 text-lg font-mono text-gray-200">
                    <li>Please only ask Marvel Rivals gameplay-related questions. Any other questions will not be answered.</li>
                    <li>You are allowed 5 questions to the AI assistant in one conversation.</li>
                </ul>
            </div>
        )}

        {/* ——— LLM Response ——— */}
        <div className="w-full max-w-3xl text-gray-100 mx-auto h-full">

        </div>

        {/* ——— Conversation History ——— */}
        {/* {props.llmConversation && (
            <div className="w-full max-w-3xl p-4 text-lg text-gray-100 mx-auto mt-6">
                {llmResponseDisplay()}
                {props.llmConversation}
            </div>
        )} */}


        <div className="w-full max-w-3xl mx-auto mt-6 space-y-6">

            {/* Initial LLM response */}
            <div className="p-4 rounded-xl  text-gray-100 pt-0">
                {llmResponseDisplay()}
            </div>

            {/* Conversation */}
            {props.llmConversation && props.llmQuestions && (
                <div className="flex flex-col space-y-4">
                    {props.llmQuestions.map((question, i) => (
                        <div key={i} className="flex flex-col space-y-2">

                            {/* Assistant / System */}
                            <div className="self-start max-w-[80%] bg-blue-600/80 text-white p-3 rounded-xl rounded-bl-none shadow">
                                {question}
                            </div>

                            {/* User reply (if exists) */}
                            {props.llmConversation[i] && (
                                <div className="self-end max-w-[80%] bg-gray-700 text-gray-100 p-3 rounded-xl rounded-br-none shadow">
                                    {props.llmConversation[i]}
                                </div>
                            )}

                        </div>
                    ))}
                </div>
            )}
        </div>



        {/* ——— Input Area ——— */}
        {props.disabled && props.playerInfo && (
            <div className="w-full max-w-3xl bg-gray-700 rounded-xl p-5 flex flex-col space-y-4 shadow mx-auto mt-4">

                <input
                    onChange={(e) => props.setllmInputValue(e.target.value)}
                    placeholder="Ask for tips on improving in Marvel Rivals..."
                    className="w-full p-3 rounded-lg text-black border border-gray-300 focus:outline-none focus:ring focus:ring-purple-400"
                    maxLength={150}
                />

                <div className="flex flex-row items-center justify-between">
                    <span className="text-sm text-gray-300">Limit: 150 characters</span>

                    <button
                        className="bg-purple-400 text-black font-medium rounded-lg px-5 py-2 hover:bg-purple-500 transition"
                        onClick={() => { props.askLLM() }}
                    >
                        Ask
                    </button>
                </div>

            </div>
        )}
    </>)

}