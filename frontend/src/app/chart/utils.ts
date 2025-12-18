import { HeroInfo } from "../types/types";
import { TopPlayerAccuracy } from "../lib/topPlayerAccuracy";

const HEROES = [
    'cloak & Dagger',
    'invisible woman',
    'angela',
    'blade',
    'star lord',
    'magik',
    'mantis',
    'groot',
    'doctor strange',
    'the thing'
];


export function heroList(data: HeroInfo[]) {
    // var count = 8;
    var values: string[] = [];
    var i = 0;
    if (!data) {
        values.push(HEROES[0]);
        return values;
    }

    data.map((hero) => {
        values.push(hero.name.charAt(0).toUpperCase() + hero.name.slice(1));
        i += 1;
    });

    return values;
}

export function numbers(playerData: HeroInfo[], user: boolean, statType: string, labels: string[]) {
    //var max = (statType === 'accuracy') ? 100 : 20;
    var count = playerData.length;
    var data = [];
    var value;

    const validStatTypes = ['kd', 'assists', 'accuracy']

    if (user) {
        var i = 0;

        if (playerData) {
        playerData.map((hero) => {
            let val = hero['accuracy'] * 100;
            if (statType === 'kd') {
                val = (hero['totalDeaths'] > 0) ? hero['totalKills'] / hero['totalDeaths'] : hero['totalKills'];
            }
            if (statType === 'assists') { val = Math.round(hero['totalAssists'] / hero['matchesPlayed']) }
            //  if (statType !== 'accuracy' && val > max) {
            //     max = (Math.floor(max / 5) + 1) * 5
            //  }
            data.push(val);
            i += 1;
        });
    }
        for (; i < count; ++i) {
            data.push(0);
        }
        return data;
    }

    for (let i = 0; i < count; i++) {
        let found = false;
        for (const [player, stats] of Object.entries(TopPlayerAccuracy)) {
            if (player === labels[i].toLowerCase()) {
                let val = stats['accuracy'] * 100;
                if (statType === 'kd') {
                    val = (stats['deaths'] > 0) ? stats['kills'] / stats['deaths'] : stats['kills'];
                }
                if (statType === 'assists') { 
                    val = (stats['matches'] > 0) ? stats['assists'] / stats['matches'] : stats['assists'];
                }

                data.push(val);
                found = true;
                break;
            }
        }
        if (!found) { data.push(value); }

    }

    return data;
}

// export function transparentize(value, opacity) {
//   var alpha = opacity === undefined ? 0.5 : 1 - opacity;
//   return colorLib(value).alpha(alpha).rgbString();
// }

export const CHART_COLORS = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};