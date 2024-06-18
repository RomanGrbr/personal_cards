import React, {useEffect, useState} from 'react'
import {useParams, useNavigate} from 'react-router-dom'

import {Button, SmiCard, StatBlock} from '../../components'
import styles from './style.module.css'
import api from '../../api'

const Smi = ({langs}) => {
    const {id} = useParams()
    const navigate = useNavigate()
    const [data, setData] = useState([])
    const [stats, setStats] = useState(false)
    const [statsSmi, setStatsSmi] = useState([])
    const [isLoading, setIsLoading] = useState(true);

    const getSmi = (aggs) => {
        api
            .getSmiSearch({
                card_id: id, aggs: aggs,
            })
            .then((res) => {
                {
                    aggs ? setStatsSmi(res.statistics) : setData(res.article_list)
                }
                setIsLoading(false);
            })
            .catch((err) => {
                navigate(`/fpk/${id}`);
            })
        }

    useEffect(() => {
        document.title = 'СМИ о персоне';
    }, []);

    useEffect((_) => {
        getSmi(false)
    }, [])

    return (
        <div className={styles.container}>
            <Button className={`btn ${stats ? 'btn-info' : 'btn-outline-info'} m-2`}
                    clickHandler={(_) => {
                        setStats(true)
                        getSmi(true)
                    }}
                    title="Перейти в раздел статистики количества упоминания в СМИ"
            >
                Статистика
            </Button>
            <Button className={`btn ${!stats ? 'btn-info' : 'btn-outline-info'} m-2`}
                    clickHandler={(_) => {
                        setStats(false)
                        getSmi(false)
                    }}
                    title="Перейти в раздел поисковой выдачи, для просмотра новостей связанных с персоной"
            >
                Поисковая выдача
            </Button>
            {isLoading && <div className={styles.loader}></div>}
            {!stats ? data.map((item) => (
                    <SmiCard item={item} langs={langs} key={item.article_uuid}/>
                )) :
                statsSmi.map((item, index) => (<StatBlock key={index} item={item}/>))
            }

        </div>
    );
};

export default Smi;
