import React, {useEffect, useState} from 'react'
import {useParams, useNavigate, use} from 'react-router-dom'

import {
    Container, Main, Button, CardInfo, DictorSearch,
    Media, Socials, Smi, SocialPub, Statistics, PhotoSearch
} from '../../components'
import styles from './styles.module.css'
import api from '../../api'

const SingleCard = ({loadItem}) => {
    const navigate = useNavigate()
    const info = 'info'
    const media = 'media'
    const social = 'social'

    const smi = 'smi'
    const speakers = 'speakers'
    const social_pub = 'social_pub'
    const photo = 'photo'
    const statistics = 'statistics'

    const {id} = useParams()
    const [leftButton, setLeftButton] = useState(info)
    const [rightButton, setRightButton] = useState(statistics)
    const [langs, setLangs] = useState({})

    const [posts, setPosts] = useState([])
    const [socStats, setSocStats] = useState([])
    const [allStats, setAllStats] = useState([])

    const getSetLang = () => {
        let langs = {}
        api
            .getLangsNames()
            .then((res) => {
                for (let i = 0; i < res.length; i++) {
                    langs[res[i].iso_639_3] = res[i].lang_name
                }
            })
            .catch(err => {
                console.log('Ошибка при сборе языков:', err)
            })
        setLangs(langs)
    }

    const getPublications = ({social_id = null}) => {
        api
            .getScsSearch({card_id: id, social_id: social_id, aggs: false})
            .then((res) => {
                setPosts(res.article_list)
            })
    }

    const getSocialStatistics = ({social_id = null}) => {
        api
            .getStatistics({card_id: id, social_id: social_id})
            .then((res) => {
                setSocStats(res.statistics)
                setAllStats(res.all_stats)
            })
    }

    let left_buttons = [
        {
            title: 'Общая информация',
            click: () => {
                setLeftButton(info)
                getSocialStatistics({uuid: null})
            },
            disabled: false,
            isActive: leftButton === info,
            help: 'Перейти на вкладку общей информации о персоне'
        },
        {
            title: 'Социальные сети',
            click: () => {
                setLeftButton(social)
            },
            disabled: false,
            isActive: leftButton === social,
            help: 'Перейти на вкладку c информацией о социальных сетях, связанных с персоной'
        },
        {
            title: 'Работа с медиафайлами',
            click: () => {
                setLeftButton(media)
            },
            disabled: false,
            isActive: leftButton === media,
            help: 'Перейти на вкладку для работы с медиафайлами, где есть возможность добавить или удалить фотографии, аудио или видео файлы, связанных с персоной'
        }
    ];

    let right_buttons = [
        {
            title: 'СМИ о персоне',
            click: () => {
                setRightButton(smi)
            },
            disabled: false,
            isActive: rightButton === smi,
            help: 'Перейти на вкладку СМИ, где есть возможность ознакомится со статистикой и поисковой выдачей о персоне'
        },
        {
            title: 'Публикации в соц. сетях',
            click: () => {
                setRightButton(social_pub),
                    getPublications({social_id: null})
            },
            disabled: false,
            isActive: rightButton === social_pub,
            help: 'Перейти на вкладку с публикациями о персоне в социальных сетях'
        },
        {
            title: 'Дикторы',
            click: () => {
                setRightButton(speakers)
            },
            disabled: false,
            isActive: rightButton === speakers,
        },
        {
            title: 'Поиск по фото',
            click: () => {
                setRightButton(photo)
            },
            disabled: false,
            isActive: rightButton === photo,
        },
        {
            title: 'Статистика',
            click: () => {
                setRightButton(statistics),
                    getSocialStatistics({uuid: null})
            },
            disabled: false,
            isActive: rightButton === statistics,
            help: 'Перейти на вкладку отображения статистики в социальных сетях, связанных с персоной'
        },

    ];

    useEffect(() => {
        document.title = 'Персона';
    }, []);

    useEffect((_) => {
        getSocialStatistics({uuid: null})
    }, [])

    useEffect(() => {
        getSetLang()
    }, []);

    return (
        <Main>
            <Container>
                <div className={styles.container}>
                <Button className={`btn btn-outline-secondary m-2`}
                    title='Назад'
                    key='Назад'
                    clickHandler={(_) => {
                        navigate(`/fpk/`)
                    }}
                    isActive={false}
                    >
                    Назад
                </Button>
                    <div className={styles.left}>
                        {left_buttons.map((button) => (
                            <Button className={`btn btn-outline-secondary ${button.isActive ? 'active' : ''} m-2`}
                                    title={button.help}
                                    key={button.title}
                                    clickHandler={(_) => {
                                        setLeftButton('');
                                        button.click({id});
                                    }}
                                    isActive={button.isActive}
                            >
                                {button.title}
                            </Button>
                        ))}
                        {leftButton === info && <CardInfo
                            setLeftButton={setLeftButton}
                            social={social}
                            allStats={allStats}
                        />}
                        {leftButton === media && <Media/>}
                        {leftButton === social && <Socials
                            getPublications={getPublications}
                            getSocialStatistics={getSocialStatistics}
                            setRightButton={setRightButton}
                            social_pub={social_pub}
                            statistics={statistics}
                        />}
                    </div>

                    <div className={styles.right}>
                        {right_buttons.map((button) => (
                            <Button className={`btn btn-outline-secondary ${button.isActive ? 'active' : ''} m-2`}
                                    title={button.help}
                                    key={button.title}
                                    disabled={button.disabled}
                                    clickHandler={(_) => {
                                        setRightButton('');
                                        button.click({id});
                                    }}
                                    isActive={button.isActive}
                            >
                                {button.title}
                            </Button>
                        ))}
                        {rightButton === smi && <Smi langs={langs}/>}
                        {rightButton === social_pub && <SocialPub
                            getPublications={getPublications}
                            posts={posts}
                            langs={langs}/>}
                        {rightButton === statistics && <Statistics
                            getSocialStatistics={getSocialStatistics}
                            socStats={socStats}/>}
                        {rightButton === photo && <PhotoSearch langs={langs}/>}
                        {rightButton === speakers && <DictorSearch langs={langs}/>}
                    </div>
                </div>
            </Container>
        </Main>
    );
};

export default SingleCard;
