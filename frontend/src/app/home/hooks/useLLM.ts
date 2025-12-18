import { useEffect, useState } from "react";
import axios from "axios";

import { PlayerInfo } from "../../types/types";


interface llmQuestion {
    text: string,
    session_id: string,
}



export default function useLLM(playerInfo: PlayerInfo | null) {
    const [sessionID, setSessionID] = useState<string | null>(null);
    const [disabled, setDisabled] = useState(false);

    const [llmInputValue, setllmInputValue] = useState("");
    const [llmConversation, setllmConversation] = useState<string[]>([]);
    const [llmQuestions, setllmQuestions] = useState<string[]>([]);
    const [llmResponseCode, setllmResponseCode] = useState(0);
    const [llmResponse, setllmResponse] = useState<string[]>([]);

    const genLLM = () => {
        if (!playerInfo) {
            return
        }
        setllmResponseCode(1);
        axios.post('http://127.0.0.1:5000/api/llm/', playerInfo)
            .then(res => {
                console.log("Response data: ", res.data);
                setllmResponse(res.data.tips);
                setllmResponseCode(2);
                setSessionID(res.data.session_id);
            })
            .catch(err => {
                console.error(err)
                setllmResponseCode(-1);
            })
            .finally(() => setDisabled(true));
    }

    const askLLM = () => {
        setDisabled(true);
        if (!playerInfo || !sessionID) {
            return
        }
        if (llmQuestions.length >= 5) {
            setllmConversation([...llmConversation, "You have reached your question limit. Please try again later."]);
            return;
        }

        let query: llmQuestion = { text: llmInputValue, session_id: sessionID };
        setllmQuestions([...llmQuestions, llmInputValue]);
        axios.post('http://127.0.0.1:5000/api/llm/conversation', query)
            .then(res => {
                //setllmConversation(res.data.text);
                setllmConversation([...llmConversation, res.data.text]);
            })
            .catch(err => {
                console.error(err)
            })
            .finally();

    }

    return {
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
        askLLM,
    };

}