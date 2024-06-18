import {v4 as uuid} from 'uuid'

import {useState, useEffect} from 'react'
import {useNavigate, useParams} from 'react-router-dom'
import Select from 'react-select';

import {Button, Input} from '../../components'
import styles from './style.module.css'
import api from '../../api'
import defaultAvatar from '../../images/defaultAvatar.jpeg';


const Socials = (
    {
        getPublications, getSocialStatistics,
        setRightButton, social_pub, statistics
    }) => {
    const search = 'search'
    const found = 'found'
    const confirmed = 'confirmed'

    const linkedin = 'linkedin'
    const twitter = 'twitter'
    const vk = 'vk'
    const reddit = 'reddit'
    const instagram = 'instagram'
    const facebook = 'facebook'
    const telegram = 'telegram'
    const flickr = 'flickr'
    const tumblr = 'tumblr'
    const change_org = 'change.org'

    const navigate = useNavigate()
    const {id} = useParams()
    const [activeButton, setActiveButton] = useState(found)
    const [source, setSource] = useState('')
    const [data, setData] = useState([])
    const [searchData, setSearchData] = useState([])
    const [confirmScs, setConfirmScs] = useState([])
    const [activeButtons, setActiveButtons] = useState({});

    const searchFields = [
        {value: 'username', label: 'Имя в соц сети'},
        {value: 'full_name', label: 'Полное имя'}
    ]

    const appendConfirmScs = ({social_id}) => {
        setConfirmScs([...confirmScs, social_id])
    }

    const discardConfirmScs = ({social_id}) => {
        const arrayWithoutD = confirmScs.filter(function (letter) {
            return letter !== social_id;
        });
        setConfirmScs(arrayWithoutD)
    }

    const getSocialFound = ({source = ''}) => {
        api
            .getSocialNetworkFound({card_id: id, source: source})
            .then((res) => {
                setData(res.pages);
            })
    }

    const getSocialConfirmed = ({source}) => {
        api
            .getSocialNetworkConfirmed({card_id: id, source: source})
            .then((res) => {
                setData(res.pages);
            })
    }

    const addSocial = ({ active_button = ''}) => {
        api.addSocialNetwork(
            {card_id: id, socials: confirmScs, source: source})
            .then((res) => {
                if (active_button !== search) {
                    setData(res.pages)
                }
                getPublications({social_id: null})
                getSocialStatistics({social_id: null});
                setConfirmScs([])
            })
            .catch((err) => {
                navigate(`/fpk/${id}`);
            })
    }

    const discardSocial = () => {
        api.discardSocialNetwork({card_id: id, socials: confirmScs})
            .then((res) => {
                setData(res.pages)
                getPublications({social_id: null})
                getSocialStatistics({social_id: null});
                setConfirmScs([])
            })
            .catch((err) => {
                navigate(`/fpk/${id}`);
            })
    }

    const getSearch = (value) => {
        switch (value.value) {
            case 'username':
                api.getSocialSearch({username: searchData}).then((res) => {
                    setData(res.pages)
                })
                break;
            case 'full_name':
                api.getSocialSearch({full_name: searchData}).then((res) => {
                    setData(res.pages)
                })
                break;
        }
    }

    let buttons = [
        {
            title: 'Поиск',
            click: () => {
                setActiveButton(search)
                setData([])
                setSource('')
            },
            disabled: false,
            isActive: activeButton === search,
        },
        {
            title: 'Подтвержденные аккаунты',
            click: () => {
                setActiveButton(confirmed)
                getSocialConfirmed({source: ''})
                setSource('')
            },
            disabled: false,
            isActive: activeButton === confirmed,
        },
        {
            title: 'Найденные аккаунты',
            click: () => {
                setActiveButton(found)
                getSocialFound({source: ''})
                setSource('')
            },
            disabled: false,
            isActive: activeButton === found,
        },
    ];

    useEffect(() => {
        document.title = 'Социальные сети';
      }, []);

    useEffect((_) => {
        getSocialFound({source: ''})
    }, [])

    return (
        <div className={styles.container}>
            {buttons.map((button) => (
                <Button
                    title={
                    button.title === "Поиск" ? "Перейти во вкладку поиска социальных сетей"
                        : button.title === "Подтвержденные аккаунты" ? "Перейти во вкладку с подтвержденными аккаунтами"
                        : button.title === "Найденные аккаунты" ? "Перейти во вкладку найденных аккаунтов" : ""
                    }
                    className={`btn btn-outline-secondary ${button.isActive ? 'active' : ''} m-2`}
                        key={button.title}
                        clickHandler={(_) => {
                            button.click();
                        }}
                        disabled={button.disabled}
                        isActive={button.isActive}
                >
                    {button.title}
                </Button>
            ))}
            {}
            {activeButton !== search && <div>
                <div>
                <Button
                    title="Отобразить все найденные социальные сети"
                    className={`btn btn-outline-info m-2 ${source === '' ? 'active' : ''}`}
                    key={'all'}
                    clickHandler={(_) => {
                        setSource('')
                        {
                            activeButton === found ?
                                getSocialFound({source: ''}) :
                                getSocialConfirmed({source: ''})
                        }
                    }}
                    isActive={source === ''}>
                    Все соцсети
                </Button>
                </div>
                <div>
                {[facebook, instagram, telegram, twitter, reddit].map((button) => (
                    <Button
                        title={`Отобразить социальную сеть ${button}`}
                        className={`btn btn-outline-info m-2 ${source === button ? 'active' : ''}`}
                            key={button}
                            clickHandler={(_) => {
                                setSource(button)
                                {
                                    activeButton === found ?
                                        getSocialFound({source: button}) :
                                        getSocialConfirmed({source: button})
                                }
                            }}
                            isActive={source === button}
                    >
                        {button}
                    </Button>
                ))}
                </div>
                <div>
                {[linkedin, vk, flickr, tumblr, change_org].map((button) => (
                    <Button
                        title={`Отобразить социальную сеть ${button}`}
                        className={`btn btn-outline-info m-2 ${source === button ? 'active' : ''}`}
                            key={button}
                            clickHandler={(_) => {
                                setSource(button)
                                {
                                    activeButton === found ?
                                        getSocialFound({source: button}) :
                                        getSocialConfirmed({source: button})
                                }
                            }}
                            isActive={source === button}
                    >
                        {button}
                    </Button>
                ))}
                </div>
                {/* {[linkedin, twitter, vk, reddit, instagram, facebook,
                    telegram, flickr, tumblr, change_org
                ].map((button) => (
                    <Button
                        title={`Отобразить социальную сеть ${button}`}
                        className={`btn btn-outline-info m-2 ${source === button ? 'active' : ''}`}
                            key={button}
                            clickHandler={(_) => {
                                setSource(button)
                                {
                                    activeButton === found ?
                                        getSocialFound({source: button}) :
                                        getSocialConfirmed({source: button})
                                }
                            }}
                            isActive={source === button}
                    >
                        {button}
                    </Button>
                ))} */}
                {/* <Button
                    title="Отобразить все найденные социальные сети"
                    className={`btn btn-outline-info m-2 ${source === '' ? 'active' : ''}`}
                    key={'all'}
                    clickHandler={(_) => {
                        setSource('')
                        {
                            activeButton === found ?
                                getSocialFound({source: ''}) :
                                getSocialConfirmed({source: ''})
                        }
                    }}
                    isActive={source === ''}>
                    Все соцсети
                </Button> */}
                    <div title={confirmScs.length === 0 ?"Для сохранения изменений необходимо выбрать один или несколько аккаунтов":"Сохранить изменения"}>
                        <Button
                                className={'btn btn-success m-2'}
                                clickHandler={(_) => {
                                    {activeButton === found ? addSocial({active_button: activeButton}) : discardSocial()}
                                    setRightButton(social_pub)
                                }}
                                disabled={confirmScs.length === 0}
                        >
                            Сохранить
                        </Button>
                    </div>
                </div>}
            {activeButton === search &&
                <>
                    <Input
                        name="search"
                        onChange={(e) => {
                            const value = e.target.value;
                            setSearchData(value);
                        }}
                        value={searchData}
                    />
                    <Select
                        className="basic-single"
                        classNamePrefix="select"
                        defaultValue={searchFields[0]}
                        onChange={getSearch}
                        name="color"
                        options={searchFields}
                    />

                    <div
                        style={{
                            color: 'hsl(0, 0%, 40%)',
                            display: 'inline-block',
                            fontSize: 12,
                            fontStyle: 'italic',
                            marginTop: '1em',
                        }}
                    >
                    <Button className={'btn btn-success m-2'}
                        clickHandler={(_) => {
                            addSocial({active_button: activeButton})
                            setRightButton(social_pub)
                        }}
                    >
                        Сохранить
                    </Button>
                    </div>
                </>
            }
            {data.map((item) => (
                <ul key={uuid()}>
                    {' '}
                    <div className={styles.tableContainer}>
                        <table>
                            <tbody>
                            <tr>
                                <td>
                                    <img style={{width: '200px', height: '200px'}}
                                         src={item.profilePicture.internalUrl ? item.profilePicture.internalUrl: defaultAvatar}
                                         onError={(e) => {e.target.onerror = null; e.target.src = defaultAvatar}}
                                         className={styles.card__image}
                                         alt='User Avatar'
                                    />
                                </td>

                            </tr>
                            </tbody>
                        </table>

                    <table className={styles.currentTable}>
                        <tbody>
                        <tr>
                            <td>Имя:</td>
                            <td>{item.page.fullName}</td>
                        </tr>
                        <tr>
                            <td>Имя пользователя:</td>
                            <td>{item.page.username}</td>
                        </tr>
                        <tr>
                            <td>Число подписчиков:</td>
                            <td>{item.page.followersCount}</td>
                        </tr>
                        <tr>
                            <td>Имя соцсети:</td>
                            <td>{item.sourceName}</td>
                        </tr>
                        <tr>
                            <td>Число друзей:</td>
                            <td>{item.page.friendsCount}</td>
                        </tr>
                        <tr>
                            <td>Число подписок:</td>
                            <td>{item.page.followingCount}</td>
                        </tr>
                        <tr>
                            <td>Число постов:</td>
                            <td>{item.page.postsCount}</td>
                        </tr>
                        <tr>
                            <td>SocialID:</td>
                            <td>{item.page.socialId}</td>
                        </tr>
                        </tbody>
                    </table>
                    </div>
                    {activeButton !== confirmed &&
                        <Button
                            title={confirmScs.includes(item.page.socialId)?"Удалить аккаунт": 'Подтвердить информацию, найденную в аккаунте, с персоной' }
                        className={`${confirmScs.includes(item.page.socialId) ? 'btn btn-danger': 'btn btn-success'} m-2`}
                        clickHandler={(_) => {
                            confirmScs.includes(item.page.socialId) ?
                                discardConfirmScs({social_id: item.page.socialId}) :
                                appendConfirmScs({social_id: item.page.socialId})
                        }}
                    >
                        {confirmScs.includes(item.page.socialId) ? 'Удалить' : 'Подтвердить'}
                    </Button>}
                    {activeButton === confirmed && <>
                        <Button
                            title={confirmScs.includes(item.page.socialId)?'Подтвердить информацию, найденную в аккаунте, с персоной': "Удалить аккаунт"}
                            className={`${confirmScs.includes(item.page.socialId) ? 'btn btn-success':'btn btn-danger'} m-2 `}
                            clickHandler={(_) => {
                                confirmScs.includes(item.page.socialId) ?
                                    discardConfirmScs({social_id: item.page.socialId}) :
                                    appendConfirmScs({social_id: item.page.socialId})
                            }}
                        >
                            {confirmScs.includes(item.page.socialId) ?
                                'Подтвердить' : 'Удалить'}
                        </Button>

                        <Button className={`btn btn-outline-info ${activeButtons[item.page.socialId] === 'statistics' ? 'active' : ''} m-2`}
                            clickHandler={(_) => {
                                getSocialStatistics({social_id: item.page.socialId})
                                setRightButton(statistics)
                                setActiveButtons({[item.page.socialId]: 'statistics'});
                            }}>Статистика по аккаунту
                        </Button>

                        <Button className={`btn btn-outline-info ${activeButtons[item.page.socialId] === 'social_pub' ? 'active' : ''} m-2`}
                            clickHandler={(_) => {
                                getPublications({social_id: item.page.socialId})
                                setRightButton(social_pub)
                                setActiveButtons({[item.page.socialId]: 'social_pub'});
                            }}>Публикации
                        </Button>

                    </>}
                </ul>
            ))}
        </div>
    );
};

export default Socials;