export interface HeroInfo {
    name: string;
    accuracy: number;
    matchesPlayed: number;
    totalKills: number;
    totalDeaths: number;
    totalAssists: number;
    mvp: number;
    svp: number;
    wins: number;
    damage: number;
    heal: number;
    damage_taken: number;
}

// Related Details to Maps such as name, image, and id
export interface MapDetails{
    game_mode: string;
    name: string;
    image_url: string;
    location: string;
}

export interface MapInfo {
    map_id: number;
    matches: number;
    wins: number;
    kills: number;
    deaths: number;
    assists: number;
}

export interface PlayerInfo {
    name: string;
    icon: string;
    rank: string;
    level: string;
    topHeroes: HeroInfo[];
    topMaps: MapInfo[];
}



export interface HomepageProps {
    contents: string;
    playerInfo: PlayerInfo | null;
    showGraphic: string;
    llmResponseCode: number;
    disabled: boolean;
    llmResponse: string[];
    llmConversation: string[];
    llmQuestions: string[];

    genLLM: () => void;
    askLLM: () => void;
    setShowGraphic: (value: string) => void;
    setllmInputValue: (value: string) => void;

}

export interface SwitcherProps {
    showHeroGraphic: string;
    setShowHeroGraphic: (value: string) => void;
}

export interface LeaderboardHero {
    name: string;
    role: string;
    matches: number;
    wins: number;
    kills: number;
    deaths: number;
    assists: number;
    win_rate: number;
    play_time: number;
    total_hero_damage: number;
    total_damage_taken: number;
    total_hero_heal: number;
    mvps: number;
    svps: number;
    kpg: number;
    apg: number;
    dpg: number;
    mvp_rate: number;
    svp_rate: number;

}