import { useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import { Chart as ChartJS } from 'chart.js/auto' // Не удалять

import styles from './style.module.css'

const Statistics = ({ getSocialStatistics, socStats }) => {

  useEffect(() => {
    document.title = 'Статистика';
  }, []);

  const StatsBlock = ({item}) => {
    return (
      <Line
        type="line"
        width={160}
        height={60}
        options={{plugins: {
          title: {
            display: true,
            text: item.text,
            fontSize:30
          },
          legend: {
            display: true,
            position: "bottom",
          }
        }}}
        data={item}
      />
    );
  }

  return (
      <div className={styles.container}>
        {socStats.length && socStats[0].datasets.length ? socStats.map((item, index) => (<StatsBlock key={index} item={item} />)) : <div>Нет данных. Подтвердите аккаунты или включите автоматический сбор.</div>}
      </div>
    );
  };

export default Statistics;
