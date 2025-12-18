import { useState } from "react";
import axios from "axios";

import { PlayerInfo } from "../../types/types";


export default function useStats(playerInfo: PlayerInfo | null, setPlayerInfo: (value: PlayerInfo | null) => void, setllmResponse: (value: string[]) => void) {
    const [responseStatus, setResponseStatus] = useState(0);

    const getStats = (str: String) => {
        setPlayerInfo(null);
        setResponseStatus(0);
        setllmResponse([]);

        axios.get(`http://127.0.0.1:5000/api/users/${str}`)
            .then(res => {
                console.log("Response data: ", res.data);
                setPlayerInfo(res.data);
            })
            .catch(err => {
                setResponseStatus(err.response.status);
            });

    };

    const refreshStats = () => {
        if (!playerInfo) {
            return
        }

        axios.post(`http://127.0.0.1:5000/api/users/${playerInfo.name}/refresh`)
            .then(res => {
                console.log("Response data: ", res.data);
                console.log("Success: ", res.status)
                alert("Stats refreshed successfully! Please allow up to 20 minutes for the changes to take effect.");
            })
            .catch(err => {
                if (err.status == 403) {
                    console.error("User not found")
                }
                console.error(err.message);

            });

    }


    return {
        responseStatus,
        getStats,
        refreshStats
    };
}