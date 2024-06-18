import {useState, useEffect} from 'react'
import {useNavigate} from 'react-router-dom'
import AsyncSelect from 'react-select/async'

import styles from './style.module.css'
import {ImageInput, AttrInput, Input, Button} from '../../components'
import api from '../../api'
import media_type from '../../configs/constants'

const CardCreate = () => {
    const history = useNavigate()
    const [cardFullName, setCardFullName] = useState('')
    const [cardAvatar, setCardAvatar] = useState(null)
    const [cardAttrs, setCardAttrs] = useState([])
    const [autoCollect, setAutoCollect] = useState(false)
    const [attrs, setAttrs] = useState([])
    const [wikiSearch, setWikiSearch] = useState([])
    const {image, audio, video, file, date} = media_type

    const [isEmpty, setIsEmpty] = useState(true); // (не)пустой input
    const [hasBeenActive, setHasBeenActive] = useState(false);



    const checkIfDisabled = () => {
        return cardFullName === '' || cardAvatar === '' || cardAvatar === null
    }

    const WikiSearchResult = (inputValue) => {
        api.getWikiSearsh({keyword: inputValue})
            .then((res) => {
                setWikiSearch(res.cards)
            })
        return wikiSearch
    }

    const loadOptions = (inputValue, callback) => {
        callback(WikiSearchResult(inputValue))
    };

    const handleSelect = (data) => {
        setCardFullName(data.value);
    }

    useEffect((_) => {
        api
            .getAttrs({attr_type: ''})
            .then((res) => {
                setAttrs(
                    res.results.filter(
                        attr => ![image, audio, video, file].includes(
                            attr.attr_type)
                    )
                )
            })
            .catch((err) => {
                history('/fpk');
            })
    }, [])

    const onSubmitClickHandler = (e) => {
        if (cardFullName === '') {
            alert('Заполните поле: Наименование объекта (ФИО)')
            return
        }
        if (cardAvatar === null) {
            alert('Заполните поле: Фото')
            return
        }
        e.preventDefault();
        const data = {
            full_name: cardFullName,
            avatar: cardAvatar,
            auto_collect: autoCollect,
            attrs: cardAttrs.map(item => ({
                id: item.id,
                value: item.value,
            })),
        };
        api
            .createCard(data)
            .then((res) => {
                history(`/fpk/${res.id}`);
            })
            .catch((err) => {
                const {non_field_errors} = err;
                if (non_field_errors) {
                    return alert(non_field_errors.join(', '));
                }
                const errors = Object.values(err);
                if (errors) {
                    alert(errors.join(', '));
                }
            });
    }
    const onChangeNameClickHandler = (e) => {
        const value = e.target.value;
        setCardFullName(value);
        if (value.trim().length > 0) {
            setIsEmpty(false);
        } else {
            setIsEmpty(true);
        }
        setCardFullName(value);
    }
    const onChangeFileClickHandler = (file) => {
        setCardAvatar(file)
    }
    const onChangeAutoCollectClickHandler = (value) => {
        setAutoCollect(value)
    }

    const onChangeInputHandler = (e) => {
        const value = e.target.value;
        onChangeAutoCollectClickHandler(value);
    }

    return (
        <>
            <div className={styles.myForm}>
                <div title="Введите ФИО" className={styles.formElement}>
                    <AsyncSelect
                        cacheOptions
                        loadOptions={loadOptions}
                        onChange={handleSelect}
                        placeholder="Поиск"
                        noOptionsMessage={() => "Нет результатов поиска"}
                    />
                </div>

                <div title="Введите ФИО">
                    <input type="text"
                           placeholder="Наименование объекта (ФИО)*"
                           name="name"
                           onChange={onChangeNameClickHandler}
                           value={cardFullName}
                           onBlur={() => setHasBeenActive(true)}
                           className={`${styles.formElement} ${isEmpty && hasBeenActive ? styles.error : ''}`}
                    />
                </div>
                <div>
                    {attrs.map(attr =>
                        <AttrInput
                            key={attr.id}
                            attr={attr}
                            cardAttrs={cardAttrs}
                            setCardAttrs={setCardAttrs}
                            className={styles.formElement}
                        />
                    )}
                </div>
                <div title="Загрузите изображение"
                     className={styles.formElement}>
                    <ImageInput
                        onChange={onChangeFileClickHandler}
                        label="Загрузить фото*"
                    />
                </div>
                <div title="Автоматический сбор работает только в случае отсутствия подтвержденных социальных сетей"
                     className="custom-control custom-checkbox">
                    <input
                        style={{width: '20px', height: '20px', marginRight: '10px'}}
                        type="checkbox"
                        className="custom-control-input"
                        id="auto_collect"
                        onChange={onChangeInputHandler}></input>
                    <label className="custom-control-label" htmlFor="customCheck1">Автоматический сбор</label>
                </div>
                <button
                    onClick={onSubmitClickHandler}
                    // disabled={checkIfDisabled()}
                    className="btn btn-success col-3">
                    Создать карточку
                </button>
            </div>
        </>
    );
};

export default CardCreate
