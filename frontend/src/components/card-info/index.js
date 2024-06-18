import {useState, useEffect} from 'react'

import {Button, CardRead, CardEdit} from '../../components'
import styles from './style.module.css'

const CardInfo = ({setLeftButton, social, allStats}) => {
    const [read, setRead] = useState(true)

    useEffect(() => {
        document.title = 'Персона'
    }, []);

    return (
        <div>
            {read && <CardRead allStats={allStats}/>}
            {!read && <CardEdit setRead={setRead}/>}
            <div>
                <Button
                    title={read ? "Перейти в раздел редактирования карточки" : "Отменить изменения"}
                    modifier="style_dark-blue"
                    className={read ? "btn btn-success" : "btn btn-danger"}
                    clickHandler={(_) => {
                        read ? setRead(false) : setRead(true);
                    }}
                >
                    {read ? 'Редактировать' : 'Отменить редактирование'}
                </Button>
                <Button
                    title="Перейти в раздел найденных аккаунтов, которые могут быть связаны с персоной и для ознакомления с личными данными"
                    className="btn btn-info m-2"
                        modifier="style_dark-blue"
                        clickHandler={(_) => {
                            setLeftButton(social);
                        }}
                >
                    Посмотреть обновления
                </Button>
            </div>
        </div>
    );
};

export default CardInfo;
