import React, {useState, useEffect} from 'react'
import {useParams, useNavigate} from 'react-router-dom'

import {Button, StatBlock} from '../../components'
import styles from './style.module.css'
import api from '../../api'

const SocialPub = ({langs}) => {
    const {id} = useParams()
    const navigate = useNavigate()
    const [data, setData] = useState([])
    const [stats, setStats] = useState(false)
    const [isLoading, setIsLoading] = useState(true);
    const [statsPub, setStatsPub] = useState([])

    const getPub = (aggs) => {
        api
            .getScsSearch({card_id: id, social_id: null, aggs: aggs})
            .then((res) => {
            {aggs ? setStatsPub(res.statistics) : setData(res.article_list)}
            setIsLoading(false)
            })
            .catch((err) => {
            navigate(`/fpk/${id}`);
            })
        }

    const Publication = ({item, langs}) => {
        let date = new Date(item.publish_date * 1000);
        let formattedTime = date.toLocaleString('ru-RU', {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric'
        })
        
        let title = ""
        if (item.author) {
            if (item.author.fullName) {
                if (item.author.fullName instanceof Array) {
                   title =  item.author.fullName[0]
                } else {
                    title =  item.author.fullName
                }
            }
        }
        return (  
            
            <>
                <style>
                    {`
                    .searched_word {
                    background-color: #ff9; 
                        font-weight: bold; 
                    }
                `}
                </style>
                <div className={styles.publications}>
                    <div className={styles.header}>
                        <span> {item.domain.domain}</span>
                        <span>{item.domain.domain !== item.domain.title && " " + item.domain.title}</span>
                    </div>

                    <div className={styles.body}>
                        <div>
                            {item.media && item.media.type === 'image' ? 
                            <img src={item.media.internalUrl} className={styles.card__image}></img> : ''}
                            {item.media && item.media.type === 'video' ? 
                            <video src={item.media.internalUrl} className={styles.card__image} controls></video> : ''}
                        </div>
                        <div>
                        <div className={styles.title}>
                            <a href={`/pao/newPAO/storunit.html?article_uuid=${item.article_uuid}&index_type=${item.index_type}`}
                               className={styles.link}>
                                {title}
                            </a>
                        </div>
                        <span dangerouslySetInnerHTML={{ __html: item.cnt }}></span>

                        <div><span className={styles.text_muted}>Дата публикации: </span>{formattedTime}</div>
                        <div><span className={styles.text_muted}>Источник: </span><span>{item.domain.domain}</span></div>
                        <div><span
                            className={styles.text_muted}>Язык: </span> {langs[item.lang] ? langs[item.lang] : item.lang}
                        </div>
                        <div>
                            <span className={styles.text_muted}>URL: </span>
                                {item.url}
                        </div>
                        </div>
                    </div>
                </div>
            </>
        )
    }

    useEffect(() => {
        document.title = 'Публикации';
    }, []);

    useEffect((_) => {
        getPub(false)
    }, [])

    return (
        <div className={styles.container}>
            <Button className={`btn ${stats ? 'btn-info' : 'btn-outline-info'} m-2`}
                clickHandler={(_) => {
                setStats(true)
                getPub(true)
                }}
                >
                Статистика
            </Button>
            <Button className={`btn ${!stats ? 'btn-info' : 'btn-outline-info'} m-2`}
                clickHandler={(_) => {
                setStats(false)
                getPub(false)
                }}
                >
                Поисковая выдача
            </Button>
            {isLoading && <div className={styles.loader}></div>}
            {!stats ? data.map((item) => (
                <Publication item={item} langs={langs} key={item.article_uuid}/>
            )) :
                statsPub.map((item, index) => (<StatBlock key={index} item={item} />))
            }
        </div>
    );
};

export default SocialPub;
