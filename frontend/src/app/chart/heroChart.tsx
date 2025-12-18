import { heroList, CHART_COLORS, numbers } from './utils'
import { HeroInfo } from '../types/types';

export const options = (label: string) => {

    return {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: 'white', // legend text color
                },
                title: {
                    text: label,
                    display: true,
                    color: 'white',
                    font: {
                        size: 24
                    },
                    size: 24
                }
            },

        },
        scales: {
            x: {
                ticks: {
                    color: 'white', // x-axis label color
                    font: {
                        size: 15
                    },
                },

            },
            y: {
                ticks: {
                    callback: function (value: string | number) {
                        if (label === 'Accuracy')
                            return value + '%';
                        return value;
                    },
                    color: 'white', // y-axis label color
                    size: 18,
                    font: {
                        size: 15
                    },
                },
            },
        },


    }
};


// SORT BY WORST ACCURACY TO BEST

export const BarData = (data: HeroInfo[], statType: string) => {
    const labels = heroList(data);

    const accs = numbers(data, true, statType, labels);
    const proAccs = numbers(data, false, statType, labels);

    return {
        labels: labels,
        datasets: [
            {
                label: 'You',
                data: accs,
                borderColor: CHART_COLORS.purple,
                backgroundColor: CHART_COLORS.purple,
                barHeight: 500,

                //transparentize(CHART_COLORS.red, 0.5),
            },
            {
                label: 'Top 1000 Players',
                data: proAccs,
                borderColor: CHART_COLORS.orange,
                backgroundColor: CHART_COLORS.orange,
                barHeight: 500,
                //transparentize(CHART_COLORS.blue, 0.5),
            }
        ]
    }
};