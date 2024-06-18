import {Line} from 'react-chartjs-2'
import {Chart as ChartJS} from 'chart.js/auto' // Не удалять

const StatBlock = ({item}) => {
    return (
        <Line
            type="line"
            width={160}
            height={60}
            options={{
                plugins: {
                    title: {
                        display: true,
                        text: 'Статистика за неделю',
                        fontSize: 30
                    },
                    legend: {
                        display: true,
                        position: "bottom",
                    }
                }
            }}
            data={item}
        />
    );
}

export default StatBlock